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
  inline nav links; **below 701px they are replaced by a quiet full-screen overlay menu**
  (`#menu` + `#menu-btn` → "Menu"/"Close"; Esc to close, scroll-lock, background set `inert`,
  closes on link tap). **The overlay threshold was raised from 640 to 700 in the 2026-10 review:**
  measured, six links + mark + toggle cannot share one row under ~700px at any sane size (the
  mark was being squeezed to 0–94px and "Register interest" wrapped from 641 to ~890). In the
  **701–940px band** (iPad / iPad-mini portrait, narrowed windows) the bar tightens instead —
  `.bar .mark{ flex:none; width:5rem }`, links 0.62rem / 0.1em tracking / `nowrap`, bar padding
  4vw (the Afterglow hint + skip link follow that edge) — so iPads keep the desktop nav as
  decided. The band runs to 940 because the full-size bar only clears the mark with a coarse
  pointer's 44px toggle from ~920px (at 901 the gap was 4px; `flex:none` made it visible), and it
  is **scoped to where the inline nav shows** — `… and (min-height:501px), … and (pointer:fine),
  … and (pointer:none)` — because a width-only band also fired on landscape phones (844×390 is in
  range, uses the overlay) and shrank their mark / pulled the bar off the `--edge` column. The touch-sizing queries stay at 640
  (capability-based; different concern). The hero is a **still on mobile** (ambient motion/video reserved for
  larger/wifi); the hero light-drift is disabled < 640px. **Cellular-data guardrail —
  IMPLEMENTED (2026-07-11):** on phones (`max-width:640px` or coarse+short) only the **hero**
  crossfades and the two **hold-to-preview pause plates** keep their pair (the hold IS their touch
  feature, night layers lazy); every other `.shot-night` layer is `display:none` + `loading="lazy"`
  — hidden lazy images never intersect, so the evening set is **never fetched** on phones (index +
  gallery, hand-synced; verified by request-log in the rehearsal matrix). At night those frames
  keep their day layer visible via an opacity revert — don't remove it, or phones go blank at night.
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
  stays on `main` (the GitHub Actions workflows need it) but is excluded from the Pages output
  (`_config.yml`, 2026-11-03) and robots-disallowed.
- **Stale remote branches to delete (user-side).** **Ten** `claude/*` branches (checked 2026-11-16 via
  the GitHub MCP `list_branches` and `git ls-remote` — the 2026-11-03 note "one left" was wrong):
  `brand-assets`, `brevo-interest-form`, `exhibition-quickwins`, `materials-coast-palette`,
  `nav-active-highlight`, `nav-sync`, `optimistic-cerf-ahilv4`, `remove-root-originals`,
  `second-green-accent`, `woven-visual-placeholders` — all superseded by everything since
  (`optimistic-cerf-ahilv4` is the branch the fresh container keeps booting onto). Delete via the
  GitHub *Branches* UI — the proxy 403s git ref-deletions and the GitHub MCP tools have no
  delete-branch action. Done when they disappear from `git ls-remote`.
