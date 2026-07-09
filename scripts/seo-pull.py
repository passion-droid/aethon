#!/usr/bin/env python3
"""
AETHON — insights pull: Google Search Console + PageSpeed Insights + Cloudflare
Web Analytics (cookieless audience data).

Tooling, NOT part of the website. The site stays buildless/static; this only
reads metrics and writes reports. Runs in CI (.github/workflows/seo-insights.yml)
on a schedule, or locally.

Auth — nothing secret in the repo; all from env vars / GitHub secrets, each
optional (missing sources degrade gracefully so the workflow stays green):
  GSC_SA_KEY            service-account JSON whose client_email is a USER on the
                        Search Console domain property. Read scope.
  PSI_API_KEY           PageSpeed Insights API key (PSI also runs keyless, but the
                        shared anonymous quota is small).
  CLOUDFLARE_API_TOKEN  Cloudflare token with **Account Analytics: Read**.
  CF_ACCOUNT_TAG        Cloudflare account ID.
  CF_SITE_TAG           Web Analytics site tag (optional; account-wide if omitted).

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
import urllib.error

SITE = os.environ.get("SEO_SITE", "aethon.house")
PROPERTY = f"sc-domain:{SITE}"
PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CF_GRAPHQL = "https://api.cloudflare.com/client/v4/graphql"
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
    end = datetime.date.today() - datetime.timedelta(days=2)   # GSC data lags ~2 days
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
    except urllib.error.HTTPError as ex:
        # Surface the real reason (e.g. "API key not valid", "API not enabled")
        body = ex.read().decode("utf-8", "replace")
        msg = body
        try:
            msg = json.loads(body).get("error", {}).get("message", body)
        except Exception:  # noqa: BLE001
            pass
        return {"available": False, "reason": f"HTTP {ex.code} — {msg[:180]}"}
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


# ---------- Cloudflare Web Analytics (RUM, cookieless) ----------
def pull_cloudflare(days):
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account = os.environ.get("CF_ACCOUNT_TAG")
    if not token or not account:
        return {"available": False, "reason": "no CLOUDFLARE_API_TOKEN / CF_ACCOUNT_TAG set"}
    site = os.environ.get("CF_SITE_TAG")
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    site_filter = f', siteTag: "{site}"' if site else ""
    flt = f'date_geq: "{start.isoformat()}", date_leq: "{end.isoformat()}"{site_filter}'
    query = """query {
      viewer { accounts(filter: {accountTag: "%s"}) {
        totals: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 1) { count sum { visits } }
        pages: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 15, orderBy: [count_DESC]) {
          count sum { visits } dimensions { requestPath } }
        countries: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 10, orderBy: [count_DESC]) {
          count dimensions { countryName } }
      } }
    }""" % (account, flt, flt, flt)
    req = urllib.request.Request(
        CF_GRAPHQL, data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as ex:
        return {"available": False, "reason": f"HTTP {ex.code} — {ex.read().decode('utf-8','replace')[:180]}"}
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": str(ex)}
    if data.get("errors"):
        return {"available": False, "reason": "; ".join(e.get("message", "") for e in data["errors"])[:200]}
    try:
        acct = data["data"]["viewer"]["accounts"][0]
        tot = acct["totals"][0] if acct.get("totals") else {}
        return {
            "available": True,
            "range": [start.isoformat(), end.isoformat()],
            "pageviews": tot.get("count", 0),
            "visits": (tot.get("sum") or {}).get("visits", 0),
            "pages": [{"path": g["dimensions"]["requestPath"], "views": g["count"],
                       "visits": (g.get("sum") or {}).get("visits", 0)} for g in acct.get("pages", [])],
            "countries": [{"country": g["dimensions"]["countryName"], "views": g["count"]}
                          for g in acct.get("countries", [])],
        }
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": f"parse error: {ex}"}


# ---------- On-page events (aethon-events worker, Workers KV) ----------
def pull_events(days):
    """Anonymous per-day event counters written by the aethon-events worker.

    Reads KV keys of the form  <event>:<YYYY-MM-DD>  from the "aethon_events" namespace.
    Degrades gracefully (like every other source) until the worker/token exist.
    """
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account = os.environ.get("CF_ACCOUNT_TAG")
    if not token or not account:
        return {"available": False, "reason": "no CLOUDFLARE_API_TOKEN / CF_ACCOUNT_TAG set"}
    api = "https://api.cloudflare.com/client/v4"
    hdrs = {"Authorization": f"Bearer {token}"}

    def get(url):
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)

    try:
        ns = get(f"{api}/accounts/{account}/storage/kv/namespaces?per_page=100")
        ns_id = next((n["id"] for n in ns.get("result", []) if n.get("title") == "aethon_events"), None)
        if not ns_id:
            return {"available": False, "reason": "KV namespace 'aethon_events' not found — worker not deployed yet?"}
        keys, cursor = [], ""
        while True:
            page = get(f"{api}/accounts/{account}/storage/kv/namespaces/{ns_id}/keys?limit=1000"
                       + (f"&cursor={cursor}" if cursor else ""))
            keys += [k["name"] for k in page.get("result", [])]
            cursor = (page.get("result_info") or {}).get("cursor") or ""
            if not cursor:
                break
        start = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        window, totals = {}, {}
        for name in keys:
            event, _, day = name.rpartition(":")
            if not event:
                continue
            try:
                val = int(urllib.request.urlopen(urllib.request.Request(
                    f"{api}/accounts/{account}/storage/kv/namespaces/{ns_id}/values/{name}",
                    headers=hdrs), timeout=60).read() or b"0")
            except Exception:  # noqa: BLE001
                continue
            totals[event] = totals.get(event, 0) + val
            if day >= start:
                window[event] = window.get(event, 0) + val
        return {"available": True, "days": days, "window": window, "totals": totals,
                "tracked_keys": len(keys)}
    except urllib.error.HTTPError as ex:
        return {"available": False, "reason": f"HTTP {ex.code} — token may lack Workers KV read"}
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": str(ex)}


# ---------- report ----------
def render(gsc, psi_mobile, psi_desktop, cf, events, when):
    out = [f"# AETHON — insights · {when}", ""]

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
            out.append(f"- **{label}** — unavailable ({psi.get('reason', '')[:180]})")
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

        def gsc_table(rows, head):
            if not rows:
                return ["", f"_No {head} yet._"]
            lines = ["", f"### Top {head}", "",
                     f"| {head} | clicks | impressions | CTR | avg pos |", "|---|--:|--:|--:|--:|"]
            for r in rows:
                lines.append(f"| {r['keys'][0]} | {int(r.get('clicks', 0))} | {int(r.get('impressions', 0))} | "
                             f"{r.get('ctr', 0) * 100:.1f}% | {r.get('position', 0):.1f} |")
            return lines

        out += gsc_table(gsc.get("queries"), "queries")
        out += gsc_table(gsc.get("pages"), "pages")
    out.append("")

    out.append("## Cloudflare Web Analytics (cookieless)")
    if not cf.get("available"):
        out.append(f"_Unavailable: {cf.get('reason', '')[:200]}_")
    else:
        out.append(f"Range **{cf['range'][0]} → {cf['range'][1]}** — "
                   f"**{cf['visits']} visits · {cf['pageviews']} page views**")
        if cf.get("pages"):
            out += ["", "### Top pages", "", "| path | views | visits |", "|---|--:|--:|"]
            for p in cf["pages"]:
                out.append(f"| {p['path']} | {p['views']} | {p['visits']} |")
        if cf.get("countries"):
            out += ["", "### Top countries", "", "| country | views |", "|---|--:|"]
            for c in cf["countries"]:
                out.append(f"| {c['country']} | {c['views']} |")
    out.append("")
    out.append("## On-page events (anonymous counters)")
    if not events.get("available"):
        out.append(f"_Unavailable: {events.get('reason', '')[:200]}_")
    else:
        win = events.get("window", {})
        if not win:
            out.append(f"No events in the last {events.get('days')} days yet.")
        else:
            out += [f"Last {events.get('days')} days (all-time in parens):", "",
                    "| event | count |", "|---|--:|"]
            for name in sorted(win, key=win.get, reverse=True):
                out.append(f"| {name} | {win[name]} ({events['totals'].get(name, 0)}) |")
    out.append("")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Pull GSC + PSI + Cloudflare insights for AETHON.")
    ap.add_argument("--out", default="seo-reports", help="output directory")
    ap.add_argument("--days", type=int, default=28, help="look-back window (days)")
    args = ap.parse_args()

    when = datetime.date.today().isoformat()
    gsc = pull_gsc(args.days)
    psi_mobile = pull_psi("mobile")
    psi_desktop = pull_psi("desktop")
    cf = pull_cloudflare(args.days)
    events = pull_events(args.days)

    os.makedirs(args.out, exist_ok=True)
    report = render(gsc, psi_mobile, psi_desktop, cf, events, when)
    base = os.path.join(args.out, when)
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write(report)
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump({"date": when, "gsc": gsc, "cloudflare": cf, "events": events,
                   "psi": {"mobile": psi_mobile, "desktop": psi_desktop}}, fh, indent=2)

    print(report)
    step = os.environ.get("GITHUB_STEP_SUMMARY")
    if step:
        with open(step, "a", encoding="utf-8") as fh:
            fh.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
