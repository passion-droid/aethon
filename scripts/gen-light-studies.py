#!/usr/bin/env python3
"""
AETHON — synthetic light studies (tooling, NOT part of the site).

Generates the abstract Daylight / Afterglow placeholder images that stand in every
photo slot until the real photography lands: quiet coastal-light compositions drawn
purely from the brand palette (warm stone, pale gold, olive — NEVER blue). Matched
pairs share one geometry (horizon, sun position, motif) and differ only in register,
exactly like the locked-tripod day/evening pairs the imagery brief asks for — so the
site's crossfade, hold-to-preview and lightbox can be exercised for real.

Deterministic (fixed seeds): masters are NOT committed — regenerate any time with
    python3 scripts/gen-light-studies.py --out <dir>
then feed them to scripts/process-photos.py, which emits the web assets the pages
reference. Slot names here match the registry in process-photos.py (imagery brief
Appendix A).
"""
import argparse
import os

import numpy as np
from PIL import Image

# palette (CLAUDE.md — exact site values)
MARBLE      = (233, 231, 224)   # E9E7E0
MARBLE_LT   = (240, 238, 232)   # F0EEE8
TRAVERTINE  = (220, 205, 179)   # DCCDB3
SANDSTONE   = (199, 176, 140)   # C7B08C
GREIGE      = (140, 132, 120)   # 8C8478
OAK         = (44, 38, 32)      # 2C2620
GLOW_DAY    = (242, 221, 190)   # F2DDBE (--light-glow, day)
GLOW_EVE    = (243, 200, 134)   # F3C886 (--light-glow, night)
AMBER       = (233, 172, 99)    # E9AC63 (--light-warm, night)
NIGHT_HI    = (58, 49, 42)      # 3A312A (night frame-grad top)
NIGHT_MID   = (44, 38, 32)      # 2C2620
NIGHT_LO    = (33, 26, 20)      # 211A14


def _ramp(h, stops):
    """Vertical ramp: stops = [(y0, rgb), …] -> (h,3) float array."""
    ys = np.array([s[0] for s in stops], float)
    cols = np.array([s[1] for s in stops], float)
    t = np.linspace(0.0, 1.0, h)
    out = np.empty((h, 3))
    for c in range(3):
        out[:, c] = np.interp(t, ys, cols[:, c])
    return out


def _gauss(xx, yy, cx, cy, sx, sy):
    return np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2))


def study(w, h, register, motif="horizon", horizon=0.58, sunx=0.68, seed=7,
          glow=1.0):
    """One abstract coastal light study as an RGB uint8 array."""
    rng = np.random.default_rng(seed)
    yy, xx = np.meshgrid(np.linspace(0, 1, h), np.linspace(0, 1, w), indexing="ij")
    day = register == "day"

    if motif == "band":
        # close raking-light texture — pressed lime / travertine ridges, no horizon
        base = _ramp(h, [(0.0, TRAVERTINE), (1.0, SANDSTONE)])[:, None, :] * np.ones((h, w, 3))
        diag = xx * 2.2 + yy * 0.9
        ridges = (np.sin(diag * 34 + rng.uniform(0, 6)) * 0.5
                  + np.sin(diag * 89 + rng.uniform(0, 6)) * 0.22)
        shade = 1.0 + ridges[..., None] * 0.055
        img = base * shade
        light = _gauss(xx, yy, 0.18, 0.25, 0.9, 0.7)[..., None] * np.array(GLOW_DAY)
        img = img + light * 0.10
    else:
        if day:
            stops = [(0.0, MARBLE_LT), (max(horizon - 0.16, 0.05), MARBLE),
                     (horizon, TRAVERTINE), (min(horizon + 0.05, 0.98), TRAVERTINE),
                     (0.9, SANDSTONE), (1.0, tuple(c * 0.92 for c in SANDSTONE))]
        else:
            stops = [(0.0, NIGHT_LO), (max(horizon - 0.2, 0.05), NIGHT_HI),
                     (horizon, NIGHT_MID), (0.9, NIGHT_LO),
                     (1.0, tuple(c * 0.8 for c in NIGHT_LO))]
        img = _ramp(h, stops)[:, None, :] * np.ones((h, w, 3))

        # the western glow — day: high pale gold; afterglow: low, amber, sun below horizon.
        # Day blends by lerp, not addition — an additive glow on the pale marble base clips
        # to a hard white disc; lerping toward the glow colour stays a quiet warm lift.
        if day:
            g1 = _gauss(xx, yy, sunx, horizon - 0.10, 0.34, 0.30)
            g2 = _gauss(xx, yy, sunx, horizon - 0.02, 0.10, 0.05)
            a = np.clip((g1 * 0.55 + g2 * 0.25) * glow, 0, 0.85)[..., None]
            img = img * (1 - a) + np.array(GLOW_DAY) * a
            a2 = np.clip(g2 * 0.45 * glow, 0, 0.6)[..., None]
            img = img * (1 - a2) + np.array((252.0, 248.0, 240.0)) * a2
        else:
            # lerp, never add: an additive glow clips R and G to 255 in the core and the
            # amber turns acid green — the same clipping trap as the day glow
            g = _gauss(xx, yy, sunx, horizon, 0.42, 0.10) * 0.85 \
                + _gauss(xx, yy, sunx, horizon - 0.05, 0.75, 0.30) * 0.30
            a = np.clip(g * 0.62 * glow, 0, 0.9)[..., None]
            img = img * (1 - a) + np.array(AMBER) * a
            core = np.clip(_gauss(xx, yy, sunx, horizon, 0.10, 0.035) * 0.5 * glow, 0, 0.7)[..., None]
            img = img * (1 - core) + np.array(GLOW_EVE) * core

        # water shimmer below the horizon — horizontal streaks; a warm column at night
        sea = yy > horizon
        streak = rng.normal(0, 1, (h, 1)) * np.ones((h, w))
        streak = streak * _gauss(xx, yy, sunx, horizon + 0.1, 0.5 if day else 0.16, 0.22)
        img += (sea * streak)[..., None] * (np.array(GLOW_DAY if day else AMBER)) * 0.045

        if motif == "verticals":
            # soft cypress verticals rising from the foreground
            for i in range(3):
                cx = 0.2 + 0.28 * i + rng.uniform(-0.05, 0.05)
                trunk = _gauss(xx, yy, cx, 1.0, 0.016 + 0.008 * rng.random(), 0.62)
                tone = np.array((107, 99, 80)) if day else np.array((16, 12, 9))
                a = 0.5 if day else 0.75
                img = img * (1 - (trunk * a)[..., None]) + tone * (trunk * a)[..., None]
        elif motif == "glowpool":
            # one warm pool of light in a dark field — the lit olive / the lit room (lerp, as above)
            g = _gauss(xx, yy, sunx, 0.62, 0.20, 0.16) * 1.0 \
                + _gauss(xx, yy, sunx, 0.62, 0.09, 0.07) * 0.8
            a = np.clip(g * 0.75, 0, 0.92)[..., None]
            img = img * (1 - a) + np.array(AMBER) * a
            core = np.clip(_gauss(xx, yy, sunx, 0.60, 0.045, 0.035) * 0.55, 0, 0.6)[..., None]
            img = img * (1 - core) + np.array(GLOW_EVE) * core

    # gentle corner vignette + fine grain against banding
    vin = 1.0 - 0.10 * (((xx - 0.5) ** 2 + (yy - 0.5) ** 2) * 1.6)
    img *= vin[..., None]
    img += rng.normal(0, 1.7, (h, w, 3))
    return np.clip(img, 0, 255).astype("uint8")


