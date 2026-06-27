#!/usr/bin/env python3
"""
One-off Cloudflare diagnostic (tooling, not part of the site). Uses
CLOUDFLARE_API_TOKEN + CF_ACCOUNT_TAG to report:
  - whether the token is valid,
  - the aethon.house zone status + nameservers (assigned vs. seen at registrar),
  - its DNS records,
to debug the GitHub Pages / NXDOMAIN migration.

Prints only non-secret, publicly-queryable data (nameservers, DNS records) —
never the token or account id. Stdlib only. Re-runnable as a migration monitor.
"""
import os
import json
import urllib.request
import urllib.error

API = "https://api.cloudflare.com/client/v4"
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ACCOUNT = os.environ.get("CF_ACCOUNT_TAG")
ZONE = os.environ.get("SEO_SITE", "aethon.house")


def call(path):
    req = urllib.request.Request(API + path, headers={"Authorization": f"Bearer {TOKEN}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        try:
            body = json.load(e)
        except Exception:  # noqa: BLE001
            body = {"errors": [{"message": e.read().decode("utf-8", "replace")[:200]}]}
        return body, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def errstr(d, err):
    msgs = "; ".join(f"{x.get('code', '')}:{x.get('message', '')}" for x in (d or {}).get("errors", []))
    return msgs or err or "unknown error"


def main():
    out = [f"# Cloudflare diagnostic — {ZONE}", ""]
    if not TOKEN:
        out.append("`CLOUDFLARE_API_TOKEN` is not set.")
        emit(out)
        return

    d, err = call("/user/tokens/verify")
    ok = bool(d and d.get("success"))
    out.append(f"**Token:** {'valid ✓' if ok else 'INVALID — ' + errstr(d, err)}")

    zid = None
    q = f"/zones?name={ZONE}" + (f"&account.id={ACCOUNT}" if ACCOUNT else "")
    d, err = call(q)
    if d and d.get("success") and d.get("result"):
        z = d["result"][0]
        zid = z["id"]
        out.append(f"**Zone status:** `{z.get('status')}`  (paused={z.get('paused')})")
        out.append(f"**Cloudflare nameservers (assigned):** {', '.join(z.get('name_servers') or ['—'])}")
        out.append(f"**Nameservers seen at the registrar:** {', '.join(z.get('original_name_servers') or ['—'])}")
    else:
        out.append(f"**Zone lookup failed:** {errstr(d, err)}")
        out.append("_(If this is a permissions error, the token needs **Zone → Zone → Read**.)_")

    if zid:
        d, err = call(f"/zones/{zid}/dns_records?per_page=100")
        if d and d.get("success"):
            recs = d.get("result", [])
            if recs:
                out += ["", "**DNS records:**", "", "| type | name | content | proxy |", "|---|---|---|---|"]
                for r in sorted(recs, key=lambda r: (r["type"], r["name"])):
                    out.append(f"| {r['type']} | {r['name']} | {r['content']} | "
                               f"{'orange' if r.get('proxied') else 'grey'} |")
            else:
                out.append("**DNS records:** none found (empty zone — this would explain NXDOMAIN).")
        else:
            out.append(f"**DNS records lookup failed:** {errstr(d, err)}")
            out.append("_(If this is a permissions error, the token needs **Zone → DNS → Read**.)_")

    emit(out)


def emit(lines):
    report = "\n".join(lines) + "\n"
    print(report)
    step = os.environ.get("GITHUB_STEP_SUMMARY")
    if step:
        with open(step, "a", encoding="utf-8") as fh:
            fh.write(report)


if __name__ == "__main__":
    main()
