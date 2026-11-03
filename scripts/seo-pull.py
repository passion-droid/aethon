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
import io
import os
import sys
import json
import zipfile
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


def _gsc_rows(svc, start, end, dimensions, limit, extra=None):
    body = {"startDate": start, "endDate": end, "dimensions": dimensions,
            "rowLimit": limit, "dataState": "all"}
    if extra:
        body.update(extra)
    return svc.searchanalytics().query(siteUrl=PROPERTY, body=body).execute().get("rows", [])


def _gsc_totals(svc, start, end, extra=None):
    rows = _gsc_rows(svc, start, end, [], 1, extra)
    return rows[0] if rows else {}


def _brand_filter(op):
    return {"dimensionFilterGroups": [{"filters": [
        {"dimension": "query", "operator": op, "expression": "aethon"}]}]}


def pull_gsc(days):
    svc, err = gsc_service()
    if not svc:
        return {"available": False, "reason": err}
    end = datetime.date.today() - datetime.timedelta(days=2)   # GSC data lags ~2 days
    start = end - datetime.timedelta(days=days)
    s, e = start.isoformat(), end.isoformat()
    try:
        return {
            "available": True,
            "range": [s, e],
            "totals": _gsc_totals(svc, s, e),
            "queries": _gsc_rows(svc, s, e, ["query"], 25),
            "pages": _gsc_rows(svc, s, e, ["page"], 25),
            # brand vs discovery vs image search — the strategic split for a brand site
            "brand": _gsc_totals(svc, s, e, _brand_filter("contains")),
            "nonbrand": _gsc_totals(svc, s, e, _brand_filter("notContains")),
            "image": _gsc_totals(svc, s, e, {"type": "image"}),
            "countries": _gsc_rows(svc, s, e, ["country"], 8),
            "devices": _gsc_rows(svc, s, e, ["device"], 5),
            "daily": _gsc_rows(svc, s, e, ["date"], 40),
        }
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": f"query failed: {ex}"}


def pull_index():
    """Index status via the URL Inspection API (3 calls, quota 2000/day) + sitemap health."""
    svc, err = gsc_service()
    if not svc:
        return {"available": False, "reason": err}
    urls = [f"https://{SITE}/", f"https://{SITE}/legal/", f"https://{SITE}/gallery/"]
    out = {"available": True, "pages": [], "sitemaps": []}
    for u in urls:
        try:
            r = svc.urlInspection().index().inspect(
                body={"inspectionUrl": u, "siteUrl": PROPERTY}).execute()
            st = r.get("inspectionResult", {}).get("indexStatusResult", {})
            rr = r.get("inspectionResult", {}).get("richResultsResult") or {}
            kinds = [d.get("richResultType", "?") for d in rr.get("detectedItems", [])]
            out["pages"].append({
                "url": u,
                "verdict": st.get("verdict", "?"),
                "coverage": st.get("coverageState", "?"),
                "lastCrawl": (st.get("lastCrawlTime") or "—")[:16].replace("T", " "),
                "canonical": st.get("googleCanonical") or "—",
                "rich": f"{rr.get('verdict', '')}: {', '.join(kinds)}" if rr else "",
            })
        except Exception as ex:  # noqa: BLE001
            out["pages"].append({"url": u, "verdict": "ERROR", "coverage": str(ex)[:120],
                                 "lastCrawl": "—", "canonical": "—"})
    try:
        for m in svc.sitemaps().list(siteUrl=PROPERTY).execute().get("sitemap", []):
            web = next((c for c in m.get("contents", []) if c.get("type") == "web"), {})
            out["sitemaps"].append({
                "path": m.get("path", "?"),
                "lastDownloaded": (m.get("lastDownloaded") or "—")[:10],
                "submitted": web.get("submitted", "?"),
                "errors": m.get("errors", 0), "warnings": m.get("warnings", 0),
            })
    except Exception as ex:  # noqa: BLE001
        out["sitemaps"] = []
        out["sitemap_error"] = str(ex)[:160]
    return out


