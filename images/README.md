# images/ — site imagery & the optimisation process

Every photograph the site serves lives here, **pre-optimised**. The site itself has
**no build step** — these files are produced once (a quick authoring step) and
committed ready-to-serve. Nothing here runs at page load beyond the browser fetching
a small WebP.

Folders: `hero/` · `pause/` · `plates/` · `views/` · `gallery/` (the photo slots),
`materials/` (macro chips), `plan/` (floor renders), `sketch/` (the concept artifact).

## ⚠️ This is a public repo — never commit raw originals
Phone/camera files embed **EXIF GPS (the house's location)** and timestamps, and are
large. Committing them would leak location (against the brand guardrails) and bloat
history. So:

- **Drop master files into `images/_masters/`** (any of png/jpg/tif/webp) — it's
  `.gitignore`d and never committed. *Or* simply attach them in the Claude chat.
  (Material macros may also use the older `materials/_originals/`, equally ignored.)
- The pipeline **strips all metadata** and writes only the small web assets. **Only
  those get committed.**

## Photography day — the one command
Every photo slot on both pages is **already wired**; the markup is final. Integrating
the real photography changes **files only**:

1. Name each delivered master by its slot (list below): matched pairs as
   `<slot>--day.*` + `<slot>--eve.*`, single-hour slots as `<slot>.*`, and drop them
   into `images/_masters/`.
2. `python3 scripts/process-photos.py` (add `--check` first to validate presence,
   ratio and size without writing). Per image: EXIF orientation honoured, colour
   managed to sRGB (embedded ICC respected), centre-cropped to the slot's exact
   ratio, resized, saved AVIF q55 + WebP q75 + progressive JPEG q82, metadata
   stripped.
3. Commit the regenerated `hero/ pause/ plates/ views/ gallery/` files. Done — the
   pages pick them up by name.

| Slot | Where | Ratio | Hours |
|---|---|---|---|
| `hero` | hero, full viewport | 16:10 | pair |
| `plate-living` | The architecture | 16:10 | pair |
| `pause-west` / `pause-afterglow` | the two full-bleed pauses | 16:10 | pair |
| `plate-garden` | The garden | 16:10 | day |
| `plate-interior` | The interior | 16:10 | evening |
| `views-west` | Views, wide | 21:9 | pair |
| `views-living` / `views-pool` | Views | 16:10 | pair |
| `views-olives` | Views, tall | 4:5 | day |
| `views-olive-night` | Views, tall | 4:5 | evening |
| `views-terrace` / `views-interior` | Views | 16:10 | day / evening |
| `views-material` | Views, band | 3:1 | day |
| `gallery-approach` | /gallery/ chapter I feature | 21:9 | pair |

(The registry lives in `scripts/process-photos.py`; it mirrors the imagery brief's
Appendix A. **The gallery is fully wired too (2026-07-15)** — all six chapters, 23
frames: the features `gallery-approach` / `gallery-living` / `gallery-west` are 21:9
**pairs**; `gallery-olives` / `gallery-cypress` are 4:5 portraits; every other plate
is a 3:2 **single that carries its caption's hour** — evening for `gallery-lit-olive`,
`gallery-terrace-gold`, `gallery-last-light`, `gallery-evening-glow`, day for the
rest, incl. the chapter-VI material textures. Photography day covers them with the
same master-naming rules; nothing in `gallery/index.html` needs editing.)

**Until then: synthetic light studies.** `scripts/gen-light-studies.py` generates the
abstract Daylight/Afterglow stand-ins now live in every slot (brand palette only,
matched pair geometry, deterministic seeds) — they flow through the exact same
pipeline, so the whole photo path stays exercised. Two rendering rules learned from
them: **lerp glows toward a warm colour, never add** (additive light clips R+G to an
acid green), and **any text-backing wash must fade out inside its box** (a stop that
is still translucent at the edge draws a visible seam over real imagery).

**Single-hour slots carry `hour-day` / `hour-eve` on their `.frame`** — the label
colour follows the *image's* register, not the theme (a day image keeps its dark
label at night). Keep those classes when real photography lands, and re-check each
frame's label contrast per the photography-day checklist.

