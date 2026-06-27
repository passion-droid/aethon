# SEO, search & analytics — AETHON House

Reference for how this site is found, how the link looks when shared, and how we
measure it — **without** turning a museal private-residence brand into an
estate-agent listing. Companion to the `## SEO / meta` notes in `CLAUDE.md`.

---

## 1 · Positioning (from a live SERP analysis, June 2026)

There are **two completely different search arenas**, and AETHON must stand in
the right one.

**Arena A — estate / portal SERP (do NOT compete).** For *luxury villa Paphos,
seafront villa Cyprus, Tombs of the Kings villa, Faros villa for sale*, page one
is wall-to-wall portals and agencies — JamesEdition, Rightmove, Zoopla,
LuxuryEstate, Cyprus Sotheby's, Leptos, and local agents (bluesky-houses,
winwinestates, pafosproperties). High authority, thousands of listings,
transactional intent. A one-page brand site **cannot** rank here, and trying
would force AETHON into a "compare the €/m²" frame that contradicts the brand.

**Arena B — design / architecture SERP (this is ours).** For *architect-designed
villa Paphos, minimalist villa Cyprus, Japandi*, the SERP is editorial and
design-led — Architizer, architectural magazines (e.g. ek-mag's "Villa 242,
Paphos"), Cyprus Edit, design studios. **No estate portals dominate.** A
design-led single residence with a named creative team belongs here, and can
earn placement on *merit*, not ad spend. This is the winnable, on-brand niche.

### Three findings that shape strategy
1. **Brand-name collisions in-locale.** "AETHON Paphos" currently surfaces
   **Almyra Hotel's "Aethon Premium Sea View" rooms** (a 5-star Paphos hotel —
   same city, same "Aethon", same sea-view register) and the ancient **"House of
   Aion"** (a major Paphos mosaic site; near-homophone). Winnable, but it needs
   GSC + time + a couple of authoritative backlinks. **Mitigation:** always use
   the **"AETHON House"** two-word lockup (matches the `.house` domain) in
   titles/links — done in the `<title>`.
2. **A near-namesake developer exists** — "Faros Sea Residence"
   (farossearesidence.com). Keep *Faros* as locale colour only; lead with
   **AETHON**, never build the positioning on "Faros residence".
3. **The credited team is the backlink goldmine.** The colophon names
   Vardastudio, House Talks Interiors, Antoine Garden Design, DARK Lighting and
   **Dear Modern / Cliff Tan** (Feng Shui — large international following). A
   single project page or editorial feature on **their** sites linking back to
   `aethon.house` is the **highest-leverage off-page action** — more than any tag.

### One-line positioning
> Not "a seafront villa for sale in Paphos," but **"an architecturally
> significant private seafront residence on the western coast of Paphos"** —
> discovered through design and architecture, not estate listings.

### Keyword tiers
- **Tier 1 — brand (own these):** AETHON, AETHON House, AETHON Paphos, AETHON
  house of light.
- **Tier 2 — on-brand long-tail (winnable):** seafront residence Paphos · private
  house Faros beach Paphos · architect-designed seafront house western Paphos ·
  sea-view residence Tombs of the Kings · Kato Paphos seafront house.
- **Tier 3 — head terms (carry the vocabulary in meta so we're *eligible*; don't
  expect ranking):** luxury / beachfront / seafront / first-line villa Paphos
  Cyprus. Note: avoid the word **"luxury"** in visible copy — it's the
  estate-agent superlative the brand guardrails reject; "private / seafront /
  architectural" reads more premium and stays on-voice.

Strategy in one sentence: **own brand + on-brand long-tail via the meta layer and
design-press backlinks; never chase portal-owned head terms.**

---

## 2 · Google Search Console + sitemap (one-time, owner)

Sitemap URL to submit: **`https://aethon.house/sitemap.xml`**