# ---------- PageSpeed Insights ----------
def pull_psi(strategy, path="/"):
    params = {"url": f"https://{SITE}{path}", "strategy": strategy,
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
        # the audit's top improvement suggestions (only real ones — >=100ms estimated savings)
        "opportunities": sorted(
            (f"{a.get('title', '?')} (~{round(a['details']['overallSavingsMs'])} ms)"
             for a in audits.values()
             if (a.get("details") or {}).get("type") == "opportunity"
             and (a["details"].get("overallSavingsMs") or 0) >= 100),
        )[:3],
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


def _spike_days(daily, interval=10, cap=3):
    """Outlier days in the visits-by-day curve — the days worth a drilldown.

    A day is a spike at >= max(2.5x the median active day, 5 retained beacons);
    needs at least 4 active days of context so a young site doesn't flag its
    whole first week. Cloudflare's figures are adaptive samples multiplied back
    (every number a multiple of the sample interval), so a floor below ~5
    retained beacons flags pure sampling noise — 20 visits was two beacons.
    Biggest first, capped to bound the follow-up queries."""
    active = [d for d in daily if d.get("visits", 0) > 0]
    if len(active) < 4:
        return []
    vals = sorted(d["visits"] for d in active)
    threshold = max(2.5 * vals[len(vals) // 2], 5 * (interval or 10))
    spikes = sorted((d for d in active if d["visits"] >= threshold),
                    key=lambda d: d["visits"], reverse=True)
    return spikes[:cap]


def pull_cloudflare_extras(days):
    """Referrers, daily visits, spike-day forensics and a 404 watch — separate
    GraphQL call so a schema hiccup here never takes the core section down."""
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account = os.environ.get("CF_ACCOUNT_TAG")
    if not token or not account:
        return {"available": False, "reason": "no CLOUDFLARE_API_TOKEN / CF_ACCOUNT_TAG set"}
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    flt = f'date_geq: "{start.isoformat()}", date_leq: "{end.isoformat()}"'
    out = {"available": True, "referrers": [], "daily": [], "spikes": [],
           "notfound": [], "errors": []}

    def gql(query):
        req = urllib.request.Request(
            CF_GRAPHQL, data=json.dumps({"query": query}).encode(),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)

    # referrers + daily curve (same RUM dataset as the core section)
    try:
        q = """query { viewer { accounts(filter: {accountTag: "%s"}) {
          refs: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 10, orderBy: [count_DESC]) {
            count dimensions { refererHost } }
          daily: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 40, orderBy: [date_ASC]) {
            count sum { visits } dimensions { date } }
        } } }""" % (account, flt, flt)
        data = gql(q)
        if data.get("errors"):
            out["errors"].append("rum: " + "; ".join(e.get("message", "") for e in data["errors"])[:150])
        else:
            acct = data["data"]["viewer"]["accounts"][0]
            out["referrers"] = [
                {"host": g["dimensions"]["refererHost"] or "(direct)", "views": g["count"]}
                for g in acct.get("refs", [])]
            out["daily"] = [
                {"date": g["dimensions"]["date"], "visits": (g.get("sum") or {}).get("visits", 0)}
                for g in acct.get("daily", [])]
    except Exception as ex:  # noqa: BLE001
        out["errors"].append(f"rum: {str(ex)[:150]}")

    # sampling resolution: every RUM figure is an adaptive sample multiplied back, so
    # the retained-beacon count (visits / interval) is the honest size of each number
    try:
        q = """query { viewer { accounts(filter: {accountTag: "%s"}) {
          s: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 1) { count avg { sampleInterval } }
        } } }""" % (account, flt)
        data = gql(q)
        if data.get("errors"):
            out["errors"].append("sampling: " + "; ".join(e.get("message", "") for e in data["errors"])[:150])
        else:
            srow = (data["data"]["viewer"]["accounts"][0].get("s") or [{}])[0]
            out["sample_interval"] = (srow.get("avg") or {}).get("sampleInterval")
    except Exception as ex:  # noqa: BLE001
        out["errors"].append(f"sampling: {str(ex)[:150]}")

    # spike forensics: for each outlier day, ask the same RUM dataset WHO it was —
    # referrer / country / path, one query per day (<= cap extra calls)
    for d in _spike_days(out["daily"], out.get("sample_interval") or 10):
        day = d["date"]
        try:
            dflt = f'date_geq: "{day}", date_leq: "{day}"'
            q = """query { viewer { accounts(filter: {accountTag: "%s"}) {
              refs: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 5, orderBy: [count_DESC]) {
                count dimensions { refererHost } }
              geo: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 5, orderBy: [count_DESC]) {
                count dimensions { countryName } }
              paths: rumPageloadEventsAdaptiveGroups(filter: {%s}, limit: 5, orderBy: [count_DESC]) {
                count dimensions { requestPath } }
            } } }""" % (account, dflt, dflt, dflt)
            data = gql(q)
            if data.get("errors"):
                out["errors"].append(f"spike {day}: " + "; ".join(
                    e.get("message", "") for e in data["errors"])[:120])
                continue
            acct = data["data"]["viewer"]["accounts"][0]
            out["spikes"].append({
                "date": day, "visits": d["visits"],
                "referrers": [{"host": g["dimensions"]["refererHost"] or "(direct)",
                               "views": g["count"]} for g in acct.get("refs", [])],
                "countries": [{"country": g["dimensions"]["countryName"], "views": g["count"]}
                              for g in acct.get("geo", [])],
                "paths": [{"path": g["dimensions"]["requestPath"], "views": g["count"]}
                          for g in acct.get("paths", [])],
            })
        except Exception as ex:  # noqa: BLE001
            out["errors"].append(f"spike {day}: {str(ex)[:150]}")

    # 404 watch on the proxied zone (needs the zone id via REST; Zone:Read covers it)
    try:
        req = urllib.request.Request(
            f"https://api.cloudflare.com/client/v4/zones?name={SITE}",
            headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            zones = json.load(resp)
        zone = (zones.get("result") or [{}])[0].get("id")
        if not zone:
            raise RuntimeError("zone not visible to token")
        # free-plan zones cap this dataset at a 1-day query span — a 24h spot-check
        # is the watchman we can have (report cadence samples it fortnightly)
        now = datetime.datetime.now(datetime.timezone.utc)
        day = (f'datetime_geq: "{(now - datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")}", '
               f'datetime_leq: "{now.strftime("%Y-%m-%dT%H:%M:%SZ")}"')
        q = """query { viewer { zones(filter: {zoneTag: "%s"}) {
          nf: httpRequestsAdaptiveGroups(
            filter: {%s, edgeResponseStatus: 404}, limit: 10, orderBy: [count_DESC]) {
            count dimensions { clientRequestPath } }
        } } }""" % (zone, day)
        data = gql(q)
        if data.get("errors"):
            out["errors"].append("404: " + "; ".join(e.get("message", "") for e in data["errors"])[:150])
        else:
            z = data["data"]["viewer"]["zones"][0]
            out["notfound"] = [
                {"path": g["dimensions"]["clientRequestPath"], "count": g["count"]}
                for g in z.get("nf", [])]
    except Exception as ex:  # noqa: BLE001
        out["errors"].append(f"404: {str(ex)[:150]}")
    return out


# ---------- Brevo — the interest list (count only, never contact data) ----------
def pull_brevo():
    """Size of the "AETHON — Interest" list. Degrades gracefully until the
    BREVO_API_KEY secret exists (create a read-suited key in Brevo -> SMTP & API)."""
    key = os.environ.get("BREVO_API_KEY")
    if not key:
        return {"available": False,
                "reason": "no BREVO_API_KEY secret set — add it and this section fills itself"}
    req = urllib.request.Request(
        "https://api.brevo.com/v3/contacts/lists?limit=50",
        headers={"api-key": key, "accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as ex:
        return {"available": False, "reason": f"HTTP {ex.code} — {ex.read().decode('utf-8', 'replace')[:150]}"}
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": str(ex)[:150]}
    lists = [{"name": l.get("name", "?"),
              "subscribers": l.get("totalSubscribers", 0),
              "blacklisted": l.get("totalBlacklisted", 0)}
             for l in data.get("lists", []) if "aethon" in l.get("name", "").lower()]
    return {"available": True, "lists": lists}


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
        window, totals, daily, unreadable = {}, {}, {}, 0
        for name in keys:
            event, _, day = name.rpartition(":")
            if not event:
                continue
            try:
                val = int(urllib.request.urlopen(urllib.request.Request(
                    f"{api}/accounts/{account}/storage/kv/namespaces/{ns_id}/values/{name}",
                    headers=hdrs), timeout=60).read() or b"0")
            except Exception:  # noqa: BLE001
                unreadable += 1   # a 429 / 5xx must never read as a zero count — it is reported
                continue
            totals[event] = totals.get(event, 0) + val
            daily.setdefault(event, {})[day] = val   # the day buckets are the TTL-proof truth
            if day >= start:
                window[event] = window.get(event, 0) + val
        return {"available": True, "days": days, "window": window, "totals": totals,
                "daily": daily, "unreadable": unreadable, "tracked_keys": len(keys)}
    except urllib.error.HTTPError as ex:
        return {"available": False, "reason": f"HTTP {ex.code} — token may lack Workers KV read"}
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": str(ex)}


# ---------- previous report (trend memory) ----------
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _download_artifact(url, hdrs):
    """GitHub artifact zips 302-redirect to signed blob URLs that reject requests
    still carrying the API Authorization header — follow the hop by hand, bare."""
    try:
        with urllib.request.build_opener(_NoRedirect).open(
                urllib.request.Request(url, headers=hdrs), timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as ex:
        if ex.code in (301, 302, 303, 307, 308) and ex.headers.get("Location"):
            with urllib.request.urlopen(ex.headers["Location"], timeout=120) as resp:
                return resp.read()
        raise


def fetch_previous_report():
    """The previous run's raw JSON, read from its workflow artifact IN MEMORY —
    the report gains a memory while the 'nothing committed' stance stays true.

    Needs GITHUB_TOKEN with actions:read (granted in the workflow); degrades
    gracefully anywhere else. The current run's artifact doesn't exist yet at
    pull time, so the newest 'seo-insights-*' artifact IS the previous report."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        return {"available": False, "reason": "no GITHUB_TOKEN / GITHUB_REPOSITORY (local run)"}
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    hdrs = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}
    try:
        req = urllib.request.Request(f"{api}/repos/{repo}/actions/artifacts?per_page=100",
                                     headers=hdrs)
        with urllib.request.urlopen(req, timeout=60) as resp:
            arts = json.load(resp).get("artifacts", [])
        cand = sorted((a for a in arts if a.get("name", "").startswith("seo-insights-")
                       and not a.get("expired")),
                      key=lambda a: a.get("created_at", ""), reverse=True)
        # every artifact is a report run — the days the site's own PageSpeed loads happened
        run_days = sorted({(a.get("created_at") or "")[:10] for a in cand if a.get("created_at")})
        if not cand:
            return {"available": False, "reason": "no previous seo-insights artifact (first run?)",
                    "run_days": run_days}
        blob = _download_artifact(cand[0]["archive_download_url"], hdrs)
        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
            name = next((n for n in zf.namelist() if n.endswith(".json")), None)
            if not name:
                return {"available": False, "reason": "previous artifact holds no JSON", "run_days": run_days}
            data = json.loads(zf.read(name))
        return {"available": True, "data": data,
                "date": data.get("date") or os.path.basename(name)[:-5], "run_days": run_days}
    except urllib.error.HTTPError as ex:
        return {"available": False, "reason": f"HTTP {ex.code} — workflow may lack actions:read"}
    except Exception as ex:  # noqa: BLE001
        return {"available": False, "reason": str(ex)[:150]}


def _dig(d, *keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def _fmt_delta(cur, prev):
    if cur is None or prev is None:
        return None
    d = int(cur) - int(prev)
    return f"+{d}" if d > 0 else (f"-{-d}" if d < 0 else "±0")


def _poisson_ci(n, conf=0.95):
    """Exact (Garwood) Poisson limits for an observed count n — pure python, for the
    handful of retained beacons behind every Cloudflare figure at this scale."""
    import math
    a = (1 - conf) / 2

    def cdf(k, lam):   # P(X <= k) — terms in log space (exp(-lam) underflows past ~745)
        if lam <= 0:
            return 1.0
        return min(1.0, sum(math.exp(-lam + i * math.log(lam) - math.lgamma(i + 1)) for i in range(k + 1)))

    def solve(pred, lo, hi):   # largest lam in [lo, hi] for which pred holds (pred monotone)
        for _ in range(60):
            mid = (lo + hi) / 2
            if pred(mid):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    lower = 0.0 if n <= 0 else solve(lambda lam: 1 - cdf(n - 1, lam) < a, 0.0, n + 1.0)
    upper = solve(lambda lam: cdf(n, lam) > a, 0.0, 3.0 * n + 20)
    return lower, upper


# the page's R4 clock, mirrored (index.html no-flash init): mid-month Paphos sunset /
# sunrise in Cyprus wall-clock hours — tells whether a load at an instant opens in Afterglow
_SUNSET = [17.2, 17.7, 18.1, 19.5, 19.9, 20.2, 20.3, 19.8, 19.1, 18.3, 16.9, 16.7]
_SUNRISE = [6.9, 6.7, 6.1, 6.3, 5.8, 5.6, 5.7, 6.1, 6.5, 6.9, 6.4, 6.8]


def _house_hour(when_utc):
    try:
        from zoneinfo import ZoneInfo
        local = when_utc.astimezone(ZoneInfo("Asia/Nicosia"))
    except Exception:  # noqa: BLE001
        return None
    h = local.hour + local.minute / 60
    night = h >= _SUNSET[local.month - 1] or h < _SUNRISE[local.month - 1]
    return {"utc": when_utc.strftime("%Y-%m-%d %H:%M"), "cyprus": local.strftime("%H:%M"), "night": night}


# ---------- report ----------
def render(gsc, index, psi_mobile, psi_desktop, psi_gallery, cf, cfx, brevo, events, prev, when,
           psi_run=None):
    out = [f"# AETHON — insights · {when}", ""]
    pd = prev.get("data") if prev.get("available") else None
    pdate = prev.get("date") if pd else None
    run_days = set(prev.get("run_days") or []) | {when}   # today's artifact does not exist yet — this run IS a run day

    out.append("## PageSpeed Insights (lab)")
    for label, psi in [("Mobile /", psi_mobile), ("Desktop /", psi_desktop),
                       ("Mobile /gallery/", psi_gallery)]:
        if psi.get("available"):
            sc = psi["scores"]
            out.append(f"- **{label}** — perf **{sc.get('performance', '?')}** · a11y {sc.get('accessibility', '?')} · "
                       f"best-practices {sc.get('best-practices', '?')} · SEO {sc.get('seo', '?')}  "
                       f"_(field: {psi['field']})_")
            m = psi["metrics"]
            out.append(f"    - LCP {m['largest-contentful-paint']} · CLS {m['cumulative-layout-shift']} · "
                       f"TBT {m['total-blocking-time']} · FCP {m['first-contentful-paint']} · SI {m['speed-index']}")
            if "gallery" in label and sc.get("seo", 100) < 100:
                out.append("    - _(SEO score reflects the deliberate noindex — intended)_")
            for o in psi.get("opportunities", []):
                out.append(f"    - suggest: {o}")
        else:
            out.append(f"- **{label}** — unavailable ({psi.get('reason', '')[:180]})")
    if psi_run:
        # the lab loads run the page's JS: in Cyprus night they open in Afterglow and the two
        # homepage loads count afterglow-auto (+2) — say which it was, so the counter can be read
        out.append(f"- _lab loads ran at {psi_run['cyprus']} Cyprus time — "
                   + ("**Afterglow: the two homepage loads may have counted afterglow-auto (+2)**_"
                      if psi_run["night"] else "Daylight; afterglow-auto unaffected_"))
    out.append("")

    out.append("## Search Console")
    if not gsc.get("available"):
        out.append(f"_Unavailable: {gsc.get('reason', '')[:200]}_")
        out.append("_(Normal right after verifying — give Google a few days of crawl + some traffic.)_")
    else:
        t = gsc.get("totals", {})
        out.append(f"Range **{gsc['range'][0]} → {gsc['range'][1]}**")
        if t:
            line = (f"- **Totals** — clicks {int(t.get('clicks', 0))} · impressions {int(t.get('impressions', 0))} · "
                    f"CTR {t.get('ctr', 0) * 100:.1f}% · avg position {t.get('position', 0):.1f}")
            pt = _dig(pd, "gsc", "totals")
            if pt is not None:
                line += (f"  _(vs {pdate}: impressions {_fmt_delta(t.get('impressions', 0), pt.get('impressions', 0))}, "
                         f"clicks {_fmt_delta(t.get('clicks', 0), pt.get('clicks', 0))})_")
            out.append(line)
            # the homepage alone is the brand proxy — site totals mix in /legal/'s imprint-string
            # matches (company name, registration number), which drag the average position
            home_url = f"https://{SITE}/"
            home = next((r for r in gsc.get("pages", []) if r["keys"][0] == home_url), None)
            if home:
                hl = (f"- **Homepage (brand proxy)** — clicks {int(home.get('clicks', 0))} · "
                      f"impressions {int(home.get('impressions', 0))} · avg position {home.get('position', 0):.1f}")
                ph = next((r for r in (_dig(pd, "gsc", "pages") or []) if r.get("keys", [None])[0] == home_url), None)
                if ph is not None:
                    hl += f"  _(vs {pdate}: impressions {_fmt_delta(home.get('impressions', 0), ph.get('impressions', 0))})_"
                elif pd is not None:
                    hl += f"  _(not listed on {pdate})_"
                out.append(hl)
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

        b, nb, im = gsc.get("brand", {}), gsc.get("nonbrand", {}), gsc.get("image", {})
        out.append(f"- **Brand vs discovery** — 'aethon' queries: {int(b.get('impressions', 0))} impressions / "
                   f"{int(b.get('clicks', 0))} clicks · other queries: {int(nb.get('impressions', 0))} / "
                   f"{int(nb.get('clicks', 0))} · **image search**: {int(im.get('impressions', 0))} impressions"
                   f"{' (baseline for the photography)' if not im.get('impressions') else ''}"
                   + ("  _(query-filtered — Google omits anonymized queries under a query filter, so 0/0 beside "
                      "real impressions means unattributable, not absent)_"
                      if int(b.get('impressions', 0)) + int(nb.get('impressions', 0)) < int(t.get('impressions', 0)) else ""))
        if gsc.get("devices"):
            out.append("- **Devices** — " + " · ".join(
                f"{r['keys'][0].lower()} {int(r.get('impressions', 0))}" for r in gsc["devices"]))
        if gsc.get("countries"):
            out.append("- **Countries** — " + " · ".join(
                f"{r['keys'][0].upper()} {int(r.get('impressions', 0))}" for r in gsc["countries"][:8]))
        active_days = [r for r in gsc.get("daily", []) if int(r.get("impressions", 0)) > 0]
        if active_days:
            out.append("- **By day** — " + " · ".join(
                f"{r['keys'][0][5:]} ×{int(r['impressions'])}" for r in active_days))

        if not gsc.get("queries") and int(t.get("impressions", 0)) > 0:
            # empty query table + real impressions = Google anonymized the rare
            # queries; "no queries yet" would misread as "no search activity"
            out += ["", "_No reportable queries — Google anonymizes rare queries at this "
                        "volume; the impressions above are real but unattributed._"]
        else:
            out += gsc_table(gsc.get("queries"), "queries")
        out += gsc_table(gsc.get("pages"), "pages")
    out.append("")

    out.append("## Index status (GSC URL Inspection)")
    if not index.get("available"):
        out.append(f"_Unavailable: {index.get('reason', '')[:200]}_")
    else:
        out += ["| page | verdict | coverage | last crawl | Google canonical |", "|---|---|---|---|---|"]
        for pg in index["pages"]:
            out.append(f"| {pg['url'].replace('https://' + SITE, '') or '/'} | {pg['verdict']} | "
                       f"{pg['coverage']} | {pg['lastCrawl']} | {pg['canonical']} |")
        if index.get("sitemaps"):
            for m in index["sitemaps"]:
                out.append(f"- sitemap `{m['path'].replace('https://' + SITE, '')}` — "
                           f"{m['submitted']} URLs submitted · last downloaded {m['lastDownloaded']} · "
                           f"{m['errors']} errors / {m['warnings']} warnings")
        elif index.get("sitemap_error"):
            out.append(f"- _sitemap status unavailable: {index['sitemap_error']}_")
        rich = [f"{p['url'].replace('https://' + SITE, '') or '/'} → {p['rich']}"
                for p in index["pages"] if p.get("rich")]
        out.append("- rich results: " + ("; ".join(rich) if rich
                   else "none detected — expected (WebSite/Residence JSON-LD are not rich-result types)"))
        out.append("- _(/gallery/ is noindex **by design** — an 'excluded by noindex' row is the intended state.)_")
    out.append("")

    out.append("## Cloudflare Web Analytics (cookieless)")
    if not cf.get("available"):
        out.append(f"_Unavailable: {cf.get('reason', '')[:200]}_")
    else:
        line = (f"Range **{cf['range'][0]} → {cf['range'][1]}** — "
                f"**{cf['visits']} visits · {cf['pageviews']} page views**")
        if _dig(pd, "cloudflare", "available"):
            line += (f"  _(vs {pdate}: visits {_fmt_delta(cf['visits'], _dig(pd, 'cloudflare', 'visits'))}, "
                     f"views {_fmt_delta(cf['pageviews'], _dig(pd, 'cloudflare', 'pageviews'))} — sampled, see the band)_")
        out.append(line)
        si = cfx.get("sample_interval") if cfx.get("available") else None
        if si and cf.get("visits") is not None:
            n = int(round(cf["visits"] / si))
            lo, hi = _poisson_ci(n)
            out.append(f"- _sampling: 1 in {si:g} — {cf['visits']} visits = ≈{n} retained beacons, a 95 % band of "
                       f"roughly {int(round(lo * si))}–{int(round(hi * si))} visits; differences inside that band are "
                       f"noise, and the groupings below are separate samples that need not sum to the total_")
        if cf.get("pages"):
            out += ["", "### Top pages", "", "| path | views | visits |", "|---|--:|--:|"]
            for p in cf["pages"]:
                out.append(f"| {p['path']} | {p['views']} | {p['visits']} |")
        if cf.get("countries"):
            out += ["", "### Top countries", "", "| country | views |", "|---|--:|"]
            for c in cf["countries"]:
                out.append(f"| {c['country']} | {c['views']} |")
    if cfx.get("available"):
        if cfx.get("referrers"):
            out += ["", "### Referrers", "", "| source | views |", "|---|--:|"]
            for r in cfx["referrers"]:
                out.append(f"| {r['host']} | {r['views']} |")
        if cfx.get("daily"):
            out.append("")
            marked = [d for d in cfx["daily"] if d["visits"] and d["date"] in run_days]
            out.append("**Visits by day** — " + " · ".join(
                f"{d['date'][5:]}:{d['visits']}" + ("▸" if d["date"] in run_days else "")
                for d in cfx["daily"] if d["visits"]))
            if marked:
                out.append("_▸ a report ran that day — its PageSpeed step loads / twice and /gallery/ once "
                           "(≤ 3 beacons; marked, never subtracted — unsubtractable at this sampling)_")
        if cfx.get("spikes"):
            out += ["", "**Spike forensics** — outlier days, and who that traffic was (views):", ""]
            for s in cfx["spikes"]:
                refs = ", ".join(f"{r['host']} {r['views']}" for r in s["referrers"][:4]) or "—"
                geo = ", ".join(f"{c['country']} {c['views']}" for c in s["countries"][:4]) or "—"
                paths = ", ".join(f"{p['path']} {p['views']}" for p in s["paths"][:4]) or "—"
                out.append(f"- **{s['date'][5:]}**{' ▸report run' if s['date'] in run_days else ''} "
                           f"({s['visits']} visits) — referrers: {refs} · countries: {geo} · paths: {paths}")
        out.append("")
        nf_err = next((e for e in cfx.get("errors", []) if e.startswith("404:")), None)
        if cfx.get("notfound"):
            out += ["**404s (proxied, last 24 h)** — check for broken links:", ""]
            for nf in cfx["notfound"]:
                out.append(f"- `{nf['path']}` × {nf['count']}")
        elif nf_err:
            out.append(f"**404s (proxied, last 24 h)** — not checked: {nf_err[5:]}")
            if "permission" in nf_err:
                out.append("  _(token needs Zone → Analytics → Read on the aethon.house zone)_")
        else:
            out.append("**404s (proxied, last 24 h)** — none. No broken links.")
        for e in cfx.get("errors", []):
            if not e.startswith("404:"):
                out.append(f"- _extras partial: {e}_")
    else:
        out.append(f"_Extras unavailable: {cfx.get('reason', '')[:150]}_")
    out.append("")

    out.append("## Interest list (Brevo)")
    if not brevo.get("available"):
        out.append(f"_Unavailable: {brevo.get('reason', '')[:200]}_")
    elif not brevo.get("lists"):
        out.append("_No list with 'AETHON' in its name found — check the list name in Brevo._")
    else:
        prev_lists = {x.get("name"): x.get("subscribers")
                      for x in (_dig(pd, "brevo", "lists") or [])}
        for l in brevo["lists"]:
            d = _fmt_delta(l["subscribers"], prev_lists.get(l["name"]))
            out.append(f"- **{l['name']}** — **{l['subscribers']}** on the list"
                       + (f" (Δ {d})" if d else "")
                       + (f" ({l['blacklisted']} unsubscribed/blocked)" if l["blacklisted"] else ""))
    out.append("")
    out.append("## On-page events (anonymous counters)")
    if not events.get("available"):
        out.append(f"_Unavailable: {events.get('reason', '')[:200]}_")
    else:
        win = events.get("window", {})
        if not win:
            out.append(f"No events in the last {events.get('days')} days yet.")
        else:
            prev_tot = _dig(pd, "events", "totals")
            daily = events.get("daily") or {}
            intro = f"Last {events.get('days')} days (lifetime in parens — `_hits`: trailing 60 d by TTL):"
            if prev_tot is not None:
                out += [intro, "", f"| event | count | new since {pdate} |", "|---|--:|--:|"]
            else:
                out += [intro, "", "| event | count |", "|---|--:|"]
            for name in sorted(win, key=win.get, reverse=True):
                tot = events["totals"].get(name, 0)
                row = f"| {name} | {win[name]} ({tot}{' · 60 d' if name == '_hits' else ''}) |"
                if prev_tot is not None:
                    if name == "_hits" and daily:
                        # 60-day TTL: a lifetime difference would be inflow minus expiry — count the
                        # day buckets instead: from the previous run's reading of its own day onward
                        # (exact), or the days after it when that reading is not stored (older JSON)
                        hd = daily.get("_hits", {})
                        base = _dig(pd, "events", "daily", "_hits", pdate) if pdate else None
                        if base is not None:
                            new = sum(v for d, v in hd.items() if d >= pdate) - int(base)
                        else:
                            new = sum(v for d, v in hd.items() if pdate and d > pdate)
                        row += f" +{new} |" if new > 0 else " ±0 |"
                    else:
                        # named events keep 400 days, so the lifetime difference IS the new
                        # count — exact until the first expiry (2027-08 for the July launch)
                        row += f" {_fmt_delta(tot, prev_tot.get(name, 0))} |"
                out.append(row)
            # _hits counts EVERY request the worker sees. Requests without an allowlisted
            # name are scanner probes (every /e* path while the pre-2026-11 worker is live;
            # bare /e or unknown names after the exact-path worker is deployed) — not
            # visitors and not DNT: an opted-out browser sends nothing at all.
            # Window-only on purpose: _hits keys expire after 60 days while named
            # events keep 400, so lifetime sums cross retention horizons and
            # don't compare (and a --days > 60 window would truncate _hits too).
            hits_win = win.get("_hits", 0)
            unattr_win = hits_win - sum(v for k, v in win.items() if k != "_hits")
            if unattr_win > 0:
                out += ["", f"_`_hits` check: {unattr_win} of {hits_win} window requests "
                            "carry no allowlisted event name — scanner probes of the endpoint, "
                            "not visitors; the named rows are the human signal._"]
            kv = f"_KV read: {events.get('tracked_keys', 0)} keys"
            if events.get("unreadable"):
                kv += f" · **{events['unreadable']} unreadable — counts above may be low**"
            out += ["", kv + "_"]
    out.append("")
    if not prev.get("available") and os.environ.get("GITHUB_ACTIONS"):
        out += [f"_Trend deltas unavailable: {prev.get('reason', '')[:150]}_", ""]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Pull GSC + PSI + Cloudflare insights for AETHON.")
    ap.add_argument("--out", default="seo-reports", help="output directory")
    ap.add_argument("--days", type=int, default=28, help="look-back window (days)")
    args = ap.parse_args()

    when = datetime.date.today().isoformat()
    gsc = pull_gsc(args.days)
    index = pull_index()
    psi_run = _house_hour(datetime.datetime.now(datetime.timezone.utc))
    psi_mobile = pull_psi("mobile")
    psi_desktop = pull_psi("desktop")
    psi_gallery = pull_psi("mobile", "/gallery/")
    cf = pull_cloudflare(args.days)
    cfx = pull_cloudflare_extras(args.days)
    brevo = pull_brevo()
    events = pull_events(args.days)
    prev = fetch_previous_report()

    os.makedirs(args.out, exist_ok=True)
    report = render(gsc, index, psi_mobile, psi_desktop, psi_gallery, cf, cfx, brevo, events, prev, when,
                    psi_run=psi_run)
    base = os.path.join(args.out, when)
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write(report)
    with open(base + ".json", "w", encoding="utf-8") as fh:
        # trend_base stays metadata-only — embedding prev["data"] would chain
        # every past report into every artifact
        json.dump({"date": when, "gsc": gsc, "index": index, "cloudflare": cf,
                   "cloudflare_extras": cfx, "brevo": brevo, "events": events,
                   "psi": {"mobile": psi_mobile, "desktop": psi_desktop,
                           "gallery_mobile": psi_gallery, "run": psi_run},
                   "trend_base": {k: prev.get(k) for k in ("available", "date", "reason", "run_days")
                                  if k in prev}}, fh, indent=2)

    print(report)
    step = os.environ.get("GITHUB_STEP_SUMMARY")
    if step:
        with open(step, "a", encoding="utf-8") as fh:
            fh.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
