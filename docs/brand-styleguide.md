# AETHON brand styleguide (Oli, delivered 2026-06)

Captured from `AETHON_STYLE_GUIDE.pdf` (kept alongside this file in `docs/`). This is the
designer's authoritative brand sheet. Where it differs from the site's existing palette/voice
rules in `CLAUDE.md`, those differences are **flagged below** — to be reconciled with the owner,
not silently overwritten.

> **Status — wired across all four pages (2026-06).** LT Museum is now `--ff-display`; the logo
> image-replaces the header mark, hero wordmark and footer mark (day = dark + gold dot, night =
> white + gold dot, footer = whiteout); favicon set + `site.webmanifest` shipped. **Gold decision:
> logo-only** (UI accent stays green). Masters removed — only the served assets are committed.
> **Both weights wired:** LT Museum **Medium** for nav/labels, **Bold** for the section eyebrows.
> Favicon uses Oli's **square** "A" icon — a crisp `icon.svg` SVG favicon + maskable app icons.

---

## Logo
- The **AETHON** logotype, set in **LT Museum**: letters in **olive (#4C5039)** with a single
  **gold dot (#C1A152) over the "O"** — the signature detail. Distinctive low-crossbar "A".
- Delivered as **SVG** (main logo) + a **whiteout** version (for dark grounds, e.g. the footer).
- **Header use:** replaces the current CSS text wordmark (owner-confirmed). Needs a
  Daylight/Afterglow treatment — the SVG should adapt (swap fills, or `currentColor` if mono;
  but note it is **two-colour**, olive + gold, so a simple `currentColor` won't carry the dot —
  likely a day SVG + a night/whiteout SVG, or CSS-tinted `<svg>` inline).

## Icon
- The **"A" monogram** alone (the logo's A). Basis for the **favicon / app icon**.

## Type — LT Museum
- **LT Museum**, weights **Medium + Bold**. A display/titling face (museum-style caps).
- **Role:** the brand **display** face → replaces **Jost** (`--ff-display`). **Spectral** (the body
  serif, `--ff-text`) is **not** addressed by the guide, so it **stays** for body copy unless the
  owner says otherwise.
- **Self-hosting:** convert the supplied `.ttf` → latin-subset `woff2`, `@font-face` across all four
  pages, no CDN (matches the existing Jost/Spectral setup). **License check required** — embedding
  via `@font-face` needs web rights; confirm from the font EULA / that LT Museum was licensed for
  web. ("LT" = LinoType-style naming — likely a foundry face, so this matters.)

## Colours
| Role | HEX | RGB | 60% tint | 20% tint |
|---|---|---|---|---|
| **Gold** | `#C1A152` | 193 161 82 | `#DAC797` | `#F3ECDC` |
| **Olive** | `#4C5039` | 76 80 57 | `#949688` | `#DBDCD7` |
| **Warm black** | `#222216` | 34 34 22 | `#7A7A73` | `#D3D3D0` |

Tints are the colour mixed toward white (60% / 20% ink strength).

### Reconciliation with the current site palette (`CLAUDE.md`)
The guide is a **brand-mark palette** (logo, type, accents) — it does **not** include the site's
**material/background** tones (Marble `#E9E7E0`, Travertine `#DCCDB3`, Sandstone `#C7B08C`, …),
which are drawn from the house and remain the page grounds. The three guide colours map onto the
**brand/ink/accent** layer:
- **Olive `#4C5039`** ≈ the current green accent `#565B3B` (the guide's is a touch darker/greyer).
- **Warm black `#222216`** ≈ the current ink `#2C2620` (the guide's is darker, more olive-black).
- **Gold `#C1A152`** is **new** — the current brand is **green-accent-only** (`CLAUDE.md`: "one
  accent colour only — green … never a blue accent"). Gold enters at minimum via the **logo dot**.

### DECISION (resolved) — gold travels **logo-only**; the options considered were:
1. **Logo only** — gold lives only in the logo dot + favicon; the site keeps its green UI accent
   (links/buttons) and stone palette unchanged. *Safest; smallest change.*
2. **Gold as a second accent** — green stays the UI accent, gold used sparingly for special
   marks/details (rules, the dot motif). *Hybrid.*
3. **Gold as the primary accent** — gold replaces green for links/buttons (a luxe, brass-on-stone
   shift). *Largest change; needs an AA contrast pass — gold on marble is low-contrast.*

And separately: **adopt the guide's exact olive/black** (`#4C5039` / `#222216`) into the
`--accent` / `--ink` tokens, or keep the current `#565B3B` / `#2C2620`? (They're close; the guide
values are slightly deeper.)

## Spacing (logo lock-up)
- **1X** = the diameter of the gold dot (the unit).
- **2X** clear-space on all sides of the logo (minimum margin before other elements). Honour this
  when placing the header/footer logos.

---

## Wiring plan (once assets land + decisions made)
1. **Font:** `.ttf` → `fonts/lt-museum-*-lt.woff2` (subset), `@font-face` + metric fallback ×4 pages,
   `--ff-display: "LT Museum", …`.
2. **Header:** inline the main logo SVG into the wordmark slot (44px tap target reserved), with a
   day/night treatment.
3. **Footer:** the whiteout logo SVG replaces the text foot-mark.
4. **Favicon:** from the "A" icon — `favicon.ico` + 16/32 PNG + `apple-touch-icon` (180) +
   `site.webmanifest`, `<link>`s ×4 pages, self-hosted.
5. **Palette:** apply per the open-decision answers; if gold becomes a UI accent, run a WCAG AA
   contrast pass on stone grounds.