- **GitHub disables scheduled workflows after 60 days without a push (public repo).** A quiet
  autumn/winter needs one push before each 60-day mark or the fortnightly report silently stops
  (last push that reset the clock: 2026-11-20 → next mark 2027-01-19).

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
- **Physical brand — door mats: order specified (2026-11).** Eight custom logo mats from a Cypriot
  supplier (En Oiko Dimiourgies; qualities *Prado* = printed nylon 7 mm, *Azure* = vinyl loop).
  **Owner's final choice after checking the samples in real light (2026-11-16): Prado base Beige 2
  + logo Brown 12 · Azure base Beige + logo Brown · logo one colour incl. the dot, centred, 50 % of
  the mat width.** List:
  ENTRANCE-OUT 100×80 Azure · KITCHEN-OUT 70×60 Azure · VERANDA 200×100 Prado · ENTRANCE-IN 100×110
  Prado · BALCONY 1–3 100×60 Prado ×3 · BALCONY-IN 70×60 Prado. The one-page order sheet (EN), the
  research report and the colour measurements live in `docs/mats/` on `internal`. **Supplier's reply
  (2026-11-19) and the owner's answer:** (1) she advised reversing the Prado colours (Brown 12 base,
  dirt shows less) — *declined*: rendered on the real stone a brown base is a wine-red slab at
  3.4–4.6:1 against the floor, the object the owner had moved away from; the light base and its
  cleaning are accepted. (2) She strongly advised keeping the 2.5 cm edging on loose-laid mats
  (fraying, tearing) — *accepted*, which retires the "borderless if only black" rule: Azure edging
  in beige; Prado in beige if her supplier has it, otherwise brown to match the logo. (3) Prado on
  the veranda and balconies — the owner confirmed they are deeply covered and get no direct sun;
  Prado stays as ordered. (4) Final logo dimensions may vary slightly; proofs come for approval.
  The 12 mm sample fan was outdated — no thickness question. **Open:** the Prado edging colour,
  proofs, quotation. Brand logic used: gold stays the
  dot only and drowns on light grounds (≈1.2–1.7:1) → a one-colour mark; the wordmark comes from the
  logo file, never typeset. **Learnings:** (1) catalogue swatches mislead (the printed Prado green
  was far darker than the real yarn) — measure real samples from a photo **with a white sheet of
  paper in frame**: convert the phone's Display-P3 to sRGB, balance on the paper, compare mat and
  floor *within one photo*. (2) Pile looks darker in raking sun than in shade (self-shadowing): the
  same Light Grey 4 sat 1.1:1 on the travertine in shade and 1.6:1 in low sun. (3) The real
  travertine is a golden sand — as light as the palette token `#DCCDB3`, clearly more saturated
  (≈ `#DEC89D` measured); the token stays a design value. (4) The wordmark's strokes are 1.4–1.9 %
  of its width (stems 6.8 of 366.78 units): 7–9 mm at a 50 cm logo; published vinyl-loop inlay
  minima are 9.5–10 mm. (5) The supplier's "max one side 150 cm" caps the SHORT side (the price list
  runs to 150×300). (6) From the research: Cliff Tan's own published advice is not to put a mark you
  value on a doormat; a 7–9 mm borderless edge is above every trip threshold (ADA 6.4 mm, BG BAU
  4 mm), though nothing binds a private house; PVC-backed mats on porous stone want lifting to dry
  (weekly indoors, after rain outdoors).
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
  **Dress rehearsal LIVE (2026-07-11): every front-page photo slot + the gallery's chapter-I
  feature now carries a synthetic light study** — abstract Daylight/Afterglow compositions in the
  brand palette (matched pair geometry per slot; owner chose to deploy them live while the site is
  unpromoted). Generator: `scripts/gen-light-studies.py` (deterministic seeds; masters into the
  gitignored `images/_masters/`). **Intake pipeline: `scripts/process-photos.py`** — slot registry
  mirrors the brief's Appendix A; masters named `<slot>--day/--eve.*` (pairs) or `<slot>.*`
  (singles) → AVIF/WebP/JPEG sets with the exact filenames the pages reference. **The photo markup
  is FINAL: photography day = replace files, rerun the script, commit — no HTML edits** (runbook:
  `images/README.md`). Wired slots: hero pair (day = LCP, `fetchpriority=high`, both layers eager
  for the R4 night arrival), both pause pairs (hold-to-preview now flips real images), architecture
  plate pair, garden/interior single-hour plates, all 8 Views (3 pairs + 5 singles), and —
  since 2026-07-15 — the FULL gallery (all six chapters, 23 frames: 3 feature pairs incl.
  `gallery-approach`, 2 portrait + 18 further curated single-hour plates whose captions name
  their hour — own 11-check matrix green: trio/offset geometry, lightbox hours, phone
  guardrail); the establishing-film plate stays a labelled placeholder (it awaits
  footage, not a still). **Single-hour frames carry `hour-day`/`hour-eve`** — the label colour
  follows the IMAGE's register, not the theme (theme-following labels landed pale-on-pale /
  dark-on-dark, 1.0–1.7:1; with the classes all 16 label samples measure 5.5–8.5:1 in both hours —
  keep the classes when real photos land). **Rendering lessons from the studies:** additive glows
  clip R+G to acid green — lerp toward a warm colour instead (generator comments); and the
  `body.preview .hero-inner::before` text-wash must fade out INSIDE its box — its old stops were
  still translucent at the edge, drawing a seam over any real image (fixed; invisible over the flat
  placeholder it was designed on). The gallery **lightbox now opens the CURRENT hour's layer**
  (`.shot-night img` under `body.night` when visible; it always took the first = day img). Scales
  to ~20–30 photographs; once they land, consolidate woven vs. gallery to avoid duplication. **The full brief is `docs/imagery-brief.md`
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
  membership + SOURCE**, not separate databases. **The AJAX submit is LIVE since #15
  (2026-06-21)** — visitors stay on the page: `fetch` with `mode:'no-cors'` (opaque response =
  success; single opt-in, the inline thank-you is the receipt), honeypot re-checked, button
  swaps to "Sending…", success hides the form + focuses the `#register-thanks` block (the
  owner-approved completeness copy), genuine network failure shows the quiet `#register-error`
  line and re-enables; no-JS falls back to the native POST. Formally verified 2026-07-11
  (Playwright: success / failure / beacon coexistence — the `form-submit` beacon fires either
  way). A Brevo custom redirect is moot (no navigation happens).
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
  recipe: scratch HTML (night tokens + logo-white) → Playwright screenshot → JPEG q88. A
  hero-eve light-study backdrop was offered 2026-07-15 and left open — the logo-first interim
  stands; don't re-propose unprompted.
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
  Analytics** on the **1st & 15th** (≈ fortnightly) and on demand — since 2026-07-15 incl. an
  **Index-status section** (GSC URL Inspection: verdict / coverage / last crawl / canonical for
  `/`, `/legal/`, `/gallery/` + sitemap health + rich-results check; readonly scope suffices;
  `/gallery/` showing noindex/unknown is the intended state) **and, same day: brand-vs-discovery
  + image-search split (baseline before the photography), GSC country/device/daily, PSI for
  /gallery/ (its SEO score = the deliberate noindex, annotated in-report) + top Lighthouse
  suggestions, Cloudflare referrers + daily visits — since 2026-07-26 with **spike-day
  forensics** (outlier days ≥ max(2.5× median active day, 20) get a per-day
  referrer/country/path drilldown; ≤3 days per report) — a 404 watch, and a Brevo
  interest-list count.** Since **2026-08-12** the report also carries **trend deltas vs the
  previous report**: the workflow fetches the prior run's JSON artifact **in-memory**
  (workflow permission `actions: read` + `GITHUB_TOKEN` in the step env — the deliberate
  "nothing committed" stance stays true) and annotates GSC totals, Cloudflare visits/views
  (with a "sampled" hint), the Brevo count, plus an events **Δ-column vs all-time**; the
  report JSON stores only `trend_base` metadata, never the previous data (else every
  artifact would chain all history). **Artifact-download gotcha:** the zip endpoint
  302-redirects to signed blob URLs that reject the API Authorization header — the script
  follows the hop manually and fetches the signed URL bare. And an empty GSC query table
  beside real impressions now prints the honest "Google anonymizes rare queries" line
  (the old "No queries yet" misread as zero search activity). Verified end-to-end the same
  day: a control run against the same-morning base rendered every delta ±0 (correct, base
  minutes old) and the artifact fetch worked first try — the redirect handling matters.
  Since **2026-09-26** the events section also prints an **unattributed-`_hits` check**
  whenever the window gap is real: `_hits` counts EVERY /e request, and in September
  scanners found the endpoint (rolling total 186→295 while named events stayed ~flat), so
  the report now states "N of M window requests carry no allowlisted event name — route
  noise, not visitors". Read `_hits` as route pressure; the named rows are the human
  signal. **Window-only by design (same-day adversarial-review catch):** `_hits` keys
  expire after 60 days while named events keep 400, so lifetime sums cross retention
  horizons and don't compare — the first cut printed a mislabeled "all-time" pair whose
  negative gaps my comment blamed on launch history; the real cause is the TTL asymmetry.
  Any `_hits` "(all-time)" figure in the events TABLE is likewise a trailing ~60-day sum,
  and a `--days` > 60 window would truncate `_hits` the same way.
  **2026-11-03 (boot review) — the report now says what its numbers mean:** Cloudflare prints
  the sample interval and the retained-beacon count with an exact-Poisson 95 % band (every RUM
  figure since July is a multiple of 10 → 60 visits = 6 beacons ≈ 22–131; deltas are labelled
  "see the band"); the spike floor is **5 retained beacons** (was 20 visits = two beacons — the
  10-01 "+30" forensics were noise, and its "our own PSI run" NB did not survive arithmetic:
  p≈0.001); **report run days are marked ▸** in the visits-by-day line, never subtracted (the
  PSI self-hit hypothesis was tested 2026-11-03 with two on-demand runs = six Lighthouse loads:
  none registered as a visit, events ±0 — cross-check the 11-15 report for a late-ingested 11-03
  entry); the PSI block states the **Cyprus time of the lab loads and whether they fell into R4
  night** (written on the assumption that the two homepage loads would then count
  afterglow-auto +2 — observed otherwise on 2026-11-20: Lighthouse loads send no beacons, so the
  line is information only); GSC gets a **Homepage (brand proxy)** line — site totals mix in /legal/'s
  imprint-string matches (7 impressions at pos 29 dragged the average to 20.5 while the homepage
  sat at 5.5; "+2 impressions" hid a homepage drop 9→4) — and the brand split is annotated as
  query-filtered (Google omits anonymized queries under a query filter, so 0/0 beside real
  impressions means unattributable, not absent); the events column is **"new since <date>"**
  (named events: lifetime delta, exact until the first 400-day expiry ≈ 2027-08; `_hits`: summed
  from the day buckets after the previous report — the lifetime difference was inflow minus
  60-day expiry) with the `_hits` row labelled "60 d"; KV reads are counted (`N keys · M
  unreadable` — a 429 can no longer read as zero; the `_hits` "new since" starts from the previous
  run's reading of its own day bucket, so a same-day re-run prints the true inflow). `seo-pull.py` keeps `daily` buckets in the JSON
  (a few KB; `trend_base` stays metadata-only, now incl. `run_days`). Workflow: cron **05:37 UTC**
  (07:00 runs landed 5–7 h late in the :00 congestion; a December delay ≥ 7.7 h would have put the
  PSI loads into Cyprus night), actions on **v7** (Node 24 — checkout / setup-python /
  upload-artifact; the artifact REST read path is unaffected), pip step `continue-on-error` so a
  PyPI hiccup degrades Search Console instead of losing the report.
  Both owner setups landed the same night: **Brevo live** (key as `BREVO_API_KEY`
  secret, no IP allowlist — GitHub runners have none; list found, 0 subscribers = consistent
  with form-submit 0) and the **404 watch live** after a three-step token odyssey worth
  remembering: (1) the dashboard has TWO token areas — ours are ACCOUNT API tokens (My
  Profile → API Tokens is empty; identify the report token by "Last used"); (2) **"Account
  Analytics Read" is NOT "Zone Analytics Read"** — same-sounding groups, the policy's SCOPE
  (account vs zone resource) decides, so the zone permission needs its own zone-scoped policy
  block; (3) free-plan zones cap `httpRequestsAdaptiveGroups` at a **1-day query span** — the
  watch reads a 24h window (fortnightly spot-check). First reading: top-10 404s are pure
  scanner noise (`/wp-admin/install.php`, `/.env*`, `/.git/config`, aws configs — normal
  internet background, harmless on a static site), ZERO real broken site links. The report
  says "not checked" on errors, never a false "none". (Optional, owner's call, offered
  2026-07-15: slim the token to Workers Scripts/KV Write + Account & Zone Analytics Read —
  the edits left it broad; don't re-propose unprompted.) First run findings 2026-07-15: brand 9 /
  discovery 2 / **image search already 1** impression; GSC reach CY·GB·FI·GR·JO·NL·PK·PL;
  first organic referrers (google.com ×10, refseek.com ×10); PSI occasionally 500s on one
  strategy — transient, self-heals next run. emitting a dated report as a
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
  this scale. **Allowlist (19 since 2026-11-20 — `arrive` + `notice-close`, see the boot-2026-11-20
  section) in `scripts/cf-worker-events.js`:** `via-gate`/`via-sea`
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
  The worker also keeps a `_hits:<day>` heartbeat (counts EVERY request the route delivers, no
  name, 60-day TTL) — it appears in the report table; read it as route-level diagnostics, not as an
  event. **2026-11-03: `_hits` was 78 % scanner probes** — the route is `/e*`, so `/env`, `/ecp/…`
  landed in the worker, were counted and answered 204 (hidden from the 404 watch). **The worker
  source on `main` now handles only the exact `/e` path** (everything else `return fetch(request)`
  → GitHub Pages' branded 404, counted by the 404 watch) and try/catches the named put so the 204
  is unconditional. **DEPLOYED 2026-11-20 (owner: "ja, 1-4"; run #6 green — worker uploaded, the
  live route answered 204, the KV write was read back), together with the two funnel counters.**
  From now on `_hits` should fall toward the sum of the named rows and the 404 watch shows the
  `/e…` scanner probes. **That deploy's verification added one `afterglow`** — the script used to
  probe with a real event name, so `afterglow:2026-11-20 = 1` is the deploy, not a visitor (chosen
  evenings: 3, not 4). Fixed the same day: the probe now carries an unlisted name and only the
  `_hits` heartbeat moves. A GitHub-runner curl with a browser User-Agent does reach the worker
  (204), contrary to the older note below about curl probes. DNT is
  NOT a source of unattributed hits — an opted-out browser sends nothing (the page returns before
  `sendBeacon`). **Verification path:** curl/
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

## Site review 2026-10 (six-lens adversarial review; memo: internal:docs/site-review-2026-10.md)
- **Method that worked:** six reviewer lenses (code / function / aesthetic / copy / brand / seo) in
  parallel → one skeptic per finding instructed to refute + check CLAUDE.md decisions → a
  completeness critic over the modalities nobody touched (print, JS-off, blocked fonts, touch-hover,
  autofill, zoom). 34 → 32 confirmed, 1 settled, 1 refuted, +7 critic finds. Owner: "go for all".
- **Regression matrix lives in the repo now:** `scripts/verify-site.py` (~200 checks, ~2 min,
  self-serving; `--only <group>`, `--no-external`, artifacts to the temp dir). Run it after any
  change to the pages; it covers theme/R4/sweep/hold/menu/lightbox/WIP/form/beacons/guardrail/
  404/keyboard/static links/assets. The July scratchpad matrices were lost with a container.
- **Adversarial diff review before the push (same day):** five hunters over the batch diff found
  four real defects the targeted checks had missed — the touch `.more-link` underline rule was
  dead (a media query adds no specificity; the later base rule won → moved after it), the print
  block's `.mark` rule lost to `.bar .mark` and the Afterglow tokens printed pale (fixed above),
  the fallback font's vertical metrics were off after the size-adjust re-fit (see the lesson
  below), and the band's upper edge left a 4px mark/nav gap at 901px on touch (→ 940); a
  regressions hunter re-run against the FIXED tree then caught two more — the width-only band
  also hit landscape phones (→ scoped to where the nav shows) and printing with the WIP notice
  open still gave one truncated page (the inline body lock → released in print). Plus ~10
  stale doc/comment leftovers. **Rule: a batch that touches hand-synced blocks or the cascade
  gets a skeptic pass over the DIFF, not only the targeted checks — the matrix now carries print
  and band checks so these stay covered.** The gallery's hash arrival (`/gallery/#ch-…`) rests
  ~19px short of `scroll-margin-top` because the chapters are themselves `.reveal` boxes (the
  measurement is taken mid-transform) — pre-existing, matches native in-page navigation, left as-is.
- **Shipped (one batch, 2026-10-12):** phone-Afterglow pair-plate labels (were 1.4:1 — the
  guardrail shows the day layer, so the label now keeps the day register); gallery plates
  (`.plate picture{height:auto}` — pictures had swallowed the caption row; captions sat behind
  the next plate on phones); the **701–940 bar band** (see *How the site is built*); lightbox focus
  ring pale (#EEE7D6 — accent olive was 2:1 on the fixed-dark backdrop); Views `sizes` 620→760 and
  Materials 22vw→27vw; WIP `unlock()` honours an arrival fragment (deep links were lost; ×3
  byte-synced); honeypot-caught bots no longer count as `form-submit`; **a `@media print` block —
  the 4th hand-synced block across index/gallery/legal** (reveal visible, bar static, controls
  hidden, wordmarks as text, **Afterglow tokens handed back to Daylight via `--x:inherit` on
  `body.night`** — pale ink on white paper otherwise; the print selectors repeat the base rules'
  specificity, `.bar .mark` / `.wip[open]` / `.js .menu-btn`, so source order decides; and
  `body{ position:static !important; … }` releases the inline scroll-lock of an open notice /
  menu / lightbox — printing with the WIP card up gave ONE viewport-sized page otherwise; the
  hero photo is hidden in print — Chromium paginates the absolutely positioned hero image to a
  15px sliver under the bar, so the hero prints as text; Save-as-PDF was 13 blank pages); no-JS
  gating of toggle / hero chip /
  evening-lines / hold-hint (like the menu button); **hover-only rules wrapped in
  `@media (hover:hover)`** on all pages — touch no longer sticks a tapped submit button in its
  inverted state (the WIP block's hovers are left as-is to keep its byte-sync); autofill override
  (Chrome's light-blue tint — the one colour the guardrail forbids); `color-scheme` light/dark via
  `html:has(body.night)` so scrollbars / UA form chrome follow Afterglow; manifest `start_url` +
  `id`; `text-wrap: balance` on section titles + legal h1, `pretty` on `.note-source`; the touch
  `.more-link` underlines its text (the inline-block rule spanned the box under a wrapped link);
  404 honours a saved Afterglow (night tokens + white logo + saved-pref init; no R4 clock there);
  `--light-warm` held-value re-synced; dead `.measure`/`.hairline`/`.ph` CSS removed; stale
  comments fixed; **public view-source scrubbed** of the Brevo "other site"/list-name notes and
  of `docs/` paths (those live on `internal`); README refreshed (it was served on the brand
  domain until the 2026-11-03 `_config.yml` exclude); the outlook address scrubbed from this file. Copy (all owner-approved): four Oxford
  commas, "growing stiller floor by floor" (The plan), gallery chapter VI "Materials, close at
  hand" (matches the Iroko captions + both briefs), legal toggle wording, legal date.
- **Deliberately NOT done:** `.nojekyll` (would newly expose `.github/` and dotfiles on the
  domain) — **since 2026-11-03 the complementary lever is in: `_config.yml` with Jekyll `exclude:`
  keeps CLAUDE.md, README.md, images/README.md and `scripts/` out of the Pages output** (the repo is
  public, so this is domain hygiene, not confidentiality; robots.txt keeps its Disallow lines as
  belt-and-braces; `fonts/LICENSE.md` stays served for the OFL). The skeptic's Jekyll 3.10 build
  showed the Pages default plugins had ALSO been rendering **`/CLAUDE.html`** (optional-front-matter
  converts any `.md`) and **`/images/index.html`** (readme-index) — both gone with the exclude;
  Jekyll's default excludes are restated in the file because a user list replaces them; label type-size consolidation +
  worst-case label contrast (photography-day items); `prefers-reduced-data` guardrail. **Owner-side:** DARK Architectural Lighting's TLS certificate
  expired 21 Aug 2026 (their site; the credit link stays — a courtesy nudge); Cloudflare security
  headers (HSTS etc. via Transform Rules — Pages sets none); real-iOS + screen-reader passes.
- **Fallback-font lesson:** the July `size-adjust: 116.7%` for the LT Museum fallback was fitted
  over the whole glyph set, but the site sets LT Museum only UPPERCASE + tracked (tracking is in
  em and unaffected by size-adjust) — measured on the live strings the fallback over-set widths by
  up to 29%; re-fitted empirically against the page's own strings — **90%** (fallback/web width
  ratio 1.00–1.06 on nav, descriptor, tagline, eyebrows, labels; mean +2.4%, max +8.3%). **The
  ascent/descent overrides are percentages of the size-ADJUSTED em** (verified: 116.7% + 81.3/18.2
  matched the real 116px line at 100px; 90% with the same overrides gave 89px) — they were
  re-scaled together to **105.4% / 23.6%** (0.9 × 1.29 ≈ 1.161). Fit fallbacks against the
  strings actually set, not the font's average advance, and re-fit the vertical pair with it.

## Boot 2026-11-03 — data truths + optimisation review (memo: internal:docs/boot-2026-11-03.md)
- **Method:** six lenses over the 10-15 / 11-01 reports + the repo (measurement truth, performance,
  content, SEO, ops, first visit on a phone) → one skeptic per lens, refuting against CLAUDE.md and
  re-measuring → synthesis into A (safe today) / B (owner) / C (later). 13 agents; 25 proposals →
  7 shipped, 3 owner questions, the rest deferred or refuted. The sandbox has 4 CPUs → 2 concurrent
  agents; size workflows accordingly (one skeptic per lens, not per finding).
- **Data truths (keep reading the reports this way):** real traffic ≈ one arrival a day; since
  10-15 most arrivals no longer scroll (afterglow-auto +8 vs ch-place +2) — humans leaving at the
  notice or JS-running fetchers, indistinguishable with the current counters. Cloudflare is sampled
  1-in-10: 60 visits = 6 beacons (95 % ≈ 22–131) — **never read a delta or a "spike" below ~5
  beacons**. 78 % of `_hits` were `/e*` scanner probes (worker fix pending deploy). **afterglow-auto
  rises with the calendar, not with interest:** R4 keys to Cyprus wall-clock, sunset 14:54Z in
  November, two-thirds of the audience is North American → a US-Eastern working day is 89 %
  Afterglow (50 % in July); the evening is given 25× more often than chosen (75 vs 3, hold 0).
  /legal/ out-impresses the homepage via imprint strings (company name, HE number) — harmless.
  PSI 100×4 needs nothing: the 10-15 96 / SI 4.2 s and the 11-01 100 were the same commit (lab
  variance); **the mobile CLS 0.015 is one hero re-centre that only exists where neither Arial nor
  Liberation resolves** (the PSI host, every Android) — the orientation line wraps 22→45 px;
  0.0000 in 8/8 timing scenarios with a matched fallback, so the 10-12 re-fit is right. Mobile
  first view: 12 requests, 31 KB gz HTML + 101 KB (90 KB fonts); a third font preload and an
  eager first gallery plate were measured and rejected (noise).
- **Shipped (one push, 2026-11-03):** (A1) **scroll-reveal threshold** `0.16/0.12` → `threshold:0,
  rootMargin:'0px 0px -80px 0px'` on index + gallery — a ratio threshold left tall blocks (Views
  2,454 px) invisible on phones until 16 % of their height had scrolled in, i.e. 52–62 % of the
  screen blank under Materials; now every block reveals at 80–100 px visible (measured), desktop
  unchanged; (A2) `_config.yml` exclude (above); (A3) **`verify-site.py --only static` checks the
  seven hand-synced blocks byte-for-byte** (R4 init · theme-meta · font fallbacks · WIP CSS ·
  print block · WIP dialog · WIP IIFE; `SYNCED_BLOCKS` markers) — extend the dict when a new block is
  hand-synced; (A4) workflow housekeeping (above); (A5) the report-truth bundle (above); (A6) the
  worker source (deploy pending, above); (A7) `local('Arimo')` / `local('Tinos')` added to the two
  fallback src lists ×3 — metric clones of Liberation (same fit), spelled as family + full name +
  PostScript name (`'Arimo' / 'Arimo Regular' / 'Arimo-Regular'`) because CSS `local()` matches the
  latter two and the skeptic measured the bare family name matching nothing with a real Arimo
  installed; **do not add FreeSans/FreeSerif or DejaVu** (measured −4 % / +27 %).
- **ToDo B — owner decisions:** **B1 + B2 SHIPPED 2026-11-16** (owner: "mache 2 und 3"). B1: the WIP
  notice clause is now "the photography will follow" (was "is on its way", which predated the
  ~January deferral; byte-identical ×3). B2: the Views evening sentence ("Every view here keeps two
  hours — see the evening.") is hidden on phones via `#gallery p:has(> .evening-line){ display:none; }`
  inside the guardrail media query (index only) — its tap swept the page to Afterglow while 0 of 8
  Views changed; the interior's evening line stays (the hero and pause plates do answer it); the
  matrix carries a phone check + a desktop control. (Loading the evening layers on phones stays
  refuted: a photography-day decision.) **B3 DONE 2026-11-20** — deployed with the funnel counters
  (boot-2026-11-20 section).
- **ToDo C — later / owner-side:** studios backlink (Vardastudio, House Talks, Dear Modern) after
  the shoot (SEO-3); Cloudflare Cache Rule for /fonts/ (optional, ~1 visit/day: cold edge anyway;
  never a long browser TTL on same-path `images/`); ~~a `daylight-auto` twin (MT-7)~~ and ~~a
  Lighthouse-UA filter in the worker (MT-5)~~ — both closed 2026-11-20: `arrive` counts arrivals
  around the clock, and Lighthouse loads send no beacons; KV metadata read path or bulk-get
  (OPS-4b, ~950 keys ≈ late 2027); gallery lightbox on portrait phones — swipe, edge-to-edge
  image, arrows below the caption (FV-3, fold into the next gallery edit; `← The house` already has
  the quiet-link padding); Android fallback pair (`local('Roboto')` / `local('Noto Serif')` with their
  OWN measured size-adjust + overrides — needs a device that has them; Arial/Liberation never
  resolve on Android, so the swap re-centres the hero there); delete the ten stale `claude/*`
  branches (OPS-7, owner-side — see *Deploying a change*); DARK certificate · Cloudflare security headers · token scope (recorded, unchanged).
- **Refuted — don't re-raise:** interim rewrites of the Views/gallery stand-in disclosures (they are
  photography-day items, C-22; a direct /gallery/ entry sees the WIP notice first); the Register
  paragraph's conditional (left-as-is, PR #36); `/legal/` noindex; "first mobile 100" as a site
  change; afterglow-auto as "evening interest"; the PSI self-hit subtraction.
- **Lesson:** a measurement layer at this volume needs its resolution printed beside every
  number — the deltas, forensics and "all-time" pairs read as bookkeeping until the sample
  interval, the TTLs and the run days stood next to them.

## Boot 2026-11-16 — report 11-15, quick content + visual check
- **Report 11-15** (scheduled; **landed 7.3 h late** — 12:56 UTC for the 05:37 cron = 14:56 Cyprus,
  still Daylight): the :37 minute did not cure the delay — it is repo-level queueing. A December run
  delayed ≥ ~9 h would put the PSI loads into R4 night (the report then says so itself). *Optional,
  offered 2026-11-16:* move the cron ~3 h earlier — dropped 2026-11-20 (Lighthouse loads send no
  beacons, so a night run distorts nothing). PSI m98 / d100 / gallery 100, CLS 0.
  GSC 12 impressions / 0 clicks, homepage pos 4.2; the misspelling **"ethon house" now ranks at 3**
  (≈81 in September). Cloudflare 40 visits = ≈4 beacons (band 11–102), one www.google.com referral.
  Events since 11-03: **every chapter +3 and reach-register +3** — three readers started and all
  three read to the end (lifetime before: ~40 % of starters reached Register); consistent with the
  11-03 reveal fix, far too few to prove it. Brevo 0. `_hits` 335, of which 295 unattributed.
- **PSI self-hit cross-check closed:** the 11-15 visits-by-day line has no late 11-03 entry — the
  six Lighthouse loads of 11-03 never registered as visits.
- **Checks:** `verify-site.py` 225 PASS · 0 FAIL (DARK's expired certificate SKIPs; facebook.com can
  SKIP transiently — bot wall). Content read-through: no errors, only B1/B2 were stale (shipped the
  same day). Visual pass (phone + desktop × Daylight/Afterglow, gallery on the phone): clean.
- **DARK Architectural Lighting's certificate is still expired (since 21 Aug)** — a visitor who
  clicks the credit gets a browser warning. Offered 2026-11-16: unlink until fixed (the name stays
  as text). Undecided — don't act unprompted.
- **Screenshot gotcha:** Chromium truncates a `full_page` capture at 16,384 px. The desktop homepage
  is 18,448 px tall, so everything from *Register interest* down comes out blank — capture the lower
  part by scrolling (viewport tiles). Not a site defect.

## Boot 2026-11-20 — KPIs read as a funnel; the top of the funnel gets counted
- **Report 11-20 (on demand):** PSI m98 / d100 / gallery 100. GSC 14 impressions, **1 click (the
  first since July)**, homepage 9 impressions at 3.9; **Cyprus 7 impressions, 5 of them since 11-14,
  mostly mobile** — someone local is looking the house up. Cloudflare 40 visits = ≈4 beacons. Since
  11-15 one more complete read-through. Brevo 0. `_hits` 366, 319 unattributed.
- **The lifetime funnel (July → 11-20):** ch-place 36 → ch-architecture 24 → ch-plan 16 → … →
  reach-register 15. A third leaves in *The place*, another third in *The architecture*; whoever
  reaches the plans reads to the end. Since the 11-03 reveal fix 4 of 4 starters finished (11 of 32
  before) — suggestive, not proof, and some of those four are probably the owner. At least 82
  arrivals came in the house's evening alone, 36 ever began to read: the biggest loss sits between
  arriving and the first scroll, which the old counters could not see.
- **Phone walk (390 × 844):** the page is 18.2 screens; the first REAL image (the ground-floor plan)
  sits at screen 5.0 — before it the hero, ~430 words and two "forthcoming" stand-ins. Sections in
  screens: place 1.2 → architecture 2.4 → plan 4.4 → garden 6.3 → interior 7.8 → materials 9.7 →
  Views 12.0 → Register 14.9. **Shortening the opening stretch was NOT proposed for now** — the
  data is too thin and January's photography changes exactly this stretch; decide with clean numbers.
- **Shipped (one push; owner: "ja, 1-4"):**
  (1) the **▶ glyph on the establishing-film stand-in is gone** — a play control that played nothing
  sat in the first chapter; the plate and its label stay, the control returns with the footage
  (the `.play` CSS is kept for it).
  (2) **`?quiet=1` keeps the operator's own tab out of the counts.** It sets `window.name =
  'ae-quiet'` for the TAB — deliberately NOT localStorage: /legal/ lists every stored item ("two
  small functional notes … a session-only note"), and Safari evicts script storage after seven
  idle days, so a "set once" switch would silently lapse. The parameter is stripped, the status
  line under the bar says "This visit is not counted" (after the notice closes, if it is up), later
  loads in the same tab stay quiet, `?quiet=0` lifts it ("This visit is counted again"). **Owner
  habit: bookmark `aethon.house/?quiet=1` and open the site through it.** Cloudflare's own sampled
  visit count cannot be excluded this way.
  (3) **Two funnel counters:** `arrive` (every homepage load that runs the page script — people and
  script-running fetchers alike) and `notice-close` (the site notice closed by the visitor; a
  `close` listener in the beacon module, the hand-synced WIP IIFE is untouched). The report gained a
  **Reading funnel** block — every step incl. zero rows, each as "n of the step before", all rows
  on ONE time base (the window, or the days since `arrive` exists while it is younger than the
  window; before any `arrive` count it starts at ch-place). A return to the homepage within one
  visit arrives without a notice, so a row can exceed the one before. `robots.txt` now disallows
  `/e?` so compliant crawlers' renderers stay off the endpoint (Google recrawled the homepage on
  11-19 at 20:55 Cyprus time — a rendered crawl at night would count as `afterglow-auto`).
  The legal sentence on counters is generic ("a handful of … event counters … for instance"), so no
  notice change was needed; mention the two counters and the `?quiet` switch to counsel.
  (4) **Worker deployed** (the pending B3 — exact `/e` path + 19-name allowlist; run #6 green).
  The report on the new code (run #38) rendered the funnel block: no `arrive` yet, window
  ch-place 6 → ch-architecture 4 → … → reach-register 4, form-start 0.
- **Lighthouse loads send no beacons — observed again:** run #38's two homepage lab loads came
  minutes after the page with the unconditional `arrive` went live and left no `arrive` count
  (as on 11-03: six loads, events ±0). So a report run at Cyprus night would not count
  `afterglow-auto` either, and the idea of moving the cron earlier loses its reason; the report's
  Cyprus-time line stays as information. Re-check on 12-01: `arrive` must not jump on run days.
- **Matrix:** 9 new checks (arrive once, notice-close only when shown and closed, quiet tab incl.
  no storage written, lift, confirmation after the notice).
- **Gotcha — checking a third-party certificate from this sandbox:** a direct `ssl` socket to the
  host returned a valid certificate issued the same minute — the egress proxy's own interception
  certificate. The matrix's `--only external` check is the reliable one; by it **DARK's certificate
  is still expired** (unlink offer still undecided).
- **Still open / offered, undecided:** DARK link; Cloudflare security headers (owner-side).
- **Next session — read the 12-01 report for:** the first `arrive` / `notice-close` numbers (how
  many arrivals go past the notice — the question behind this whole change); `_hits` falling toward
  the sum of the named rows; `/e…` scanner probes now appearing in the 404 watch (expected); no
  `arrive` jump on the run day; and whether the owner's bookmark habit holds (a complete
  read-through on a day the owner looked is the tell). Door mats: the Prado edging colour, proofs
  and quotation are with the supplier.

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
  interim branded og:image. **07-11 refresh (pull ~90s after the rehearsal deploy):** Cloudflare
  **100 visits / 170 views per 28d**, /gallery/ 30 views (still all via homepage nav); "aethon"
  steady at pos 1.1; events — `_hits` 17, all 7 chapters ×2, reach-register 2, **afterglow-auto 3**
  (three no-preference arrivals after Paphos sunset opened in Afterglow — R4 observed in the
  wild); PSI desktop 100×4, mobile 97 (LCP 2.0s — ran before CDN caches settled). **07-15
  scheduled run (first full week of events): steady state confirmed** — PSI mobile 97 /
  desktop 100×4 WITH the studies live (LCP 2.0s, **CLS 0** — the ~30 images cost nothing
  measurable; the 97 remains the WIP dialog). Events: `_hits` 30 · all 7 chapters ×3 AND
  reach-register 3 (who arrives reads the whole portrait) · afterglow-auto 4 · afterglow 2 ·
  **first `hold` 1** (the gesture gets discovered unaided) · form-start 1. Cloudflare 110
  visits / 180 views per 28d, /gallery/ 30; "aethon" steady at pos 1.1. **07-26 on-demand
  pull (+ spike forensics shipped same day):** ~210 visits / 280 views per 28d — ~doubled
  in 11 days, driven by a **07-18/19 wave (50+30 visits)** the new drilldown attributes to
  **US · ~100% direct · homepage-only, one view per visit** — reads as a privately shared
  link making rounds (short glances, no gallery descent; a JS-running preview/AI-fetch
  fleet would look identical, though `afterglow-auto` jumping to 47/109 hits says the
  loads ran our JS at Cyprus-evening hours). First **bing.com referrals** (20 views) + 1 DE
  visit on 07-19. GSC: first organic click on "aethon" (pos 1.1, CTR 11%); garbled query
  "ainton sehou" = someone remembering the name. Brevo still 0; 404s pure scanner noise.
  Operational learnings: (a) **Cloudflare RUM adaptive sampling is unstable at this
  volume** — the same 28d range returned core totals 210/280 then 100/100 thirty minutes
  apart (the referrer table still summed 280); read counts directionally, never as
  bookkeeping. (b) The PSI flake can hit BOTH home strategies in one run (mobile timeout +
  desktop 500) while /gallery/ succeeds — still transient. **Open owner question: did
  someone share the link into a US circle around 07-18?** **08-12 pull (trend deltas
  shipped same day):** quiet plateau — the July wave was a one-off (140 visits/28d as it
  leaves the window; August = single ~10-visit days on 08-01/06/08, shallow: chapter-reach
  ~flat, register-reach +0). **First direct `/gallery/` entries** (10 visits landed there;
  was always 0 = homepage-nav only — someone shared or bookmarked the gallery link). GSC:
  since early July ALL reported queries are privacy-anonymized (a ~1/day impressions
  trickle continues, `/` at pos ~3.8 when shown; zero "aethon" queries in window — brand
  search is dormant, not derailed). PSI m96/d100×4 (lab noise, LCP 2.0 s steady); Brevo 0.
  **09-26 boot (six quiet weeks; workflow-extracted from the 08-15/09-01/09-15 scheduled
  runs + a fresh pull):** Cloudflare 130→50→30→30 visits/28d as the July wave left the
  window — the true unpromoted baseline is ~10 visits every week or two, all direct,
  US/DE-tinged (bot-adjacent; `similarpages.com` and `naver.com` appeared once each as
  referrers). GSC steady trickle (~15 impressions/28d, 0 clicks, all anonymized); the one
  named query is the misspelling **"ethon house" at pos ~81** (recurring since September —
  noted, not acted on; an `alternateName` for a typo is off-voice at 1 impression/window).
  **One thorough human reader ~09-24** (every chapter event +1 down to reach-register).
  `_hits` diverged from visitors (241 window vs ~17 named) → the unattributed-check
  feature above. /gallery/ keeps getting occasional direct entries. All four reports'
  trend deltas rendered correctly — the August feature holds in production.
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
  raw bytes for `/URI (…)` (or via pypdfium2), not with pypdf. **The system Pillow is broken the
  same way** (`from PIL import Image` → no `_imaging`; the sweep burst checks then SKIP as "needs
  Pillow") — `python3 -m pip install --ignore-installed pillow` puts a working one first on the
  path (2026-11-03); a fresh container also lacks `playwright`/`pypdfium2` — `pip install` both,
  never `playwright install`. Two more (2026-07-11): pip's
  `playwright` wants browsers newer than the preinstalled set — launch with
  `p.chromium.launch(executable_path='/opt/pw-browsers/chromium')`, never `playwright install`;
  and Playwright's URL globs need a `/` before the host segment — `**/sibforms.com/**` silently
  NEVER matches `https://06e3f483.sibforms.com/…` (dot before the host, not a slash), so the
  "mocked" request goes to the real network — route subdomain hosts with
  `re.compile(r"sibforms\.com")` instead.
- **Owner-side micro-todo:** on a real iPhone, glance at (a) the landscape overlay menu,
  (b) the dusk sweep + hold-to-preview, and (c) the live light studies (hero crossfade, a held
  pause plate, the Views grid — 2026-07-11 rehearsal). Chromium emulation is green everywhere;
  real iOS Safari unverified — Safari 18+ should run the sweep, older falls back to the crossfade.
- ~~Still open from the audit~~ **The audit is fully closed (2026-07-04):** every group-B and
  group-C item is decided and shipped (see the walkthrough block above + the memo's checkboxes).
  The only audit artefact still live is the **photography-day launch checklist** (strip
  "forthcoming" labels in the image commit; **write each frame's alt** — the stand-ins ship
  `alt=""`, a real photograph is content: runbook step 3 in `images/README.md`; re-sample
  text-over-photo contrast per frame; retire
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
  (R2) **Hold-to-preview** — `[data-hold]` paired views (the two pause plates) show the
  *opposite* hour while pressed: touch still-hold (200ms, >10px movement = scroll → cancels),
  mouse-hold, or holding Space/Enter (focusable, role=button). Since the 2026-07-11 rehearsal the
  pause plates hold REAL image pairs (light studies) — `.held` flips the actual layers; the token
  flip (`.shot-pair.held`, values hand-synced with `:root`/`body.night`) stays underneath as the
  loading/failure backdrop. **Cursor = the other hour's glyph** on fine
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
  → garden & terrace → western evening → the withdraw → materials) — since 2026-07-15 ALL 23
  frames carry light-study stand-ins via the `process-photos.py` registry (3 feature pairs +
  20 curated single-hour plates; chapter VI = band-motif material textures; the trio-lead CSS
  covers real `<picture>`s too); photography day swaps files only. The in-code SHOT BRIEF stays.
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
  statement. Linked from every footer (next to *Gallery*). Controller is a **company** — the
  imprint is **fully populated** (SIGNGUARD APP LTD, HE 492256, TIN, the Kissonerga office
  address marked "not the location of the residence", mail@aethon.house; the lawyer's pass
  still re-checks wording). Since 2026-10: sections carry ids (`#imprint` `#privacy` `#storage`
  `#content`, h2/h3 `scroll-margin-top`) and the form note links `/legal/#privacy`; the reading
  measure is 72ch (≈ 80 CPL, the memo's cap — was 92ch ≈ 110); the toggle is named
  "Daylight / Afterglow (day / night)"; typographic apostrophes; **bump the "Last updated"
  line whenever the notice text changes** (12 Oct 2026 now). The form links the privacy notice and the
  "never shared" line is corrected (Brevo named as processor). **No cookie banner** — only
  the functional day/night preference is stored (self-hosted fonts removed the Google CDN
  transfer). Indexable (unlike the gallery).
- **Renewal / origin (folded in):** the renovation story lives **inside *The architecture*** —
  no separate section, not in the nav. Its opening names the **Faros Beach Houses** origin and
  closes “Completed in 2026 … the same house, quietly raised.” No before/after imagery (no
  “before” photographs of the original house exist). The site is marketed only post-renovation,
  so it reads in the past tense, with no “under construction / owners away” implication.

## Still open (decide together — don't act unprompted)
- **Open ToDos from the 2026-11-03 boot review — see that section (B = owner decisions, C = later).**
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
  Esc/backdrop/←→, focus restore; **opens any plate** — `.lb-ph` is the no-image fallback panel); (6) **silent
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
  `<dialog>` opened **once per visit** — sessionStorage `aethon-wip`) tells a visitor the site is still
  being finished. Copy (owner-approved 2026-07-03, reworded from the original after the audit —
  "AETHON is finished; the *site* isn't"; **the clause changed 2026-11-16 from "is on its way" to
  "will follow"** once the shoot moved to ~January): *"This site is still being finished — the
  photography will follow. What you see is the shape of it; please, look around."* Blurred backdrop
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
  identity** are complete — and since the 2026-07-11 dress rehearsal the ENTIRE photo path is
  wired, tested and live on light-study stand-ins (crossfades, hold, lightbox, cellular guardrail,
  label registers). Commission the matched Daylight/Afterglow shoot per `docs/imagery-brief.md`
  (sent to Fynn 2026-07-11); integration is then a one-command file swap — see the runbook in
  `images/README.md` and the photography-day checklist (per-frame alt text, contrast re-check
  per frame, strip "forthcoming" labels, retire the WIP notice, re-run PSI). **Timeline decided (owner ↔ Fynn,
  2026-08-12): the shoot WAITS until ~January** — Fynn's professional advice is to let the
  freshly planted garden grow in and green up first (it currently reads dusty and new on
  camera). The light-study preview state is therefore the *intended* long-running state
  through autumn/winter; don't propose photography nudges, Fynn follow-ups or
  photography-day checklist items unprompted before the owner raises it (~Jan 2027).
