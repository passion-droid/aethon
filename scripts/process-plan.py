#!/usr/bin/env python3
"""
AETHON — floor-plan render processor (tooling, NOT part of the site).

Mutes a saturated architectural floor render into the stone/olive palette and
collapses the pool's blue to pale water (the no-blue guardrail), while keeping
the transparent margin around the plan. Then writes the web assets the page
serves via <picture>: AVIF + WebP (both with alpha, so the plan floats on the
page's --bg-soft and adapts to Daylight/Afterglow) + a JPEG fallback composited
on the day stone, at 800w and 1600w, full √2 ratio (no crop).

Raw 4K masters are NOT committed (see images/README.md — they're large and only
needed to regenerate). Drop them at images/plan/<Ground|First>-floor_4K.png and:
    pip install pillow numpy        # AVIF support ships with modern Pillow
    python scripts/process-plan.py
Outputs overwrite images/plan/{ground,first}-floor-{800,1600}.{avif,webp,jpg},
which is exactly what index.html already references — no markup change needed.
"""
import numpy as np
from PIL import Image

OUT = "images/plan"
BG_SOFT = (240, 238, 232)            # --bg-soft (day): the JPEG fallback is flattened onto this
RATIO = 1600 / 1132                  # the page frame's √2 aspect (aspect-ratio: 1600/1132)
JOBS = [("images/plan/Ground-floor_4K.png", "ground-floor"),
        ("images/plan/First-floor_4K.png",  "first-floor")]
SIZES = (1600, 800)


def mute(im):
    """Saturated RGBA render -> muted stone/olive RGBA, pool-blue drained to pale water."""
    im = im.convert("RGBA")
    rgba = np.asarray(im).astype(float)
    alpha = rgba[..., 3]
    hsv = np.asarray(Image.fromarray(rgba[..., :3].astype("uint8"), "RGB").convert("HSV")).astype(float)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    blue = (H >= 115) & (H <= 185) & (S > 35)                       # cyan→blue pool, never the green lawn
    S2 = np.where(blue, S * 0.08, S * 0.30)                        # global desaturation; pool nearly drained
    V2 = np.where(blue, np.clip(V * 0.88 + 36, 0, 255), V * 0.95 + 20)  # gentle lift; pool a touch paler
    hsv2 = np.stack([H, np.clip(S2, 0, 255), np.clip(V2, 0, 255)], -1).astype("uint8")

    rgb = np.asarray(Image.fromarray(hsv2, "HSV").convert("RGB")).astype(float)
    rgb[..., 0] *= 1.035                                           # warm tint toward stone
    rgb[..., 2] *= 0.95
    rgb = np.clip(rgb, 0, 255)
    return Image.fromarray(np.dstack([rgb, alpha]).astype("uint8"), "RGBA")


def main():
    for src, slug in JOBS:
        master = mute(Image.open(src))
        for w in SIZES:
            h = round(w / RATIO)
            r = master.resize((w, h), Image.LANCZOS)
            r.save(f"{OUT}/{slug}-{w}.avif", "AVIF", quality=56)
            r.save(f"{OUT}/{slug}-{w}.webp", "WEBP", quality=76, method=6)
            flat = Image.new("RGBA", r.size, BG_SOFT + (255,))
            flat.alpha_composite(r)
            flat.convert("RGB").save(f"{OUT}/{slug}-{w}.jpg", "JPEG",
                                     quality=82, optimize=True, progressive=True)
            print(f"  {slug}-{w}: {w}x{h}  avif+webp(alpha) + jpg(flattened)")


if __name__ == "__main__":
    main()
