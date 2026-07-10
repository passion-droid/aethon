# CLAUDE.md — AETHON

Persistent context for this repository. Read at the start of every session.

## What this is
The public showcase website for **AETHON House · Paphos** — a single private
residence on the western coast of Paphos, Cyprus. AETHON is a *quiet elevation* of an
existing seafront residence (originally part of the "Faros Beach Houses"): the
original architect's geometry is kept and honoured, the material and spatial language
refined. It is an evergreen brand presence, **not** a rental or an estate-agent
listing. Its quiet purpose is to hold a small, private interest list (the fuller
framing is in the internal docs). The site may be reached via a QR code at the property, so the first
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
- Fonts are **self-hosted** (LT Museum + Spectral, SIL OFL) — 4 woff2 in `/fonts/` (**latin subset
  only**; the copy is basic-Latin — add latin-ext only if accented text appears) + `@font-face`
  in each page's `<style>`; **no third-party CDN** (GDPR: no visitor IP to Google). Local too.
  **`--ff-display` is LT Museum** (`ltmuseum-lt.woff2` **Medium** + `ltmuseum-bold-lt.woff2`
  **Bold** — the brand display face: Medium for nav / labels / lockups, **Bold for the section
  eyebrows**; declared as two ranges `font-weight: 100 550` / `551 900`). **`--ff-text` is Spectral** (3 static faces — the body serif:
  headings + prose). LT Museum replaced **Jost** with Oli's brand assets; each face has a
  metric-matched `local()` fallback to hold CLS. (Brand mark + favicon also shipped — see *Known TODOs*.)
- **Mobile is the primary (QR) audience — mobile-first.** Fluid `clamp()` type, `100svh` hero,
  ~44px touch targets, 16px inputs (no iOS zoom), single-column stacking. **Touch affordances are
  capability-based (2026-07 mobile audit):** the 44px toggle, the quiet-link touch padding
  (incl. `.artifact figcaption a`, `.form-note a`, legal `a.link`), the hero-still/battery rule
  (drift off) and the hidden hero chip are gated `@media (max-width:640px), (pointer:coarse)` —
  so tablets and LANDSCAPE phones get touch sizing too, and a mouse desktop is untouched.
  **Landscape phones** (`(pointer:coarse) and (max-height:500px)`) additionally get the overlay
  menu instead of the wrapped desktop nav (menu top-aligned + scrollable there — centered flex
  clips overflowing lists; list padding clears the fixed bar), a JS resize guard so mobile
  URL-bar resizes don't close an open menu, and a touch more hero bottom padding. iPads keep the
  desktop nav (coarse but tall). Don't regress these to width-only queries. Desktop shows the
  inline nav links; **below 640px they are replaced by a quiet full-screen overlay menu**
  (`#menu` + `#menu-btn` → "Menu"/"Close"; Esc to close, scroll-lock, background set `inert`,
  closes on link tap). The hero is a **still on mobile** (ambient motion/video reserved for
  larger/wifi); the hero light-drift is disabled < 640px. When paired photos land, limit the
  `.shot-pair` day↔afterglow swap to the hero on mobile (cellular data).
- **Desktop rhythm — one uniform two-column system.** Every content section is a `.two-col`:
  eyebrow + section title in a narrow left column, body in a wider right column —
  `minmax(0,1fr) minmax(0,2fr)` at ≥880px, collapsing to a single stacked column below. Image-led
  sections (*The plan*, *Materials*, *Views*) keep the two-col for their header + intro and drop
  their media **full-width below it** (the same place *The place* puts its `.plate`); *Register
  interest* puts the form in the right column, *In brief* the detail lists. Keep new sections on
  this pattern — don't reintroduce a centered single column or a `.measure`-capped title. Page
  width is `--wrap` (84rem), so the right column caps at ~56rem (relevant when sizing list/figure
  content inside it). **Short bodies bottom-align (2026-07):** `.two-col > div:last-child{ align-self:
  end }` at ≥880px seats a short right-column body level with the header column's lower edge (so it no
  longer starts high and ends short of the title) — self-correcting, no effect when the body is the
  taller column. Body `<p>`s cap at `max-width: 44rem`; *Register interest*'s form is left-aligned to
  match (`.interest{ max-width: 44rem; margin: 0 }`, not centred). Don't revert these to top-aligned
  or re-centre the form.
- **Spacing encodes grouping (proximity), not vibes.** Vertical gaps follow the Gestalt law of
  proximity: related items sit closer, group breaks sit wider, on **one consistent ratio** (tight
  ≈ ½ of loose) and ideally on the 8-pt grid. **A label hugs what it labels** — an eyebrow should
  sit closer to its title than two body paragraphs sit to each other; a sub-label should hug its
  list, not float between two. Worked example: the **hero** is two proximity groups
  (`[descriptor + AETHON]` · gap · `[house of light + hero-line + subline]`) via
  `--hero-gap-tight` (≈16px) / `--hero-gap-loose` (≈40px, ~2.5×). When adding or adjusting spacing,
  reuse the existing rhythm and make the gap *say* the relationship — don't invent a one-off rem
  value. (Now applied site-wide as the **`--space-*` scale** — 8-pt tokens in each page's `:root`,
  hand-synced across all four files like the colour tokens; fluid section rhythm stays
  `clamp()`-based. The full scale, proximity model and the audit it came from:
  `docs/spacing-and-rhythm.md`.)

## Deploying a change
- Hosted free on **GitHub Pages**, served from the **`main`** branch, root folder.
- A change goes live ~1–2 minutes after it is committed and pushed to `main`.
  So the loop is: edit `index.html` → commit with a short message → push to `main`.
