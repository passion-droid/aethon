# CLAUDE.md — AETHON

Persistent context for this repository. Read at the start of every session.

## What this is
The public showcase website for **AETHON House · Paphos** — a single private
residence on the western coast of Paphos, Cyprus. AETHON is a *quiet elevation* of an
existing seafront residence (originally part of the "Faros Beach Houses"): the
original architect's geometry is kept and honoured, the material and spatial language
refined. It is an evergreen brand presence, **not** a rental or an estate-agent
listing. Its quiet purpose is to hold a small, private interest list for a possible
future sale. The site may be reached via a QR code at the property, so the first
impression and the mobile layout matter.

"Faros" is the locale (Faros / Lighthouse Beach), not the brand — the brand is **AETHON**.

## The house, in brief
- A renovation / elevation, not a new build — honour the original geometry.
- Spatial logic: the ground level opens to gather (living, dining, pool, garden, sea); the
  upper levels withdraw for rest and retreat.
- Garden and terrace are central — they frame the western horizon where the sun meets
  the sea each evening.
- **Confirmed facts (now public on the site):** built **2018**, renewed / **completed 2026**;
  began as one of the **Faros Beach Houses** (origin folded into *The architecture*, not a
  separate section). Operating company is in *Legal* (SIGNGUARD APP LTD).
- **Signature spatial move — the threshold dissolves:** the ground floor's glazed walls slide
  back so the living and entertaining rooms, the **~10 m pool** (laid against the house, with a
  shallow sun-shelf) and the garden read as *one space*; a **planted internal courtyard** brings
  the garden inside too. The old ground-floor bedroom is now a **relax / entertainment "room kept
  for the evening"** — so the ground is all *gather*, the bedrooms *withdraw* above. (Pool stated
  as "some ten metres", never a precise dimension.)
- Philosophy: Bauhaus discipline · Japandi emptiness · Feng Shui balance ·
  Mediterranean warmth. Less, but better. (Public copy names only Japandi, Mediterranean
  and Feng Shui; **Bauhaus stays an *unstated* influence** — carried by “Reduction, not
  decoration” and “proportion rather than ornament”, never name-dropped on the site.)

## How the site is built
- The whole site is one self-contained file: **`index.html`** — HTML, CSS (in a
  `<style>` block), and a little JavaScript (in a `<script>` block).
- **No build step, no framework, no dependencies, no package manager. Do not
  introduce any.** Do not split the CSS or JS into separate files unless explicitly asked.
