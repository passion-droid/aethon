#!/usr/bin/env python3
"""Process Cliff Tan's concept sketch into the site's stone palette — UNCROPPED.

The sketch is a pencil perspective of the ground floor that gathers (Cliff Tan,
Dear Modern). It is an *artifact*, not a technical drawing, and the full original
must not be cut — so this keeps the whole frame (no crop), only:
  • honours rotation, forces sRGB, strips all metadata (EXIF),
  • cleans the paper and deepens the graphite (autocontrast),
  • tones it into the palette as a warm graphite duotone (ink -> warm paper),
    so it sits with the muted floor plans rather than reading as a phone photo,
  • writes AVIF/WebP/JPEG at two widths for a <picture> (no upscaling past native).

Run from the repo root:  python3 scripts/process-sketch.py
Raw master lives only locally / in chat — it is not kept in the public tree.
"""
from PIL import Image, ImageOps
import os

SRC = "Cliff-Tan_sketch.jpg"
OUT = "images/sketch"
SLUG = "ground-floor-sketch"

# Palette anchors (from CLAUDE.md): ink (dark oak), a warm greige mid, marble-soft paper.
INK   = (44, 38, 32)     # --oak  #2C2620
MID   = (150, 140, 124)  # warm greige
PAPER = (240, 238, 232)  # --bg-soft #F0EEE8

os.makedirs(OUT, exist_ok=True)

im = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")   # rotation + sRGB
g  = ImageOps.grayscale(im)                                    # pencil is monochrome
g  = ImageOps.autocontrast(g, cutoff=0.6)                      # clean paper, deepen line
duo = ImageOps.colorize(g, black=INK, white=PAPER, mid=MID)    # tone into the palette

w, h = duo.size                                                # native 1264 x 917 — no crop
for width in (1264, 800):
    if width >= w:
        r = duo                                                # never upscale past native
        width = w
    else:
        r = duo.resize((width, round(h * width / w)), Image.LANCZOS)
    base = f"{OUT}/{SLUG}-{width}"
    r.save(base + ".avif", "AVIF", quality=60)                 # fresh save = no metadata
    r.save(base + ".webp", "WEBP", quality=78, method=6)
    r.save(base + ".jpg",  "JPEG", quality=85, optimize=True, progressive=True)
    print(f"  wrote {base}.(avif|webp|jpg)  {r.size}")

print("done — uncropped, toned, metadata stripped.")