# slot -> (motif, horizon, sunx, seed, glow); geometry is shared by a pair's two hours
COMPOSITIONS = {
    "hero":            ("horizon",   0.60, 0.66, 11, 1.00),
    "plate-living":    ("horizon",   0.55, 0.74, 21, 0.90),
    "pause-west":      ("horizon",   0.62, 0.58, 31, 1.00),
    "pause-afterglow": ("horizon",   0.56, 0.70, 41, 1.10),
    "plate-garden":    ("verticals", 0.60, 0.30, 51, 0.85),
    "plate-interior":  ("glowpool",  0.55, 0.46, 61, 1.00),
    "views-west":      ("horizon",   0.58, 0.63, 71, 1.00),
    "views-living":    ("horizon",   0.52, 0.78, 81, 0.85),
    "views-pool":      ("horizon",   0.66, 0.52, 91, 0.95),
    "views-olives":    ("verticals", 0.64, 0.24, 101, 0.80),
    "views-olive-night": ("glowpool", 0.58, 0.52, 111, 1.00),
    "views-terrace":   ("horizon",   0.57, 0.40, 121, 0.90),
    "views-interior":  ("glowpool",  0.55, 0.55, 131, 0.95),
    "views-material":  ("band",      0.50, 0.50, 141, 1.00),
    "gallery-approach": ("horizon",  0.61, 0.60, 151, 1.00),
}

# master canvas per slot: largest width the registry emits, at the slot's exact ratio
CANVAS = {
    "hero": (2400, 1500), "pause-west": (2400, 1500), "pause-afterglow": (2400, 1500),
    "plate-living": (1600, 1000), "plate-garden": (1600, 1000), "plate-interior": (1600, 1000),
    "views-west": (1600, 686), "views-living": (1600, 1000), "views-pool": (1600, 1000),
    "views-olives": (1600, 2000), "views-olive-night": (1600, 2000),
    "views-terrace": (1600, 1000), "views-interior": (1600, 1000),
    "views-material": (1602, 534), "gallery-approach": (2400, 1029),  # 1602x534 = exact 3:1
}

# which hours each slot keeps (mirrors process-photos.py / Appendix A)
HOURS = {
    "hero": "pair", "plate-living": "pair", "pause-west": "pair", "pause-afterglow": "pair",
    "views-west": "pair", "views-living": "pair", "views-pool": "pair", "gallery-approach": "pair",
    "plate-garden": "day", "views-olives": "day", "views-terrace": "day", "views-material": "day",
    "plate-interior": "eve", "views-olive-night": "eve", "views-interior": "eve",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="images/_masters", help="masters folder (gitignored)")
    ap.add_argument("--only", default="", help="comma-separated slot names")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    for slot, (motif, horizon, sunx, seed, glow) in COMPOSITIONS.items():
        if only and slot not in only:
            continue
        w, h = CANVAS[slot]
        hours = HOURS[slot]
        for hour in (("day", "eve") if hours == "pair" else (hours,)):
            reg = "day" if hour == "day" else "eve"
            arr = study(w, h, reg, motif, horizon, sunx, seed, glow)
            name = f"{slot}--{hour}.png" if hours == "pair" else f"{slot}.png"
            Image.fromarray(arr).save(os.path.join(args.out, name))
            print(f"  {name}  {w}x{h}")


if __name__ == "__main__":
    main()