- **A push is NOT a deploy — verify the Pages run before reporting "live" (2026-07-05).** GitHub
  Pages builds+deploys via the `pages build and deployment` workflow; the **deploy job can fail
  even when the push and the build succeed** (seen 2026-07-05: build green, deploy died with the
  generic `Deployment failed, try again later` — the site silently kept serving the previous SHA).
  After every push: check the run for the pushed SHA via the GitHub MCP
  (`actions_list list_workflow_runs`, match `head_sha`; logs via `get_job_logs failed_only`) and
  only call it deployed on `conclusion: success`.
- **One push per deploy — never stack pushes ~1–2 min apart.** Batch ALL commits of a working
  session step (site files + CLAUDE.md + docs) into a **single push**: back-to-back pushes put two
  Pages deployments in flight and they can BOTH fail with the generic error above (exactly what
  happened 2026-07-05, two pushes ~70 s apart). If that error appears with a green build job, the
  content is fine — **do not debug the HTML**; retrigger with one fresh commit+push (empty commit
  ok) and verify the new run.
- The live site **403s automated fetches** (bot protection) — to confirm what's live, compare the
  repo to `origin/main` (they're identical once merged) rather than fetching `aethon.house` — and
  since 2026-07-05, "compare the repo" is not enough: confirm the **Pages run succeeded** too.
- **The git proxy in this env can be flaky.** Pushes sometimes fail with a *spurious*
  `non-fast-forward`/`behind` rejection, and ref-**deletions** return a 403 — both transient. Trust
  **`git ls-remote origin main`** (authoritative remote SHA) over the possibly-stale local
  `origin/main` ref, and just retry the push. Once, a local checkout drifted to an old commit
  mid-session — `git fetch && git reset --hard origin/main` restores the working tree to what's live.
- **Boot check — the fresh container often comes up on a stale branch** (seen repeatedly landing on
  `claude/brand-assets` at an old HEAD, so the working tree — even `CLAUDE.md` — reads out of date).
  **First thing each session, re-sync to live:** `git fetch origin main && git checkout -B main
  origin/main`, then verify against `git ls-remote origin main` before trusting any file. Deploys go to
  `main` directly (there is no PR flow for this site — GitHub Pages serves `main`); a `main`→`main` PR
  is not a real thing to open. **The reset can also strike MID-SESSION — repeatedly** (2026-07-03:
  THREE times in one session; the container recycles during any longer pause and silently re-clones
  onto the stale branch — uncommitted work applied after that point lands on the wrong files, and
  the harness's file-read state resets, so Edit calls start failing with "has not been read").
  Rules of thumb: re-verify `git rev-parse HEAD` vs `git ls-remote origin main` **before every
  batch of edits**, not just at boot; commit+push in small increments so at most minutes of work
  are at risk; after a recycle, prefer asserted python/script replacements over the Edit tool
  (no read-state needed) or re-Read files first. A tell: greps suddenly return pre-audit content
  or previously-fixed bugs "reappear".
- **Internal docs live on the `internal` branch (2026-07-03)** — GH Pages serves everything on
  `main`, so the strategy memos were leaking onto the public domain (audit finding SEO-1). All of
  `docs/` (imagery brief, SEO playbook, styleguide memo, spacing/readability notes, signage, the
  site-audit working memo) + the Design-Source-Memo now live ONLY on `internal`. **Every `docs/…`
  path referenced in this file means the internal branch.** Read without switching branches:
  `git fetch origin internal && git show origin/internal:docs/<file>`. Commit doc updates to
  `internal` via a temporary worktree — safer than switching the main checkout (which a container
  recycle can strand): `git worktree add <scratch>/internal-wt internal`, edit + commit + push
  there, then remove it. **Two traps that have bitten:** (a) after `git worktree remove`, every
  later command in the SAME Bash call dies on a dead cwd — end the call there; the next Bash call
  resets cwd to the repo. (b) A push-verify loop comparing `git rev-parse HEAD` to ls-remote
  **false-positives when both evaluate empty** (dead cwd → "" == "") — always require the remote
  SHA to be non-empty before declaring a push confirmed. Never re-add the docs to `main`. `scripts/`
  stays on `main` (the GitHub Actions workflows need it) but is robots-disallowed.
- **Stale remote branches to delete (user-side).** ~10 old `claude/*` branches linger; deleting them
  can only be done via the GitHub *Branches* UI — the proxy 403s git ref-deletions and the GitHub MCP
  tools have no delete-branch action. Not something this agent can clear.

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
- Patiti (πατητή) — Mediterranean hand-pressed lime plaster ~ `#C5B292` (wave-structured wall texture; replaced Venetian plaster in *The material language*)
- Corian "Witch Hazel" ~ `#E8DDC9` (pale, lit shelving)
- Iroko solid wood ~ `#9C6A3E` (warm hardwood)

Outdoor shading (sails / awnings) is warm sand / oyster-white (Arizona / RAL 1013) — keep
any shade imagery or copy in that warm-neutral register, never stark white.

## Copy voice
Calm, museal, understated. Short sentences, sentence case, no exclamation marks, no
superlatives, no marketing tone. Tone references: Aman, Tadao Ando. A little human warmth
is allowed (the V&A / Six Senses corrective) — restraint, not coldness.

## Known TODOs
- **Physical brand — stone signage blueprints: done (2026-06).** `docs/signage/` holds a fabrication
  study for the property's markers, to hand to G. Patsalides + the stone carver: an **entrance
  travertine/marble plate** (hand-carved V-cut wordmark, **gild the dot over the O only**, inset QR)
  and a **seaside sandstone monolith** (deep-cut, bare, no QR) — each a dimensioned SVG + print PDF.
  Plus **`aethon-qr.svg`** — a **working QR** (links to `aethon.house`, error-correction **H**, the
  brand **"A"** at centre; **verified scannable** by decoding it back with OpenCV). Reproducible via
  `scripts/gen-signage-blueprint.py` (needs `segno`, `opencv-python-headless`, `Pillow`). Dimensions
  in **mm**; a *design study* (verify on site, not for structural use); **no address** anywhere.
- **`/icon.svg` favicon — DONE (2026-07).** All four pages' `<head>` links
  `<link rel="icon" type="image/svg+xml" href="/icon.svg">`; the file had been missing (404 on every
  page — cosmetic, browsers fell back to `favicon.ico`/PNG). Fixed by adding **`/icon.svg`**: the brand
  low-crossbar "A" (glyph + crossbar lifted from `brand/logo-dark.svg`'s last `<g>`) in white on an
  olive `#4C5039` rounded square (rx 16%), the A scaled to ~52% of a 512 canvas and centred via its
  computed bbox. Served now — no more 404. (726-byte static vector; no build step.)
- **Images:** an `images/` folder + a **buildless optimisation pipeline** now exist — see
  `images/README.md` (AVIF→WebP→JPEG via `<picture>`, 400/800w, uniform 3:2, sRGB,
  metadata stripped; Pillow runs it in-session). **Materials done:** the 8 macro swatches
  are wired (48 assets in `images/materials/`, brand colour kept as a load-time tint;
  **Patiti** — the Mediterranean hand-pressed lime plaster — replaced Venetian plaster, #53).
  Still placeholders, awaiting real images via the same pipeline: the hero ambient loop,
  the establishing-film plate in *The place*, companion images under *The architecture* /
  *The garden* / *The interior*, and the eight-slot *Views* gallery (in-code shot brief). Scales to ~20–30 photographs; once they land,
  consolidate woven vs. gallery to avoid duplication. **The full brief is `docs/imagery-brief.md`
  on the `internal` branch — Rev B (2026-07-05), synced to the live slots and shared with the
  owner's photographer contact** (external-ready render: `internal:docs/imagery-brief.pdf`, brand
  type, no address / no sale framing / contact mail@aethon.house; Appendix A maps all 15 front-page
  frames + 23 gallery captions; adds the og/social 1200×630 master as a deliverable). A
  **personalized German edition for Fynn Daubner (Envisory — the owner's photographer/videographer
  contact, Cyprus-based)** is `internal:docs/imagery-brief-fynn-de.{md,pdf}` — Du-Form, neutral from
  AETHON (not owner-signed), **photo + film co-equal** (§8 "Der Film" is a full chapter — hero loop,
  establishing film), purely creative (no logistics/terms) — all owner decisions 2026-07-05; live
  captions stay English (the site's labels). **Reworked same day after owner feedback ("liest sich
  wie Wort-für-Wort-Übersetzung — no-go"): full German NEUSCHRIEB** — idiomatic, brand-register (no
  calques; the list is a "Wunschliste — Ausgangspunkt, nicht Grenze"; A/B/C/D instead of Tier
  jargon), plus a **creative-latitude layer** (owner: he's strong in Konzeption, don't make it read
  as a strict spec) — new §9 "Dein Blick" (Landkarte, kein Drehbuch; better ideas explicitly
  welcome) + §8 closes with "dein Terrain"; **PDF links are clickable** (6 URI annotations
  verified: aethon.house ×2, /gallery/ ×2, Dear Modern, mailto). Rule for German docs: write
  natively in German, never translate the English line by line; verify „…“ quote pairs + link
  annotations before shipping. If slots or
  captions change on the site, re-sync BOTH briefs + regenerate the PDFs before re-sharing. Key
  viewpoints must be shot as **matched Daylight +
  warm-evening pairs (same locked-off viewpoint)** for the `.shot-pair` crossfade — warm afterglow,
  **never blue**; strip GPS/EXIF; deliver masters (the pipeline makes the web assets).
- **Floor plans: done.** The *Plan* section (after *The architecture*) shows the two floor
  renders, **muted into the stone/olive palette** (global desaturation + the pool's blue
  specifically collapsed to pale water, per the no-blue guardrail), processed into
  `images/plan/` (AVIF/WebP/JPEG, 800/1600w, full √2 ratio, no crop). **Re-shot from new 4K
  masters and now transparent** (AVIF/WebP keep alpha; the JPEG fallback is flattened on
  `--bg-soft`) so the plan sits on the page and **adapts to Daylight/Afterglow** — it floats on
  the warm dark stone at night — the frame's background box is removed so they sit on the page
  `--bg`, with a **contour-following `filter: drop-shadow`** (`--plan-shadow`: a dark lift in
  Daylight, a warm afterglow halo at night) that follows the plan's cut-out shape, never a box.
  The exact muting recipe is reproducible in
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
- **Icons / brand mark — DONE (Oli's styleguide, wired).** Full spec in
  **`docs/brand-styleguide.md`** (+ the PDF). Shipped across all four pages: **LT Museum** (OFL)
  self-hosted as `ltmuseum-lt.woff2`, now `--ff-display` (replaced **Jost**; **Spectral** stays for
  body/headings); the **AETHON logo** image-replaces the header mark, hero wordmark and footer mark
  (`/brand/logo-{dark,white,whiteout}.svg`; the "AETHON" text is kept off-screen for SEO/a11y) —
  **day = dark + gold dot · night = white + gold dot · footer = whiteout**; and a **favicon set**
  from the square "A" icon (crisp `icon.svg` SVG favicon + ico/PNG fallback + maskable `apple-touch`) + `site.webmanifest`,
  linked in every `<head>`. **Gold stays logo-only** (owner decision — UI accent stays green; gold
  reads close to coastal-sandstone, so it sits in the stone palette). Brand palette **gold
  `#C1A152` · olive `#4C5039` · warm black `#222216`** (+ 60/20% tints) recorded for future use.
  Masters (`.ttf`, source SVGs, the raw favicon) aren't committed — only the served assets are.
- **`og:image` / `twitter:image`: INTERIM LIVE (2026-07-09).** The branded master is live at
  `/images/og.jpg` (1200×630, ~22KB progressive JPEG): **logo-white with the gold dot on warm
  dark stone, the afterglow glow upper-right** — warm, never blue; reads at thumbnail size
  (WhatsApp-checked at 400px). All five metas are active in `index.html` (og:image + dims + alt,
  twitter:image + alt); the alt text stays as pre-written. **When photography lands, replace the
  FILE at the same path** (same dims, warm/afterglow register) — no meta edits needed. Master
  recipe: scratch HTML (night tokens + logo-white) → Playwright screenshot → JPEG q88.
- **SEO / meta pass — done (PR #39; title refined #49).** The meta/OG **descriptions** carry the
  searchable terms (seafront residence · Paphos, Cyprus · Faros beach, "a sanctuary…"); the
  **site name** (`og:site_name` + `WebSite` JSON-LD `name`) is the poetic lockup **"AETHON ·
  House of Light"** (#52 — Google was ignoring bare "AETHON" and falling back to the domain), while
  the **`<title>` + og/twitter titles** lead with **"AETHON House — private seafront residence"**
  (#52 de-duped the tagline out of the title now that the site-name line carries it — both still
  lead with the **"AETHON House"** lockup; the #49 "house of light" title moved into the site name). Added a `twitter:card`
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
  Aion"** mosaic site → always use the **"AETHON House"** lockup — the `<title>`/og/twitter titles
  lead with the **"AETHON House"** lockup to disambiguate + match the `.house` domain (the site-name line carries *House of Light*, #52). Highest-
  leverage off-page win: a backlink from the **credited team** (Vardastudio, House Talks, Dear Modern
  / Cliff Tan). **GSC + sitemap: done by owner** (domain verified, `sitemap.xml` submitted, `/` +
  `/legal/` discovered).
- **SEO measurement — automated (PR #40, extended #42).** `scripts/seo-pull.py` +
  `.github/workflows/seo-insights.yml` pull **Search Console + PageSpeed Insights + Cloudflare Web
  Analytics** on the **1st & 15th** (≈ fortnightly) and on demand, emitting a dated report as a
  **workflow artifact + run summary** (nothing committed — safe for any repo visibility). Auth via
  GitHub secrets **`GSC_SA_KEY`** (service-account JSON added as a GSC user), **`PSI_API_KEY`**, and
  **`CLOUDFLARE_API_TOKEN`** + **`CF_ACCOUNT_TAG`** (+ optional **`CF_SITE_TAG`**); every source
  degrades gracefully before its secret is set. **All three live (2026-06-27):** GSC (1 impression,
  pos 27); **PSI 100/100/100/100 on mobile + desktop** (CLS 0, TBT 0 — validates the buildless/perf
  work); Cloudflare pull authenticating (0 visits until the beacon collects). A one-off
  **`cf-dns-check.yml`** diagnostic also exists (it debugged the Porkbun→Cloudflare nameserver
  migration via the same `CLOUDFLARE_API_TOKEN`). This is **tooling, not part of the site** (the
  page stays buildless). Setup in `docs/seo-and-search.md`.
- **Analytics — decided: cookieless, no banner (no Google Analytics).** GA4 = personal data to Google
  + cookies → EU consent banner, and re-introduces the visitor-IP-to-Google transfer the self-hosted
  fonts removed. Chosen: **GSC (search) + Cloudflare** (dashboard if the domain is proxied — zero code;
  else the cookieless Web Analytics beacon). Self-hosted **Umami** was noted as the step up for on-page
  events — **superseded 2026-07-09 by the first-party events worker (next bullet)**; Umami stays
  the fallback only if a clickable dashboard is ever wanted. Owner action + the one-line beacon
  snippet are in `docs/seo-and-search.md`. **Never add GA
  or any cookie-setting analytics without revisiting the consent/no-banner stance.**
- **On-page events — LIVE (2026-07-09, owner-directed "Eigenbau"):** first-party, anonymous
  per-day counters via a **Cloudflare Worker** (`aethon-events`, route **`aethon.house/e*`**, KV
  namespace `aethon_events`) — no third party, no cookies, no IDs/IPs/UAs stored; **DNT + Global
  Privacy Control honoured on the page AND at the edge**; KV lost-update races (±1) accepted at
  this scale. **Allowlist (17) in `scripts/cf-worker-events.js`:** `via-gate`/`via-sea`
  (**dormant** — owner chose PURE stone QR URLs; params remain available for future digital
  shares), `afterglow`/`afterglow-auto` (chosen vs given — auto = R4 night-at-load without saved
  pref; chosen = MutationObserver on a later switch into night, once per visit),
  `hold`, `film-play`+`hero-loop` (pre-registered — wire `window.__aeEv('film-play')` into the
  media play handlers when footage lands), `ch-place…ch-views` + `reach-register` (chapter reach:
  IntersectionObserver **threshold 0 + rootMargin '0px 0px -25%'** — ratio thresholds never fire
  on sections taller than the phone viewport), `form-start`/`form-submit` (sendBeacon survives
  the Brevo navigation). The beacon IIFE sits in index.html BEFORE the hold module (hold's
  `engage()` calls `window.__aeEv('hold')`); one count per event per pageview; `?via=` is counted
  then stripped via `history.replaceState`. **No beacons on gallery/legal** (Cloudflare already
  counts their views). **Read path:** the fortnightly report — `seo-pull.py pull_events()` reads
  the KV buckets via `CLOUDFLARE_API_TOKEN` (owner extended the token 2026-07-09: Workers
  Scripts:Edit, KV Storage:Edit, Zone:Read, Workers Routes:Edit). **Deploy:**
  `deploy-events-worker.yml` (workflow_dispatch) → `scripts/deploy-events-worker.sh` — idempotent
  (namespace create-or-get, module upload with KV binding; on failure it names the missing token
  permission). **The route `aethon.house/e*` is OWNER-MANAGED** (created by hand in the dashboard
  2026-07-09 after the token's route permission couldn't be located; the script treats a missing
  route permission as fine and only requires the worker upload). **Route gotcha that cost a day:**
  the hand-made route was first saved as `*.aethon.house/e*` — a `*.`-prefixed pattern matches
  subdomains only, NEVER the apex domain, so the worker sat at 0 invocations while real traffic
  flowed; fixed to `aethon.house/e*` (owner, 2026-07-10) and the chain verified end-to-end the
  same minute (first counters: 7 chapters ×2, reach-register 2, afterglow 1, form-start 1).
  The worker also keeps a `_hits:<day>` heartbeat (counts EVERY /e request, no name, 60-day
  TTL) — it appears in the report table; read it as route-level diagnostics, not as an event. **Verification path:** curl/
  headless probes CANNOT reach aethon.house — the zone's bot protection 403s non-browser clients
  before the worker, and this session's egress proxy blocks the domain entirely
  (ERR_TUNNEL_CONNECTION_FAILED) — so the factual end-to-end check is: real visitor (or owner's
  phone) fires events → `seo-insights.yml` reads the KV counters into the report. Legal's hosting paragraph now discloses the counters +
  DNT/GPC (counsel batch re-checks wording). Verified by a **21-check Playwright matrix**
  (route-intercepted beacons: via count + URL strip, full chapter-scroll set, afterglow
  once-per-visit chosen vs auto, hold, DNT ⇒ zero beacons, form start/submit through native
  submit).
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

## Audit decisions (2026-07-03 — seven-persona review; working memo: internal:docs/site-audit-2026-07.md)
- **No confirmation email — single opt-in (owner-confirmed).** Brevo DOI is OFF and stays off; the
  thank-you states completeness ("no confirmation email will follow") and the legal notice says
  registration completes on submission. **Never re-introduce "a confirmation email completes your
  sign-up"** in copy, legal or code comments.
- **Cloudflare proxying confirmed (orange-cloud)** → named beside GitHub Pages in the legal
  *Hosting* section. **Cloudflare Web Analytics is ACTIVE** (auto-injected at the edge — no code
  in the repo; first data 2026-06: ~60 visits/28d) and the notice discloses it since 2026-07-04
  ("cookieless, aggregate visit statistics — no cookies, no cross-site tracking, no personal
  profiles"). Keep notice and reality in sync if analytics ever change.
- **Logo letters stay warm black on screen (owner: "leave as is").** The styleguide PDF's primary
  logotype is olive-lettered (#4C5039) — that remains the reference for print/physical; the shipped
  warm-black `brand/logo-dark.svg` is the sanctioned on-screen variant. Don't "fix" either direction.
- **Bedrooms are public: 3+1** (In brief row; owner 2026-07-09 — was "3"; the +1 reads as the
  flexible fourth room without contradicting the gather/withdraw story).
- **Gallery ends with a register path** (quiet "Register interest" link at the close — the
  audit's top visitor finding). Keep it when the gallery is redesigned around real photography.
- **C-item walkthrough decided + shipped (2026-07-04):** mid-page register pointer at the end of
  *The plan* (.more-link style); the interior's closing line "See the house in its evening — the
  small moon, above." is a text **button that sets Afterglow** (no-op/undotted at night); Gallery
  links carry a small ↗ (`.ext`) in nav + overlay menu; the orientation line is now "This is the
  portrait of AETHON — …"; the journalist's 11-edit copy bundle shipped (incl. **"the blazing
  one"** as the public gloss of Αἴθων — was "shining"; Oxford commas are house style; "pressed
  into waves"); chapter numbering runs to **07 · Views** (Register/In brief stay unnumbered);
  gallery + legal carry minimal **OG blocks** (text previews); JSON-LD gained the locality-only
  **`about: Residence`** node + alternateName array; **gold formally closed as logo-only**; the
  footer mark is now **logo-white (gold dot)** — rule: *on screen the dot is always gold*,
  whiteout is for one-colour physical repro; the **WIP notice is session-gated** (once per visit,
  sessionStorage `aethon-wip`; legal's storage section discloses it); counsel-batch wording is
  pre-drafted in place (SIGNGUARD relation clause, form metadata/IP, bounded retention, "no
  cookies at all") — lawyer reviews the finished page. **Kept against reviewers:** "The withdraw"
  chapter noun, the "Register interest" button label, "ancient olive trees" (owner-verified),
  the bar mark stays always-visible (C-20 parked); C-21 (sunset-default Afterglow) **has since
  shipped early, owner-directed (2026-07-05)** — see the *Day / Night* interactive layer.
  **Renewal design = owner-directed** (internal fact for press enquiries; public credits
  unchanged by choice — offer a visible credit row only if the owner asks).
- **Greek word renders in brand type:** `fonts/greek-aithon-lt.woff2` (5-glyph EB Garamond Italic
  subset, OFL, ~2.6KB) is declared into the Spectral stack via `unicode-range` for Αἴθων.
- **mail@aethon.house — LIVE (2026-07-03).** Cloudflare Email Routing forwards to the owner's
  Outlook inbox (inbound only — replies still show the outlook address until a real mailbox on the
  domain exists). The address lives ONLY on `/legal/`
  (imprint + rights) — the *Enquiries* row in the In-brief colophon (once added for JRN-4/C-11)
  was **removed by the owner 2026-07-05**: the homepage is address-free by choice; don't re-add
  the email anywhere on the homepage unprompted. **Owner: NO address beneath the register form**
  — the form area stays form-only. Never publish the outlook.com address again.
- **Meta rules from the audit:** subpage titles carry the "AETHON House" lockup; `lang="en-GB"`
  on all four pages; "Faros Beach" capitalised in meta; `data-nosnippet` stays on the WIP card.
- **Signage = REV D (2026-07-08, owner-requested):** the entrance plate is a **LANDSCAPE honed
  marble tile 600 × 450 × 20** (REV C's brief portrait 450 × 600 was corrected by the owner the
  same week — the plate is landscape). **All dims are plain mm for the stonemason — no typographic
  jargon:** the wordmark carries width + height dims (**420 × 97**; keynote adds "letters 69
  high" — the word "cap" is banned from the sheets), the monolith's wordmark is dimensioned
  **400 × 93** (letters 66 — REV C had inherited a WRONG "cap height 180" callout), and **both QR
  plates grew to 150 × 150** (spec: ≈118 code in a 150 tile, quiet zone ≥ 4 modules). The
  monolith's section panel now shows **both cuts: the V-incision AND the routed QR pocket**
  (plate flush, ≈6 recess). Setting-out (entrance): tile top ≈ 1600–1620 AFL → wordmark centre
  ≈ 1480–1500, QR centre ≈ 1260–1280. **Artwork rule stays explicit on the sheet:** the carved
  wordmark comes **from the logotype FILE (brand vector) — never typeset in the LT Museum font**.
  REV B keeps: **monochrome print set**; monolith carries the engraved URL + inset QR (flush
  enamel/316 — never carved into rough stone). Generator: `scripts/gen-signage-blueprint.py` on
  main; assets on `internal:docs/signage/`; PDFs printed from the SVGs at 1320×980 via headless
  Chromium. **Learned: leader/caption collisions only show in the RENDER — always rasterize both
  sheets and look before shipping** (two text overlaps caught this way in REV D).
- **Search/traffic traction (2026-07-09 pull; baseline 07-03 in parens):** GSC — query
  **"aethon" at position 1.1** (9 impressions, CTR 11%; site avg 6.5 across 17 impressions —
  dragged by stray queries; was pos 27 mid-June, 6.1 on 07-03). Cloudflare — **90 visits /
  150 views per 28d** (~60/90), CY 90 + US 60 views; **/gallery/ 20 views, all via homepage
  nav** (visitors do descend — quantifies the photography priority). PSI desktop 100×4;
  **mobile perf 97** — the WIP dialog is the LCP on fresh visits (see photography-day
  checklist); trigger runs via `seo-insights.yml` workflow_dispatch, read via job logs. Owner's
  WhatsApp share test passed (preview scrapers are not bot-blocked); shared links now carry the
  interim branded og:image.
- **Workflow-artifact downloads are proxy-blocked** (Azure blob 403 — policy; don't retry). Read
  run results via the GitHub MCP job logs instead (`get_job_logs`, tail).
- **Playwright-testing gotchas (learned the hard way):** plain `window.scrollTo(x,y)` obeys the
  page's `scroll-behavior:smooth` — sample positions only after settling, or pass
  `{behavior:'instant'}`; lazy images report `complete:false` until scrolled near, so scroll
  first, wait, then assert; after a container recycle, one-off "impossible" states (e.g. a
  scroll-lock that won't release) may be transients — re-run the exact sequence before
  diagnosing code; and screenshots taken mid-transition (menu fade 450ms, theme 700ms) look
  like bugs that aren't — wait the transition out. And in Bash heredocs: an UNQUOTED
  delimiter (needed for $VAR expansion) lets backticks run as command substitution and
  silently eat content — pass values via environment (`WT="$WT" python3 - <<'EOF'`) and keep
  the delimiter quoted. And the container's system `cryptography` package is broken (cffi
  backend panic), which kills `pypdf` on import — verify PDF link annotations by scanning the
  raw bytes for `/URI (…)` (or via pypdfium2), not with pypdf.
- **Owner-side micro-todo:** on a real iPhone, glance at (a) the landscape overlay menu and
  (b) the new dusk sweep + hold-to-preview (Chromium emulation is green everywhere; real iOS
  Safari unverified — Safari 18+ should run the sweep, older falls back to the plain crossfade).
- ~~Still open from the audit~~ **The audit is fully closed (2026-07-04):** every group-B and
  group-C item is decided and shipped (see the walkthrough block above + the memo's checkboxes).
  The only audit artefact still live is the **photography-day launch checklist** (strip
  "forthcoming" labels in the image commit; re-sample text-over-photo contrast per frame; retire
  the WIP notice; re-check the toggle border over the real hero; **re-run PSI — the mobile 97
  (2026-07-09) is the WIP dialog itself**: on a fresh visit the dialog body becomes the LCP
  element (measured via throttled probe — hero-line 696ms without dialog, dialog text re-claims
  LCP at ~1.3s with it), so retiring the notice should return mobile to ~100).

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
  **Cliff Tan's concept sketch lives HERE (owner, 2026-07-04** — moved from *The
  architecture*): text → artifact → plate rhythm, the sketch as the section's exhibit
  before the future photograph. Caption owner-approved same day: **"Concept sketch — the
  rooms, from within"** (was "the ground floor that gathers" — dissolved the
  gather/withdraw tension); the alt text still names the ground floor, factually.
  *The architecture* keeps text → timeline → plate only.
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
  **Interactive layer — R1–R4 shipped (2026-07-05, owner: "implement all", placeholders until
  photography):**
  (R1) **Dusk sweep** — the toggle runs a feathered mask sweep on the **View Transitions API**
  (Baseline 2025): night draws in from the left, day returns from the right (1600ms,
  `html[data-sweep]` picks the direction); reduced-motion / no-support falls back to the token
  crossfade untouched; `html.vt-live` suspends all CSS transitions during a sweep so the page
  beneath snaps atomically. **Keep the VT mask rules UNPREFIXED** — adding `-webkit-mask-*`
  aliases beside them silently kills the keyframe interpolation in Chromium (cost a debug ladder;
  comment in the CSS). **The day direction runs its OWN reversed keyframes (`dusk-sweep-back`,
  0%→100%)**: the mirrored `-105deg` gradient carries its black head at the mask's other end, so
  sharing the night keyframes plays the wipe BACKWARDS — day flashes in at t=0, night re-covers
  it, hard pop at the end (shipped broken 2026-07-05, user-caught). **Testing rule: a single
  mid-sweep screenshot cannot catch a reversed wipe** (the still looks identical either way) —
  verify direction with a frame BURST + left/right luminance strips and assert monotonic
  progression (probe pattern in the session notes). Sweep CSS/JS hand-synced across index +
  gallery + legal.
  (R2) **Hold-to-preview** — `[data-hold]` paired views (currently the two pause plates) show the
  *opposite* hour while pressed: touch still-hold (200ms, >10px movement = scroll → cancels),
  mouse-hold, or holding Space/Enter (focusable, role=button). Placeholders flip their frame
  tokens locally (`.shot-pair.held` — values hand-synced with `:root`/`body.night`); the `.held`
  image rules for real pairs are already in place. **Cursor = the other hour's glyph** on fine
  pointers (moon in a dark disc by day, sun in a marble disc by night; data-URI SVGs). The pause
  labels carry a `· hold for the evening/daylight` affordance (`.hold-hint` CSS content);
  aria-labels re-name the hour via a body-class MutationObserver.
  (R3) **Second toggle + discoverability** — the hero chip (`.hero-media`) is now a working
  toggle `<button>`: moon/sun icon + "Daylight / Afterglow" with the inactive hour dimmed
  ("· forthcoming" dropped from it); still hidden on touch/small screens. A **one-time hint**
  ("Afterglow — the warm hour after sunset", `role=status`, localStorage **`aethon-hint`**)
  appears under the bar on a visitor's first switch to evening. *Views* gained an in-copy
  evening door — "Every view here keeps two hours — see the evening." (`.evening-line`, same
  no-op-at-night pattern as the interior's; **new copy — revisit if the owner wants different
  wording**). The evening-line binder now wires ALL `.evening-line` instances.
  (R4) **The site keeps the house's hours** (C-21, shipped early by owner instruction): a first
  visit with **no saved theme** arriving after sunset at the house opens in Afterglow — a
  mid-month Paphos sun table + Cyprus wall-clock via `Intl` (`Asia/Nicosia`, DST handled), **no
  geolocation**, and the automatic evening is **never persisted** (only explicit toggle choices
  are). Lives in the **no-flash init** of all three pages (hand-synced); the main theme IIFE now
  seeds from `body.night` — don't regress it to a hard `'day'` default. Legal's storage sentence
  discloses the hint flag (two functional local-storage notes + the session note; counsel batch
  re-checks wording). Verified by a **42-check Playwright matrix** (sweep both directions +
  cleanup + fallback; hold engage/quick-tap/keyboard/scroll-cancel; cursor + aria swaps; chip
  sync, hint show/retire/once; clock cases summer/winter/DST + saved-pref precedence; gallery +
  legal parity; zero page errors).
- **Gallery subpage:** a deeper photo-essay at `/gallery/` (`gallery/index.html`) —
  self-contained, **noindex**; now linked from the **main nav** (homepage header + overlay menu)
  as well as the end of *Views* and the footer. Six chapters (Arrival → the ground that gathers
  → garden & terrace → western evening → the withdraw → materials) with labeled placeholder
  slots + a SHOT BRIEF; awaiting images via the pipeline (800w/1600w into `images/gallery/`).
  Buildless, so its `<style>` mirrors index.html's tokens **by hand — keep them in sync**.
  **Layout vocabulary (pass 3, 2026-06):** `.plate.feature` (full-bleed 21:9), `.plates`
  (default pair), `.offset` (asymmetric two), **`.trio`** (one large + two stacked — fixes the
  3-image "2 + orphan" problem, used in *Ground* + *Withdraw*), **`.three`** (artifact collection
  row, *Materials*), `.solo` (centred single). A **section tracker** (chapters I–VI) sits centred
  in the bar, scrollspy-driven (`.tracker`; `IntersectionObserver` rootMargin -45/-50%; chapter
  `<section>`s carry `id="ch-…"`). The **lightbox is built and testable now** — native `<dialog>`,
  opens **any** plate (a real photo, or the stone placeholder showing "Photograph forthcoming"),
  Esc / backdrop / ✕ / ←→, focus restore.
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
- **Experience-design review — quick-wins shipped; rest pending (2026-06).** A reviewer reframed
  the site as *a permanent exhibition / digital catalogue accompanying the house* — adopted as the
  guiding lens. **Shipped:** (1) an **orientation "wall label"** after the hero — *"AETHON is the
  portrait of one seafront residence on the Faros coast of Paphos…"* (the `.intro-line` beat);
  (2) **chapter numbering** `01–06` on the content sections (CSS counter on `#place…#materials`;
  Register/Credits stay un-numbered end-matter); (3) a **timeline** `2018 Built → 2026 Renewed` in
  *The architecture* (`.timeline`); (4) **"reveal only finished things"** — *all placeholder media
  is now hidden* via one rule `.hero-media, .plate, #gallery{ display:none }` until photography
  lands (Plan + Materials keep their real images). **To restore the photo slots, remove that rule**
  — the markup/scaffolding is intact. **Exhibition pass 2 — shipped (2026-06):** (5) **the gallery as the emotional
  centre** — chapters restructured into `<figure>`s with **captions as wall labels** beneath, a
  **layout vocabulary** (`.plates.offset` / `.solo`; full-bleed `.plate.feature` via
  `width:100vw; margin-left:calc(50% - 50vw)`), chapter VI expanded to ~6 **artifact** slots, a quiet
  **closing beat** (`.gal-close`), and a built-in **accessible lightbox** (native `<dialog>` +
  Esc/backdrop/←→, focus restore; **dormant until a `.plate` holds a real `<img>`**); (6) **silent
  full-bleed "pause" plates** (`.pause` / `.pause-media.shot-pair`) at two homepage scene-breaks
  (after *The Plan*, after *The interior*) — **currently visible labelled placeholders for review;
  add `.pause` to the reveal-only rule to hide them on the live homepage**; (7) **Day/Afterglow image
  crossfade** confirmed **already built** (`.shot-pair` in index + gallery) — no action, just needs
  photo pairs; (8) **curated artifacts** — **Cliff Tan's concept sketch wired as the first real
  artifact** in *The architecture* (uncropped, toned into the palette via `scripts/process-sketch.py`
  → `images/sketch/`; captioned + linked to Dear Modern; the raw master is removed from the tree per
  the no-originals rule, recoverable from history), plus an **Artifacts shot list** added to
  `docs/imagery-brief.md` (material still-lifes; never blueprints). **Copy shipped:** the *Tombs of the
  Kings* sentence simplified (**option C** — keeps the 'axis' geography + 'never within it'); the
  **"Visit" note merged into Register interest** ('…the house is met only by invitation … You are
  warmly welcome to be in touch below') rather than added as a separate beat. **Declined:** contributor
  portraits (the minimal no-bios credits stand); the reviewer's "renewal"/superlative hero line
  (post-completion framing + no-superlatives stand). **Gallery closing beat — confirmed (owner,
  option E):** *"This is the house, in the order of its day. To know the rest is to be there — by
  invitation, in time."* (ties to the by-invitation Register line). **PREVIEW TOGGLE — now ON by
  default (owner, 2026-07):** the #10 "reveal only finished" rule is gated behind `body:not(.preview)`
  and covers `.hero-media, .plate, .pause, #gallery` (+ a `body.preview .hero-photo` hero placeholder).
  **The homepage `<body>` now carries `class="preview"` — the site runs in "full live mode"**: every
  placeholder slot shows (hero placeholder photo, woven plates, both pause plates, the Views grid), so
  the whole page reads as it will once photography lands — no longer the finished-only state. **To
  return to finished** (only real content — the Cliff Tan sketch, floor plans, materials), **remove the
  `preview` class** from `<body>`. All scaffolding stays in the code either way; photography simply
  replaces the placeholders. (Paired with the *Work-in-progress notice* below, which tells visitors the
  preview state is intentional.)
- **Work-in-progress notice — shipped (2026-07).** A quiet, museal pop-up (`.wip`, a native
  `<dialog>` opened on **every load**, no persistence by design) tells a visitor the site is still
  being finished. Copy (owner-approved 2026-07-03, reworded from the original after the audit —
  "AETHON is finished; the *site* isn't"): *"This site is still being finished — the photography is
  on its way. What you see is the shape of it; please, look around."* Blurred backdrop
  (`.wip::backdrop` blur; day/night tint via `body.night .wip::backdrop`), card in the role tokens +
  LT Museum/Spectral with the AETHON logotype; closes via **✕ / "Look around" / Esc / click-outside**,
  then the page browses normally. Native `<dialog>` gives the focus trap + inert background for free
  (autofocus on "Look around"); reduced-motion-safe; graceful no-op if `showModal` is unsupported. On
  **index + gallery + legal** (not `404.html` — an error page); markup + CSS + JS are **hand-synced
  byte-identical** across the three files, like the token blocks. To retire it when the site is
  finished, delete the `.wip` block, the `<dialog class="wip">` markup and its IIFE from all three.
- **Hero — copy & spacing settled (#50, #52).** Both hero sentences run on one line on desktop
  (uncapped + `text-wrap: balance`/`pretty`; hero-line max font 2rem), balanced-wrapping on phones.
  Vertical rhythm is two proximity groups — `[descriptor + AETHON]` · gap · `[house of light +
  hero-line + subline]` — via `--hero-gap-tight`/`--hero-gap-loose` (≈16/40px). The fixed top bar
  solidifies at **20%** of viewport scroll (`innerHeight*0.2`, was 0.6) so it no longer overlaps the
  descending hero; the mobile hero-media overlap was fixed. Don't re-open these unprompted.
- **Hero motion / a short film** — slots in place (a hero ambient-loop and an establishing-film
  plate in *The place*); commissioning is pending footage. Device policy: the **hero is a still
  on mobile** — any motion/video is desktop/wifi only. Brief: `docs/imagery-brief.md`.
- **Desktop layout — settled.** The 1/3 · 2/3 two-column rhythm is now applied uniformly to
  *every* section (the makeover + a follow-up pass brought *The plan*, *Materials*, *Views*,
  *Register interest* and *In brief* onto it; see *How the site is built*). The structure/UX
  frontier is essentially closed — don't re-open the column layout unprompted.
- **Brand identity — done (Oli's styleguide, #54–#55).** LT Museum (Medium + Bold) self-hosted;
  the AETHON logo replaces the wordmark in header / hero / footer (day dark · night white · footer
  whiteout, gold dot kept); square "A" favicon + maskable app icons + `site.webmanifest`; section
  eyebrows set in LT Museum Bold; gold stays logo-only. Full record: `docs/brand-styleguide.md`
  + the *Icons / brand mark* TODO.
- **Next up (the real frontier): photography.** Text, structure, responsive UX **and the brand
  identity** are now complete; the remaining quality is visual — commission the matched Daylight/
  Afterglow shoot per `docs/imagery-brief.md`, then drop pairs into `.shot-pair`, wire the
  woven plates + *Views* + `/gallery/`, and add the lightbox. (A branded `og:image` — the logo on
  warm stone — is now possible as an interim until photography lands; see the og:image TODO.)
