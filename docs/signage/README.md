# AETHON — stone signage blueprints

Fabrication study for the physical brand markers at the property, to hand to the
renovation team (G. Patsalides) and the stone supplier / carver. Dimensions in **mm**;
this is a **design study — verify all dimensions and setting-out on site; not for
structural use.** No address appears anywhere (brand guardrail).

| File | What it is |
|---|---|
| `aethon-qr.svg` | The **working QR** — links to `aethon.house`, error-correction **H**, the brand **"A"** at centre. **Verified scannable** (decoded back to the URL with OpenCV). Vector — give it to the etcher directly. |
| `aethon-signage-sheet-1-entrance.(svg \| pdf)` | **Entrance threshold marker** — honed travertine/marble plate, hand-carved V-cut wordmark, **gilded dot only**, inset QR. Elevation + sections + QR spec + keynotes. |
| `aethon-signage-sheet-2-monolith.(svg \| pdf)` | **Seaside promenade monolith** — coastal sandstone, deep-cut wordmark, **bare (no infill)**, no QR. Elevation + letter section. |

Brand assets used verbatim: `brand/logo-dark.svg` (wordmark + gold dot) and `icon-512.png` (the "A").

**Regenerate:** `python3 scripts/gen-signage-blueprint.py`
(needs `segno`, `opencv-python-headless`, `Pillow`; writes the SVGs into `docs/signage/`).
