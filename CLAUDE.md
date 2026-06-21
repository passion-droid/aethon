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
- Philosophy: Bauhaus discipline · Japandi emptiness · Feng Shui balance ·
  Mediterranean warmth. Less, but better.

## How the site is built
- The whole site is one self-contained file: **`index.html`** — HTML, CSS (in a
  `<style>` block), and a little JavaScript (in a `<script>` block).
- **No build step, no framework, no dependencies, no package manager. Do not
  introduce any.** Do not split the CSS or JS into separate files unless explicitly asked.
- Fonts load from Google Fonts at runtime (Jost + Spectral). Everything else is local.

## Deploying a change
- Hosted free on **GitHub Pages**, served from the **`main`** branch, root folder.
- A change goes live ~1–2 minutes after it is committed and pushed to `main`.
  So the loop is: edit `index.html` → commit with a short message → push to `main`.

## Brand guardrails — always keep
- **Name system:** the brand is `AETHON` (used alone for premium/physical use); the
  descriptor line is `AETHON House · Paphos`. Pronounced “AY-thon”.
- **Tagline:** “house of light”. **Hero line:** “A sanctuary built around sunsets,
  silence, and the western sea.” Do not rewrite these unless asked.
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
- **Feng Shui is foundational:** Feng Shui ordered the plan (the design basis). Express it as principle.

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
  *The garden* / *The interior*, the two conceptual floor plans, and the eight-slot
  *Views* gallery (in-code shot brief). Scales to ~20–30 photographs; once they land,
  consolidate woven vs. gallery to avoid duplication.
- **Floor plans:** a conceptual *Plan* section (ground + first-floor placeholders) now
  sits after *The architecture*; awaiting the redrawn, low-detail artwork.
- **Credits:** **done.** The colophon credits the full team with linked company sites
  (olive, underlined, new tab) — Original architecture: Vardastudio (Andreas Vardas);
  Renovation: G. Patsalides Construction & Renovation (Georgios Patsalides); Interior:
  House Talks Interiors (Vicky Savva); Landscape: Antoine Garden Design & Construction
  (Antoine Hadjialexandrou); Lighting: DARK Architectural Lighting; Feng Shui: Dear
  Modern (Cliff Tan).
- **Interest form:** wired to **Brevo** — `action="https://sibforms.com/serve/YOUR_BREVO_FORM_ID"`
  (replace with the real serve ID once the Brevo form exists). Native POST, no API key
  exposed. Submissions go to a dedicated **"AETHON — Interest"** list with a hidden
  `SOURCE=aethon.house` tag, kept separate from the owner's *other* Brevo site; visible
  fields map to attributes `FIRSTNAME` / `EMAIL` / `MESSAGE`, honeypot `email_address_check`.
  Note Brevo's contact DB is global (unique by email) — separate AETHON interest by **list
  membership + SOURCE**, not separate databases. Optional polish: AJAX submit to stay
  on-page, and a Brevo custom redirect back to the site.
- **Domain:** `aethon.house` is connected (a `CNAME` file is on `main`); the site uses it
  as the canonical / Open Graph URL.

## Decided / planned
- **Floor plans:** included as a conceptual *Plan* section after *The architecture* —
  redrawn, atmospheric, low-detail only (placeholders in now; awaiting redrawn assets).
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
- **Gallery subpage:** a deeper photo-essay at `/gallery/` (`gallery/index.html`) —
  self-contained, **noindex**, **not** in the main nav; reached only by understated links
  at the end of *Views* and in the footer. Six chapters (Arrival → the ground that gathers
  → garden & terrace → western evening → the withdraw → materials) with labeled placeholder
  slots + a SHOT BRIEF; awaiting images via the pipeline (800w/1600w into `images/gallery/`).
  Buildless, so its `<style>` mirrors index.html's tokens **by hand — keep them in sync**.
  A quiet lightbox can be added once images land.

## Still open (decide together — don't act unprompted)
- Current section order (established): Hero → The place → The architecture → The plan →
  The garden → The interior → Materials → Views → Register interest → Credits.
- Floor plans and credits placement — **decided:** the *Plan* sits after *The
  architecture*; *Credits* is a colophon before the footer.
- **Hero motion / a short film** — slots are now in place (a hero ambient-loop and an
  establishing-film plate in *The place*, each marked with a ▶ affordance); whether to
  actually commission them is pending footage and the photo/video brief.