## What gets produced (per image)
| Property | Value |
|---|---|
| Formats | **AVIF → WebP → JPEG** fallback chain via `<picture>` — 6 files per image |
| Widths | `…-400.*` and `…-800.*` — the chip renders ≤ ~350px, so 800 covers 2× retina |
| Crop | uniform centre-crop to 3:2 landscape (800×533 / 400×267); `object-fit: cover` does the rest |
| Quality | AVIF q55 · WebP q75 (method 6) · JPEG q82 progressive |
| Colour | converted to sRGB |
| Metadata | **all stripped** (EXIF / GPS / timestamps) |
| Served | one format + size per visit (AVIF for modern, WebP for most, JPEG fallback), lazy-loaded — AVIF-800 for all eight ≈ 330 KB, far less at 400w |

### File names — slugs map 1:1 to the materials
`marble` · `venetian-plaster` · `travertine` · `coastal-sandstone` ·
`olive-leather` · `rosemary-green` · `dark-oak` · `iroko`
→ each as `-400`/`-800` × `.avif`/`.webp`/`.jpg`, e.g. `materials/marble-800.avif`.

## How the transform is run
**Option A — Claude runs it in-session (recommended):** attach the originals; Claude
runs the Pillow recipe below and commits only the WebPs.

**Option B — locally with ImageMagick** (no project install; run from `images/`):
```sh
magick marble.jpg -auto-orient -colorspace sRGB -strip \
  -gravity center -resize 800x -extent 800x533 -quality 75 -define webp:method=6 \
  materials/marble-800.webp
magick marble.jpg -auto-orient -colorspace sRGB -strip \
  -gravity center -resize 400x -extent 400x267 -quality 75 -define webp:method=6 \
  materials/marble-400.webp
```

**Option C — Squoosh.app** (browser, no install): Resize → 800 (then 400) wide ·
Format WebP · Quality 75 · tick *Strip metadata*.

## Reference recipe (Pillow) — what Option A runs
```python
from PIL import Image, ImageOps
def make(src, slug):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")   # honour rotation, force sRGB
    w, h = im.size                                                 # centre-crop to 3:2
    tw, th = (w, round(w / 1.5)) if w / h < 1.5 else (round(h * 1.5), h)
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w + tw) // 2, (h + th) // 2))
    for width in (800, 400):
        r = im.resize((width, round(width / 1.5)), Image.LANCZOS)   # no metadata written below
        r.save(f"materials/{slug}-{width}.avif", "AVIF", quality=55)
        r.save(f"materials/{slug}-{width}.webp", "WEBP", quality=75, method=6)
        r.save(f"materials/{slug}-{width}.jpg",  "JPEG", quality=82, optimize=True, progressive=True)
```

## Wiring into the page (done — Materials section)
Each `.mat-chip` colour span became a `<picture>` with AVIF/WebP `<source>`s and a
JPEG `<img>` fallback, keeping the brand colour as a load-time tint (visible while the
image lazy-loads, and if it ever fails):
```html
<picture>
  <source type="image/avif" srcset="images/materials/marble-400.avif 400w, images/materials/marble-800.avif 800w" sizes="(min-width:760px) 22vw, 45vw">
  <source type="image/webp" srcset="images/materials/marble-400.webp 400w, images/materials/marble-800.webp 800w" sizes="(min-width:760px) 22vw, 45vw">
  <img class="mat-chip" src="images/materials/marble-800.jpg"
       srcset="images/materials/marble-400.jpg 400w, images/materials/marble-800.jpg 800w"
       sizes="(min-width:760px) 22vw, 45vw"
       width="800" height="533" loading="lazy" decoding="async"
       alt="Marble — the cool ground, underfoot" style="background:#E9E7E0">
</picture>
```
plus `.mat-chip{ object-fit: cover }` for the image. Width/height reserve space to
avoid layout shift (CLS). The browser downloads exactly one source.

## Floor plans (`plan/`) — a different recipe
Unlike the 3:2 material chips, the floor renders keep their **full √2 ratio (no crop)** at
**800w / 1600w**, are **muted into the stone/olive palette** with the **pool's blue collapsed
to pale water** (the no-blue guardrail), and keep their **transparent margin** so the plan
floats on the page's `--bg-soft` and adapts to Daylight/Afterglow — AVIF + WebP carry alpha; the
JPEG fallback is flattened on the day stone. Reproducible:
```sh
pip install pillow numpy
python scripts/process-plan.py          # reads plan/<Ground|First>-floor_4K.png masters
```
Outputs overwrite `plan/{ground,first}-floor-{800,1600}.{avif,webp,jpg}` — the exact files
`index.html` already references, so no markup change. The 4K masters are **not** committed.