- Fonts are **self-hosted** (Jost + Spectral, SIL OFL) — 4 woff2 in `/fonts/` (**latin subset
  only**; the copy is basic-Latin — add latin-ext only if accented text appears) + `@font-face`
  in each page's `<style>`; **no third-party CDN** (GDPR: no visitor IP to Google). Local too.
  **Jost is a variable font** (`jost-lt.woff2`, wght 100–900) served via one `@font-face
  { font-weight: 100 900 }` — it covers 300/400/500 in a single download; don't re-split it
  into per-weight files (they'd be identical and fetched 3×). Spectral is 3 static faces.
- **Mobile is the primary (QR) audience — mobile-first.** Fluid `clamp()` type, `100svh` hero,
  ~44px touch targets, 16px inputs (no iOS zoom), single-column stacking. Desktop shows the
  inline nav links; **below 640px they are replaced by a quiet full-screen overlay menu**
  (`#menu` + `#menu-btn` → "Menu"/"Close"; Esc to close, scroll-lock, background set `inert`,
  closes on link tap). The hero is a **still on mobile** (ambient motion/video reserved for
  larger/wifi); the hero light-drift is disabled < 640px. When paired photos land, limit the
  `.shot-pair` day↔afterglow swap to the hero on mobile (cellular data).

## Deploying a change
- Hosted free on **GitHub Pages**, served from the **`main`** branch, root folder.
- A change goes live ~1–2 minutes after it is committed and pushed to `main`.
  So the loop is: edit `index.html` → commit with a short message → push to `main`.
- The live site **403s automated fetches** (bot protection) — to confirm what's live, compare the
  repo to `origin/main` (they're identical once merged) rather than fetching `aethon.house`.

## Brand guardrails — always keep
- **Name system:** the brand is `AETHON` (used alone for premium/physical use); the
  descriptor line is `AETHON House · Paphos`. Pronounced “AY-thon”.
- **Tagline:** “house of light”. **Hero line:** “A sanctuary built around sunsets,
  silence, and the western sea.” Do not rewrite these unless asked.
- **Hero orienting subline** (kept, under the hero line): “A private seafront residence on the
  western coast of Paphos.” — classifies the site for a QR visitor in seconds. The renovation is
  stated plainly just below (*The architecture* + the *In brief* colophon), so resist external
  nudges to cram “renovation” into the hero unless asked. There is **no “Faros Mansion”** name —
  reviewers keep proposing it; AETHON-only stands.
- **The sunset — not the lighthouse — is the hero.** The coast faces west; the
  evening is the house's moment. A *single, subtle* origins nod to the lighthouse
  locale (the "faros") is allowed — no lighthouse imagery or cliché beyond that.
- **Never include:** the exact address, technical blueprints, estate-agent
  superlatives, “investment opportunity” language, or any hint about the owners
  being away.
- **Floor plans:** allowed *only* as conceptual, professionally redrawn views
  (atmospheric, low-detail) — never technical or dimensioned drawings.
- **One accent colour only — green:** the accent is a single colour, green, carried in two weights — olive-green leather (primary; BoConcept Nordic Grain Olive Green) and a softer **rosemary-green fabric** (in curtains and some furniture). Everything else is stone; the **UI accent (links, buttons) stays the olive**. Never a blue accent.
- **Comfort, never gadgetry:** the smart-home (KNX), climate/cooling, outdoor misting, hearth and spa are expressed *only* abstractly, through mood and feeling (e.g. comfort "felt rather than managed"; "warmth takes its place" in the evening). Never list features, brands, specs or amenities; no security/CCTV mention at all.
- **Solar, kept poetic:** the PV/solar appears (if at all) only as the house living on the light it is named for — sustained by the western sun, quietly self-sufficient. Never panels, system sizes, savings, payback or eco-claims; no roof-panel imagery.
- **Feng Shui is foundational:** Feng Shui shaped the plan from the outset — a design basis, not the only one. Express it as principle, not primacy (copy reads “shaped from the outset by Feng Shui”, never “ordered before anything else” / “above architecture”).

## Palette — use these exact values
Derived from the house's real materials:
- Marble `#E9E7E0` (primary ground) · lighter tint `#F0EEE8`
- Travertine `#DCCDB3`
- Coastal sandstone `#C7B08C`
- Corian “Rosemary” greige `#8C8478` (muted text)
- Dark oak `#2C2620` (ink / body text)
- Olive-green leather `#565B3B` (primary green accent — BoConcept "Nordic Grain" Olive Green; night tone `#9CA279`)
- Rosemary-green fabric `#7C8569` (secondary green — softer, in curtains/furniture; **indicative, confirm vs the real cloth**)

Do **not** introduce other accent colours (e.g. ocean blue, from an earlier draft).
The sea is evoked through light and stone — never a blue accent.

Added finishes (from the interior plans; chip tones are indicative, not exact):
- Venetian plaster / Stucco Veneziano ~ `#D9CFBE` (warm hand-troweled wall texture)
- Corian "Witch Hazel" ~ `#E8DDC9` (pale, lit shelving)
- Iroko solid wood ~ `#9C6A3E` (warm hardwood)

Outdoor shading (sails / awnings) is warm sand / oyster-white (Arizona / RAL 1013) — keep
any shade imagery or copy in that warm-neutral register, never stark white.

## Copy voice
Calm, museal, understated. Short sentences, sentence case, no exclamation marks, no
superlatives, no marketing tone. Tone references: Aman, Tadao Ando. A little human warmth
is allowed (the V&A / Six Senses corrective) — restraint, not coldness.

## Known TODOs
- **Images:** an `images/` folder + a **buildless optimisation pipeline** now exist — see
  `images/README.md` (AVIF→WebP→JPEG via `<picture>`, 400/800w, uniform 3:2, sRGB,
  metadata stripped; Pillow runs it in-session). **Materials done:** the 8 macro swatches
  are wired (48 assets in `images/materials/`, brand colour kept as a load-time tint).
  Still placeholders, awaiting real images via the same pipeline: the hero ambient loop,
  the establishing-film plate in *The place*, companion images under *The architecture* /
  *The garden* / *The interior*, and the eight-slot *Views* gallery (in-code shot brief). Scales to ~20–30 photographs; once they land,
  consolidate woven vs. gallery to avoid duplication. **The full brief is `docs/imagery-brief.md`**
  (project background + tiered shot list). Key viewpoints must be shot as **matched Daylight +
  warm-evening pairs (same locked-off viewpoint)** for the `.shot-pair` crossfade — warm afterglow,
  **never blue**; strip GPS/EXIF; deliver masters (the pipeline makes the web assets).
- **Floor plans: done.** The *Plan* section (after *The architecture*) shows the two floor
  renders, **muted into the stone/olive palette** (global desaturation + the pool's blue
  specifically collapsed to pale water, per the no-blue guardrail), processed into
  `images/plan/` (AVIF/WebP/JPEG, 800/1600w, full √2 ratio, no crop). **Re-shot from new 4K
  masters and now transparent** (AVIF/WebP keep alpha; the JPEG fallback is flattened on
  `--bg-soft`) so the plan sits on the page and **adapts to Daylight/Afterglow** — it floats on
  the warm dark stone at night. The exact muting recipe is reproducible in
  `scripts/process-plan.py` (run it on the raw masters; the asset filenames/dims are unchanged,
  so `index.html` needs no edit). Keep them muted + transparent — don't reinstate the saturated
  or background-baked render. Raw HD originals shouldn't stay in the repo (see `images/README.md`).
- **Credits:** **done.** The colophon credits the full team with linked company sites
  (olive, underlined, new tab) — Original architecture: Vardastudio (Andreas Vardas);
  Renovation: G. Patsalides Construction & Renovation (Georgios Patsalides); Interior:
  House Talks Interiors (Vicky Savva); Landscape: Antoine Garden Design & Construction
  (Antoine Hadjialexandrou); Lighting: DARK Architectural Lighting; Feng Shui: Dear
  Modern (Cliff Tan).
- **Interest form:** wired to **Brevo** — the live subscription-form serve URL is in
  `index.html` (`…sibforms.com/serve/MUIF…`, the AETHON form); native POST, no API key
  exposed. Submissions go to a dedicated **"AETHON — Interest"** list with a hidden
  `SOURCE=aethon.house` tag, kept separate from the owner's *other* Brevo site; visible
  fields map to attributes `FIRSTNAME` / `EMAIL` / `MESSAGE`, honeypot `email_address_check`.
  Note Brevo's contact DB is global (unique by email) — separate AETHON interest by **list
  membership + SOURCE**, not separate databases. Optional polish: AJAX submit to stay
  on-page, and a Brevo custom redirect back to the site.
- **Domain:** `aethon.house` is connected (a `CNAME` file is on `main`); the site uses it
  as the canonical / Open Graph URL.
- **Icons / brand mark: open.** No `favicon`, `apple-touch-icon` or `web-manifest` ship yet —
  **awaiting the designer's brand-mark assets** (delivering soon). When they land, add a small
  favicon set + `apple-touch-icon` + a minimal manifest (self-hosted, no CDN), and wire the
  mark into the header if wanted. The header wordmark already has a 44px tap target reserved.
- **`og:image` / `twitter:image`: open (todo).** Still **no social-share image** — **awaiting
  photography** (needs a 1200×630 master, warm/afterglow register, never blue; run through the
  image pipeline). Both tags are **pre-wired as comments** in `index.html` (with `og:image:alt`
  + `og:image:width/height`): drop the photo at `/images/og.jpg` and uncomment to activate. Until
  then shared links show text only (no image) — this is the one preview gap that's asset-blocked.
- **SEO / meta pass — done (PR #39).** Balanced lean (owner-approved): the `<title>` and meta/OG
  descriptions now carry the searchable terms ("private seafront residence · Paphos, Cyprus ·
  Faros beach") while `og:title` stays the poetic "house of light"; added a `twitter:card`
  (`summary_large_image`, text now, image-ready), region-level geo tags (`geo.region=CY-05`,
  `geo.placename=Paphos, Cyprus` — no coordinates, per the no-address rule), `lang="en-GB"`, and
  synced the `WebSite` JSON-LD. **Strategy (don't undo):** this is a one-page brand site — it can
  own the **brand** terms (AETHON / AETHON House / AETHON Paphos) and **on-brand long-tail**
  (seafront residence / Faros beach / Kato Paphos / Tombs of the Kings), but **cannot and should
  not chase head terms** ("luxury villa Paphos" etc.) — portals (JamesEdition, Rightmove, Sotheby's,
  Leptos) own those, and "luxury"/"for sale"/"investment" wording is off-brand. Keep the visible
  page museal; let the **meta layer** carry the keywords.
- **SERP analysis + positioning — done (PR #40); full write-up in `docs/seo-and-search.md`.**
  Live-SERP research found **two arenas**: the estate/portal SERP (luxury/seafront villa Paphos —
  owned by JamesEdition/Rightmove/Zoopla/Sotheby's; **don't compete**, off-brand + unwinnable) and
  the **design/architecture SERP** (architect-designed/minimalist/Japandi villa — editorial, *not*
  portal-locked: **this is the winnable, on-brand niche**). Position AETHON as *an architecturally
  significant private seafront residence*, discovered via design — not a listing. **Brand collisions
  to know:** "Aethon" also = **Almyra Hotel's "Aethon" sea-view rooms** (same city) + the **"House of
  Aion"** mosaic site → always use the **"AETHON House"** lockup; the `<title>` now leads with it
  (PR #40, supersedes #39's "AETHON —" title) to disambiguate + match the `.house` domain. Highest-
  leverage off-page win: a backlink from the **credited team** (Vardastudio, House Talks, Dear Modern
  / Cliff Tan). **GSC + sitemap: done by owner** (domain verified, `sitemap.xml` submitted, `/` +
  `/legal/` discovered).
- **SEO measurement — automated (PR #40).** `scripts/seo-pull.py` + `.github/workflows/seo-insights.yml`
  pull **Search Console + PageSpeed Insights** on the **1st & 15th** (≈ fortnightly) and on demand,
  emitting a dated report as a **workflow artifact + run summary** (nothing committed — safe for any
  repo visibility). Auth via GitHub secrets **`GSC_SA_KEY`** (service-account JSON added as a GSC
  user) + optional **`PSI_API_KEY`**; degrades gracefully before they're set. This is **tooling, not
  part of the site** (the page stays buildless). Setup steps in `docs/seo-and-search.md`.
- **Analytics — decided: cookieless, no banner (no Google Analytics).** GA4 = personal data to Google
  + cookies → EU consent banner, and re-introduces the visitor-IP-to-Google transfer the self-hosted
  fonts removed. Chosen: **GSC (search) + Cloudflare** (dashboard if the domain is proxied — zero code;
  else the cookieless Web Analytics beacon). Self-hosted **Umami** is the on-brand step up for on-page
  events. Owner action + the one-line beacon snippet are in `docs/seo-and-search.md`. **Never add GA
  or any cookie-setting analytics without revisiting the consent/no-banner stance.**
- **Deep audit — done (PR #34).** Code-only hardening across all three pages: `theme-color`
  follows the Daylight/Afterglow toggle; mobile overlay menu got a focus trap + iOS-safe
  `position:fixed` scroll-lock (wordmark set `inert` too); `<noscript>` `.reveal` fallback;
  `overflow-x: clip`; `section{ scroll-margin-top }`; 44px wordmark tap target; `<360px` header
  tracking. **Optional polish — done (PR #38):** metric-matched fallback `@font-face`s
  (`size-adjust` + ascent/descent overrides computed from the woff2 via fontTools, tuned to
  Arial/Times; Liberation faces cover Linux; `local()` only, no extra fetch) trim font-swap
  CLS — added as the first fallback in the `--ff-display`/`--ff-text` stacks across
  index/gallery/legal (404 left minimal). And `.reveal`'s hidden state is now gated behind a
  `.js` class (added to `<html>` by the no-flash init script) so non-JS *and* broken/slow-JS
  render visible — this **superseded** the `<noscript>` `.reveal` fallback above, now removed.
- **Voice edits — owner-reviewed (PR #36).** Two of the held copy refinements shipped after
  sign-off: the dense *The place* locator sentence was split in two and the doubled
  "lighthouse coast" dropped (the *faros* idea is developed one paragraph later); the gallery's
  *western evening* + *withdraw* captions were rewritten so they no longer reuse index 669
  verbatim. **Left as-is by choice (don't re-raise unprompted):** the warmth/warm echo in *The
  interior* (~669), the "built, not furnished" button (~601), Register's "no newsletters, no
  marketing" line (~831), and the "In brief" / "The house, plainly." colophon pairing (~878–879).
  **Never auto-apply voice changes — always present for sign-off first.**

## Decided / planned
- **Floor plans:** a conceptual *Plan* section after *The architecture* — atmospheric,
  low-detail only. **Done** — the two muted floor renders are wired (see *Known TODOs*).
- **Credits:** a minimal colophon before the footer crediting the team (roles, names,
  linked company sites; no bios). **Complete** — original architect confirmed as
  Vardastudio (Andreas Vardas); Renovation by G. Patsalides Construction & Renovation
  (Georgios Patsalides) added. Heading: "The minds behind the house."
- **The interior (withdraw):** a quiet evening/retreat beat after *The garden* — the
  upper floor withdraws; the evening-warmth line (“a low fire, the slow heat of water,
  the rooms turned down to a glow”) lives here. Mood only, never rooms or amenities.
- **Accessibility / SEO:** canonical + Open Graph (`og:url` / `site_name` / `locale`) +
  `theme-color` + a minimal, non-private `WebSite` JSON-LD; mobile toggle tap target
  enlarged. **Readability pass** (standards memo: `docs/readability-and-visual-quality.md`;
  audit: `docs/readability-audit.md`) — all text passes WCAG AA in both themes; a new
  `--field-line` token brings input/toggle borders to non-text 3:1 (SC 1.4.11); day
  `--ink-mute` darkened to ~5:1 (glare margin); mobile `--section-y` floor cut to 3.5rem
  (desktop unchanged); eyebrow → 0.78rem; paragraph spacing → 1.4rem.
- **Materials section:** restructured as “the palette drawn from the coast” — a short
  concept (the colours gathered from the sea’s light, the cliffs, the coastal herbs, the
  inland woods) then the materials as execution, grouped under those four colour-notes.
  Curated to the eight that tell the story; the two **Corian** finishes are dropped from
  the public wall (they stay in the memo). The green accent sits under the coastal-herbs
  note in two weights — olive-green leather and rosemary-green fabric. Real macro
  photography is now wired (see **Images** above); each tile keeps its brand colour as a
  load-time tint behind the photo.
- **Day / Night:** **implemented.** A toggle (☀ / ☾) in the header switches the whole
  page between a day and a night mood via a `night` class on `<body>`. All colours come
  from role tokens (`--bg`, `--bg-soft`, `--ink`, `--ink-soft`, `--ink-mute`, `--accent`,
  etc.), redefined under `body.night`. Default is day; the choice is remembered via
  `localStorage` (wrapped in try/catch). **Always style with the role tokens** — a
  hard-coded colour will not adapt and will break the night view. The green accent is
  intentionally lighter at night so it reads against the dark. The real lighting scheme
  is warm (~3000 K), indirect and DALI-dimmable, so keep the night mood warm and soft.
  Framed as **Daylight / Afterglow** (the *afterglow* = the warm hour after sunset — **never
  blue**; aria-labels say so, ☀/☾ icons kept). A no-flash init `<script>` at the top of each
  `<body>` applies the saved theme before paint. A **`.shot-pair`** crossfade scaffold is in
  place (a day + warm-evening capture of the *same* viewpoint; the evening layer fades in under
  `.night`) for when paired photography lands — see **`docs/imagery-brief.md`** (the full
  photo/film brief). Plan: swap only the hero + *Views*/gallery; materials, plans, credits and
  the form stay static.
- **Gallery subpage:** a deeper photo-essay at `/gallery/` (`gallery/index.html`) —
  self-contained, **noindex**, **not** in the main nav; reached only by understated links
  at the end of *Views* and in the footer. Six chapters (Arrival → the ground that gathers
  → garden & terrace → western evening → the withdraw → materials) with labeled placeholder
  slots + a SHOT BRIEF; awaiting images via the pipeline (800w/1600w into `images/gallery/`).
  Buildless, so its `<style>` mirrors index.html's tokens **by hand — keep them in sync**.
  A quiet lightbox can be added once images land.
- **Legal page:** a discreet `/legal/` (`legal/index.html`) — self-contained, mirrors the
  design; combines the provider/imprint, a GDPR privacy notice, and a cookie/storage
  statement. Linked from every footer (next to *Gallery*). Controller is a **company**
  (placeholders `[ ]` for legal name / registration / VAT / address, pending the lawyer);
  contact `aethon-house-cy@outlook.com`. The form now links the privacy notice and the
  "never shared" line is corrected (Brevo named as processor). **No cookie banner** — only
  the functional day/night preference is stored (self-hosted fonts removed the Google CDN
  transfer). Indexable (unlike the gallery).
- **Renewal / origin (folded in):** the renovation story lives **inside *The architecture*** —
  no separate section, not in the nav. Its opening names the **Faros Beach Houses** origin and
  closes “Completed in 2026 … the same house, quietly raised.” No before/after imagery (no
  “before” photographs of the original house exist). The site is marketed only post-renovation,
  so it reads in the past tense, with no “under construction / owners away” implication.

## Still open (decide together — don't act unprompted)
- Current section order (established): Hero → The place → The architecture → The plan →
  The garden → The interior → Materials → Views → Register interest → Credits.
- Floor plans and credits placement — **decided:** the *Plan* sits after *The
  architecture*; *Credits* is a colophon before the footer.
- **Hero motion / a short film** — slots in place (a hero ambient-loop and an establishing-film
  plate in *The place*); commissioning is pending footage. Device policy: the **hero is a still
  on mobile** — any motion/video is desktop/wifi only. Brief: `docs/imagery-brief.md`.
- **Next up (the real frontier): photography.** Text + structure + responsive UX are
  essentially complete; the remaining quality is visual — commission the matched Daylight/
  Afterglow shoot per `docs/imagery-brief.md`, then drop pairs into `.shot-pair`, wire the
  woven plates + *Views* + `/gallery/`, and add the lightbox.
