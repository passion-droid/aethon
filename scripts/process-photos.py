#!/usr/bin/env python3
"""
AETHON — photography intake (tooling, NOT part of the site).

The one command of photography day. Takes delivered master files, named by slot,
and emits every web asset the pages already reference — same names, same sizes —
so integrating the real photography changes FILES ONLY, never markup:

    images/_masters/hero--day.tif            (pairs:   <slot>--day.* + <slot>--eve.*)
    images/_masters/views-terrace.tif        (singles: <slot>.*)
    python3 scripts/process-photos.py

Per image: EXIF orientation honoured, colour managed to sRGB (embedded ICC respected),
centre-cropped to the slot's exact ratio, resized to the slot's widths, saved as
AVIF (q55) + WebP (q75) + progressive JPEG (q82) with ALL metadata stripped
(EXIF / GPS / timestamps — the masters folder itself is gitignored; never commit
originals, see images/README.md).

    --check         validate masters (presence, size, ratio drift) without writing
    --only a,b      process a subset of slots
    --masters DIR   masters folder (default images/_masters)

Slot registry mirrors docs/imagery-brief.md Appendix A (internal branch). Until the
real photography lands, scripts/gen-light-studies.py generates synthetic stand-ins
that flow through this same pipeline.
"""
import argparse
import glob
import io
import os
import sys

from PIL import Image, ImageCms, ImageOps

MASTER_EXTS = ("png", "jpg", "jpeg", "tif", "tiff", "webp")

# slot: (out_dir, ratio (w,h), widths (largest first), hours: pair|day|eve)
REGISTRY = {
    "hero":              ("images/hero",    (16, 10), (2400, 1600, 800), "pair"),
    "plate-living":      ("images/plates",  (16, 10), (1600, 800),       "pair"),
    "pause-west":        ("images/pause",   (16, 10), (2400, 1600, 800), "pair"),
    "pause-afterglow":   ("images/pause",   (16, 10), (2400, 1600, 800), "pair"),
    "plate-garden":      ("images/plates",  (16, 10), (1600, 800),       "day"),
    "plate-interior":    ("images/plates",  (16, 10), (1600, 800),       "eve"),
    "views-west":        ("images/views",   (21, 9),  (1600, 800),       "pair"),
    "views-living":      ("images/views",   (16, 10), (1600, 800),       "pair"),
    "views-pool":        ("images/views",   (16, 10), (1600, 800),       "pair"),
    "views-olives":      ("images/views",   (4, 5),   (1600, 800),       "day"),
    "views-olive-night": ("images/views",   (4, 5),   (1600, 800),       "eve"),
    "views-terrace":     ("images/views",   (16, 10), (1600, 800),       "day"),
    "views-interior":    ("images/views",   (16, 10), (1600, 800),       "eve"),
    "views-material":    ("images/views",   (3, 1),   (1600, 800),       "day"),
    "gallery-approach":  ("images/gallery", (21, 9),  (2400, 1600, 800), "pair"),
    # gallery chapters I (remainder) + II–VI — 2026-07-15 extension. Features are pairs;
    # everything else keeps one curated hour (captions name it: "after dark", "golden hour", …)
    "gallery-living":     ("images/gallery", (21, 9), (2400, 1600, 800), "pair"),
    "gallery-west":       ("images/gallery", (21, 9), (2400, 1600, 800), "pair"),
    "gallery-olives":     ("images/gallery", (4, 5),  (1600, 800), "day"),
    "gallery-cypress":    ("images/gallery", (4, 5),  (1600, 800), "day"),
    "gallery-lit-olive":  ("images/gallery", (3, 2),  (1600, 800), "eve"),
    "gallery-terrace-gold": ("images/gallery", (3, 2), (1600, 800), "eve"),
    "gallery-last-light": ("images/gallery", (3, 2),  (1600, 800), "eve"),
    "gallery-evening-glow": ("images/gallery", (3, 2), (1600, 800), "eve"),
    **{s: ("images/gallery", (3, 2), (1600, 800), "day") for s in (
        "gallery-threshold", "gallery-first-light", "gallery-dining", "gallery-kitchen",
        "gallery-pool", "gallery-terrace", "gallery-room-sea", "gallery-stair",
        "gallery-patiti", "gallery-travertine-leather", "gallery-iroko", "gallery-rosemary",
        "gallery-palette-hand", "gallery-coast-still")},
}