1. [search.google.com/search-console](https://search.google.com/search-console) →
   add a **Domain** property `aethon.house` → verify via DNS TXT. **(Done.)**
2. **Sitemaps** → submit `sitemap.xml`. **(Done — two URLs discovered: `/` and
   `/legal/`; `/gallery/` is `noindex` by design.)**
3. **URL Inspection** → request indexing for `/` and `/legal/`.
4. Watch **Pages** (indexed), **Performance** (queries/clicks/position), **Core
   Web Vitals**. Search data needs a few days of crawl + traffic to appear.
5. Optional: add **Bing Webmaster Tools** (imports from GSC; feeds Copilot/ChatGPT
   search).

---

## 3 · Analytics — cookieless, no consent banner

**Google Analytics (GA4) is the wrong fit here.** GA4 sends personal data (full
IP, client IDs) to Google and sets cookies → in Cyprus/EU that requires a
**consent banner**, and it **re-introduces exactly the "visitor IP to Google"
transfer we removed by self-hosting the fonts**. Avoid GA.

**Chosen approach: Google Search Console (search side) + Cloudflare (audience
side)** — cookieless, no banner, no new third party.

| Option | Cookies | Banner | Notes |
|---|---|---|---|
| **Cloudflare dashboard analytics** | none | none | If DNS is proxied through Cloudflare (the live site's bot-protection/403 suggests it is), traffic stats already exist **with zero on-page code**. Cleanest. |
| **Cloudflare Web Analytics** (beacon) | none | none | Free RUM; per-page visits. On a proxied zone Cloudflare **auto-injects** the beacon — still no code from us. Off-zone, it's one `<script>` tag. |
| Self-hosted Umami / Plausible / GoatCounter | none | none | Purest: data only to our own server. ~1 KB script. More to run. |
| GSC | none | none | Search queries/clicks/position with no on-site code at all. |

### Setup (owner — pick the path that matches your DNS)
- **If `aethon.house` is proxied through Cloudflare (orange-cloud):**
  Cloudflare dashboard → **Analytics & Logs → Web Analytics** → enable for the
  site. On a proxied zone the beacon is **auto-injected** — **nothing to add to
  the site.** Done.
- **If NOT proxied (e.g. DNS points straight at GitHub Pages):**
  Cloudflare dashboard → **Web Analytics → Add a site** → copy the beacon token,
  then either paste this one line before `</body>` on each page, or send the
  token and it gets wired in:
  ```html
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js"
          data-cf-beacon='{"token": "YOUR_TOKEN"}'></script>
  ```
  (Cookieless, ~no consent obligation; one request to `cloudflareinsights.com`.)

For on-page event detail later, the on-brand step up is **self-hosted Umami**.

---

## 4 · Automated insights (GSC + PageSpeed) — `scripts/seo-pull.py`

A fortnightly GitHub Action pulls Search Console + PageSpeed Insights and writes
a dated report. Tooling only — the website stays buildless/static.

- Script: `scripts/seo-pull.py` (stdlib for PSI; `google-api-python-client` +
  `google-auth` for GSC, in `scripts/requirements.txt`).
- Workflow: `.github/workflows/seo-insights.yml` — runs on the **1st & 15th** of
  each month (≈ every two weeks) and via **Run workflow** (manual). Output is a
  **workflow artifact** + the **run summary** (safe whether the repo is public or
  private — nothing is committed).

### One-time setup (owner)
1. **Google Cloud:** create/pick a project → enable the **"Google Search Console
   API"** → create a **service account** → create a **JSON key** and download it.
2. **Grant the service account read access to the data:** GSC → **Settings →
   Users and permissions → Add user** → paste the service account's
   `client_email` → role **Restricted** (read is enough).
3. **(Optional) PageSpeed key:** Google Cloud → enable **"PageSpeed Insights
   API"** → create an **API key**. Without it PSI still runs but shares a small
   anonymous quota that's often exhausted.
4. **GitHub secrets:** repo → **Settings → Secrets and variables → Actions → New
   repository secret**:
   - `GSC_SA_KEY` — paste the **entire** service-account JSON.
   - `PSI_API_KEY` — the PageSpeed key (optional).
   The Action reads these from the environment; they never touch the repo.
5. Trigger a first run (Actions → **SEO insights → Run workflow**) → download the
   artifact / read the run summary.

Before the secrets exist the workflow still runs green and reports "unavailable —
pending setup". Real-user (CrUX) field data stays "insufficient" until the site
has traffic; until then PSI shows lab scores (expected to be strong — single
static file, preloaded self-hosted fonts, no framework, CLS handled).

### Switching to committed reports (only if this repo is private)
If you'd rather keep dated reports **in the repo** (easier to diff trends across
runs) and the repo is **private**, change the workflow's `permissions` to
`contents: write` and replace the upload step with a commit of `seo-reports/`
(add `[skip ci]` to the message). **Do not do this on a public repo** — it would
publish your search-query data.

### Pulling data outside CI
`scripts/seo-pull.py` runs locally too:
```bash
pip install -r scripts/requirements.txt
export GSC_SA_KEY="$(cat service-account.json)"   # and optionally PSI_API_KEY
python scripts/seo-pull.py --out seo-reports --days 28
```

---

## 5 · Current meta state (shipped)
`<title>` "AETHON House — private seafront residence in Paphos, Cyprus" ·
`og:title` kept poetic ("house of light") · meta/OG description lead with
*seafront residence · Paphos, Cyprus · Faros beach* · Twitter `summary_large_image`
card · region-level geo (`CY-05`, no coordinates) · `lang="en-GB"` · `WebSite`
JSON-LD. **`og:image` / `twitter:image` are pre-wired but asset-blocked** — drop a
1200×630 warm/afterglow master at `/images/og.jpg` and uncomment. Gallery is
`noindex`; legal is indexable.
