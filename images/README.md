# images/ — site imagery & the optimisation process

Every photograph the site serves lives here, **pre-optimised**. The site itself has
**no build step** — these files are produced once (a quick authoring step) and
committed ready-to-serve. Nothing here runs at page load beyond the browser fetching
a small WebP.

Folders scale to the rest of the page later (`hero/`, `views/`, …). First up:
**8 macro close-ups for the Materials section** — one per material → `materials/`.

## ⚠️ This is a public repo — never commit raw originals
Phone/camera files embed **EXIF GPS (the house's location)** and timestamps, and are
large. Committing them would leak location (against the brand guardrails) and bloat
history. So:

- **Drop raw files (any format / size / resolution) into a local `materials/_originals/`
  folder** — it's `.gitignore`d and never committed. *Or* simply attach them in the
  Claude chat.
- The transform **strips all metadata** and writes small **WebP** files into
  `materials/`. **Only those get committed.**

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