def to_srgb(im):
    """Honour rotation, then colour-manage to sRGB (respect an embedded ICC profile)."""
    im = ImageOps.exif_transpose(im)
    icc = im.info.get("icc_profile")
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            dst = ImageCms.createProfile("sRGB")
            return ImageCms.profileToProfile(im.convert("RGB"), src, dst)
        except Exception:
            pass  # damaged profile — fall through to a plain conversion
    return im.convert("RGB")


def centre_crop(im, rw, rh):
    w, h = im.size
    if w * rh > h * rw:                       # too wide — trim the sides
        nw = round(h * rw / rh)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w * rh / rw)                   # too tall — trim top/bottom
    y = (h - nh) // 2
    return im.crop((0, y, 0 + w, y + nh))


def emit(im, out_base, w, rh_over_rw):
    h = round(w * rh_over_rw)
    r = im.resize((w, h), Image.LANCZOS)
    r.save(f"{out_base}-{w}.avif", "AVIF", quality=55)
    r.save(f"{out_base}-{w}.webp", "WEBP", quality=75, method=6)
    r.save(f"{out_base}-{w}.jpg", "JPEG", quality=82, progressive=True, optimize=True)


def find_master(masters_dir, stem):
    for ext in MASTER_EXTS:
        hits = glob.glob(os.path.join(masters_dir, f"{stem}.{ext}"))
        if hits:
            return hits[0]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--masters", default="images/_masters")
    ap.add_argument("--only", default="", help="comma-separated slot names")
    ap.add_argument("--check", action="store_true", help="validate without writing")
    args = ap.parse_args()
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    missing, undersized, done = [], [], 0
    for slot, (out_dir, (rw, rh), widths, hours) in REGISTRY.items():
        if only and slot not in only:
            continue
        stems = [f"{slot}--day", f"{slot}--eve"] if hours == "pair" else [slot]
        for stem in stems:
            src = find_master(args.masters, stem)
            if not src:
                missing.append(stem)
                continue
            im = to_srgb(Image.open(src))
            im = centre_crop(im, rw, rh)
            need_w = widths[0]
            if im.size[0] < need_w:
                undersized.append(f"{stem} ({im.size[0]}px < {need_w}px after crop)")
                if args.check:
                    continue
            if args.check:
                print(f"  ok  {stem}  ->  {out_dir}/  {'x'.join(str(w) for w in widths)}w  {rw}:{rh}")
                continue
            os.makedirs(out_dir, exist_ok=True)
            # pair layers keep their hour in the name; single-hour slots ARE their hour
            base = stem.replace("--day", "-day").replace("--eve", "-eve")
            for w in widths:
                emit(im, os.path.join(out_dir, base), w, rh / rw)
            done += 1
            print(f"  {stem}  ->  {out_dir}/{base}-{{{','.join(str(w) for w in widths)}}}.{{avif,webp,jpg}}")

    # loud, explicit accounting — a silent gap here would surface as a broken slot live
    strays = []
    for f in glob.glob(os.path.join(args.masters, "*")):
        stem = os.path.splitext(os.path.basename(f))[0]
        slot = stem.replace("--day", "").replace("--eve", "")
        if os.path.isfile(f) and slot not in REGISTRY:
            strays.append(os.path.basename(f))
    if missing:
        print(f"!! no master for: {', '.join(missing)}")
    if undersized:
        print(f"!! undersized (upscaled unless --check): {'; '.join(undersized)}")
    if strays:
        print(f"!! masters not in the registry (ignored): {', '.join(strays)}")
    if not args.check:
        print(f"== {done} master(s) processed")
    if missing or undersized:
        sys.exit(2 if args.check else 0)


if __name__ == "__main__":
    main()
