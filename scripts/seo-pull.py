#!/usr/bin/env python3
"""
AETHON — SEO insights pull (Google Search Console + PageSpeed Insights).

This is *tooling*, NOT part of the website. The site itself stays buildless and
static (a single index.html); this script only reads metrics and writes reports.
It runs in CI (.github/workflows/seo-insights.yml) on a schedule, or locally.

Auth — nothing secret lives in the repo; both come from env vars / GitHub secrets:
  GSC_SA_KEY   contents of a Google service-account JSON key whose client_email
               has been added as a USER on the Search Console *domain* property
               (sc-domain:aethon.house). Read scope only.
  PSI_API_KEY  a PageSpeed Insights API key (optional — PSI also runs keyless,
               but the shared anonymous quota is small and often exhausted).

Either may be absent: the script degrades gracefully and still writes a report
("unavailable — pending setup") so the workflow stays green before you wire the
secrets up.

Output: a dated Markdown report + raw JSON in --out (default seo-reports/), and
the same summary appended to $GITHUB_STEP_SUMMARY when running in Actions.
"""
import os
import sys
import json
import argparse
import datetime
import urllib.parse
import urllib.request

SITE = os.environ.get("SEO_SITE", "aethon.house")
PROPERTY = f"sc-domain:{SITE}"
PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
GSC_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"


# ---------- Search Console ----------
def gsc_service():
    raw = os.environ.get("GSC_SA_KEY")
    if not raw:
        return None, "no GSC_SA_KEY secret set"
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        return None, "google-api-python-client / google-auth not installed"
    try:
        info = json.loads(raw)
        creds = service_account.Credentials.from_service_account_info(info, scopes=[GSC_SCOPE])
        return build("searchconsole", "v1", credentials=creds, cache_discovery=False), None
    except Exception as ex:  # noqa: BLE001
        return None, f"credential error: {ex}"


def _gsc_rows(svc, start, end, dimensions, limit):
    body = {"startDate": start, "endDate": end, "dimensions": dimensions,
            "rowLimit": limit, "dataState": "all"}
    return svc.searchanalytics().query(siteUrl=PROPERTY, body=body).execute().get("rows", [])


def pull_gsc(days):
    svc, err = gsc_service()
    if not svc:
        return {"available": False, "reason": err}
    # GSC data lags ~2 days; look back `days` from there.
    end = datetime.date.today() - datetime.timedelta(days=2)
    start = end - datetime.timedelta(days=days)
    s, e = start.isoformat(), end.isoformat()
    try:
        totals = _gsc_rows(svc, s, e, [], 1)
        return {
            "available": True,
            "range": [s, e],
            "totals": totals[0] if totals else {},
            "queries": _gsc_rows(svc, s, e, ["query"], 25),
            "pages": _gsc_rows(svc, s, e, ["page"], 25),
        }
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": f"query failed: {ex}"}


# ---------- PageSpeed Insights ----------
def pull_psi(strategy):
    params = {"url": f"https://{SITE}/", "strategy": strategy,
              "category": ["performance", "accessibility", "best-practices", "seo"]}
    key = os.environ.get("PSI_API_KEY")
    if key:
        params["key"] = key
    url = f"{PSI_ENDPOINT}?{urllib.parse.urlencode(params, doseq=True)}"
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = json.load(resp)
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": str(ex)}
    if "error" in data:
        return {"available": False, "reason": data["error"].get("message", "")}
    lr = data.get("lighthouseResult", {})
    cats, audits = lr.get("categories", {}), lr.get("audits", {})
    return {
        "available": True,
        "scores": {k: round(v["score"] * 100) for k, v in cats.items() if v.get("score") is not None},
        "metrics": {m: audits.get(m, {}).get("displayValue", "n/a") for m in
                    ["first-contentful-paint", "largest-contentful-paint",
                     "total-blocking-time", "cumulative-layout-shift", "speed-index"]},
        "field": data.get("loadingExperience", {}).get("overall_category", "insufficient real-user data"),
    }


# ---------- report ----------
def render(gsc, psi_mobile, psi_desktop, when):
    out = [f"# AETHON — SEO insights · {when}", ""]

    out.append("## PageSpeed Insights (lab)")
    for label, psi in [("Mobile", psi_mobile), ("Desktop", psi_desktop)]:
        if psi.get("available"):
            sc = psi["scores"]
            out.append(f"- **{label}** — perf **{sc.get('performance', '?')}** · a11y {sc.get('accessibility', '?')} · "
                       f"best-practices {sc.get('best-practices', '?')} · SEO {sc.get('seo', '?')}  "
                       f"_(field: {psi['field']})_")
            m = psi["metrics"]
            out.append(f"    - LCP {m['largest-contentful-paint']} · CLS {m['cumulative-layout-shift']} · "
                       f"TBT {m['total-blocking-time']} · FCP {m['first-contentful-paint']} · SI {m['speed-index']}")
        else:
            out.append(f"- **{label}** — unavailable ({psi.get('reason', '')[:140]})")
    out.append("")

    out.append("## Search Console")
    if not gsc.get("available"):
        out.append(f"_Unavailable: {gsc.get('reason', '')[:200]}_")
        out.append("_(Normal right after verifying — give Google a few days of crawl + some traffic.)_")
    else:
        t = gsc.get("totals", {})
        out.append(f"Range **{gsc['range'][0]} → {gsc['range'][1]}**")
        if t:
            out.append(f"- **Totals** — clicks {int(t.get('clicks', 0))} · impressions {int(t.get('impressions', 0))} · "
                       f"CTR {t.get('ctr', 0) * 100:.1f}% · avg position {t.get('position', 0):.1f}")
        else:
            out.append("- No impressions in range yet.")

        def table(rows, head):
            if not rows:
                return ["", f"_No {head} yet._"]
            lines = ["", f"### Top {head}", "",
                     f"| {head} | clicks | impressions | CTR | avg pos |",
                     "|---|--:|--:|--:|--:|"]
            for r in rows:
                lines.append(f"| {r['keys'][0]} | {int(r.get('clicks', 0))} | {int(r.get('impressions', 0))} | "
                             f"{r.get('ctr', 0) * 100:.1f}% | {r.get('position', 0):.1f} |")
            return lines

        out += table(gsc.get("queries"), "queries")
        out += table(gsc.get("pages"), "pages")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Pull GSC + PSI insights for AETHON.")
    ap.add_argument("--out", default="seo-reports", help="output directory")
    ap.add_argument("--days", type=int, default=28, help="GSC look-back window")
    args = ap.parse_args()

    when = datetime.date.today().isoformat()
    gsc = pull_gsc(args.days)
    psi_mobile = pull_psi("mobile")
    psi_desktop = pull_psi("desktop")

    os.makedirs(args.out, exist_ok=True)
    report = render(gsc, psi_mobile, psi_desktop, when)
    base = os.path.join(args.out, when)
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write(report)
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump({"date": when, "gsc": gsc,
                   "psi": {"mobile": psi_mobile, "desktop": psi_desktop}}, fh, indent=2)

    print(report)
    step = os.environ.get("GITHUB_STEP_SUMMARY")
    if step:
        with open(step, "a", encoding="utf-8") as fh:
            fh.write(report)

    # Never fail the job just because data isn't flowing yet.
    return 0


if __name__ == "__main__":
    sys.exit(main())
