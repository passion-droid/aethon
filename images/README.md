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
| Format | WebP (universally supported; one `<img>`, no fallback markup needed) |
| Widths | `…-400.webp` and `…-800.webp` — the chip renders ≤ ~350px, so 800 covers 2× retina |
| Crop | centre-crop to 3:2 landscape (800×533 / 400×267); `object-fit: cover` does the rest |
| Quality | WebP q75, method 6 |
| Colour | converted to sRGB |
| Metadata | **all stripped** (EXIF / GPS / timestamps) |
| Typical size | ~20–45 KB @800w · ~8–15 KB @400w (≈ <300 KB for all eight, lazy-loaded) |

### File names — slugs map 1:1 to the materials
`marble` · `venetian-plaster` · `travertine` · `coastal-sandstone` ·
`olive-leather` · `rosemary-green` · `dark-oak` · `iroko`
→ e.g. `materials/marble-800.webp`, `materials/marble-400.webp`.

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
        im.resize((width, round(width / 1.5)), Image.LANCZOS) \
          .save(f"materials/{slug}-{width}.webp", "WEBP", quality=75, method=6)  # no metadata written
```

## Wiring into the page (done after the assets land)
Each `.mat-chip` colour span becomes an `<img>`, keeping the brand colour as a
load-time tint (visible while the WebP lazy-loads, and if it ever fails to load):
```html
<img class="mat-chip" src="images/materials/marble-800.webp"
     srcset="images/materials/marble-400.webp 400w, images/materials/marble-800.webp 800w"
     sizes="(min-width: 760px) 22vw, 45vw"
     width="800" height="533" loading="lazy" decoding="async"
     alt="Marble — the cool ground, underfoot" style="background:#E9E7E0">
```
plus `.mat-chip{ object-fit: cover }` for the image. Width/height are set to reserve
space and avoid layout shift (CLS).
