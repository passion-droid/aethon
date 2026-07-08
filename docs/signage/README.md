# AETHON — stone signage blueprints

Fabrication study for the physical brand markers at the property, to hand to the
renovation team (G. Patsalides) and the stone supplier / carver. Dimensions in **mm**;
this is a **design study — verify all dimensions and setting-out on site; not for
structural use.** No address appears anywhere (brand guardrail).

| File | What it is |
|---|---|
| `aethon-qr.svg` | The **working QR** — links to `aethon.house`, error-correction **H**, the brand **"A"** at centre. **Verified scannable** (decoded back to the URL with OpenCV). Vector — give it to the etcher directly. |
| `aethon-signage-sheet-1-entrance.(svg \| pdf)` | **Entrance threshold marker** — honed **marble tile 600 × 450 × 20**, hand-carved V-cut wordmark, **gilded dot only**, inset QR. Elevation + sections + QR spec + keynotes. |
| `aethon-signage-sheet-2-monolith.(svg \| pdf)` | **Seaside promenade monolith** — coastal sandstone, deep-cut wordmark, **bare (no infill)**, engraved URL + **inset QR plate** (spec as Sheet 1, panel 3). Elevation + letter section. |

Brand assets used verbatim: `brand/logo-dark.svg` (wordmark + gold dot) and `icon-512.png` (the "A").

**REV B (2026-07, owner request):** sheets are a **monochrome print set** (B&W, greys for
annotation hierarchy; gilded elements shown grey + labelled); the monolith carries the
**engraved URL + inset QR**.

**REV C (2026-07-06, owner request, superseded):** entrance plate briefly re-proportioned to a
portrait 450 × 600 tile; the sheets began stating explicitly that the carved wordmark is taken
**from the logotype file (brand vector) — never typeset in the LT Museum font** (rule kept).

**REV D (2026-07-08, owner request):** entrance plate is a **landscape 600 × 450 × 20 marble
tile**; **all dimensions in plain mm** for the stonemason (no "cap height" jargon) — wordmark
dimensioned **420 × 97** on the plate (letters 69 high) and **400 × 93** on the monolith
(letters 66 — corrects a wrong "180" callout); **both QR plates enlarged to 150 × 150**; the
monolith's section drawing now shows the **routed QR pocket** beside the letter V-cut.

**Regenerate:** `python3 scripts/gen-signage-blueprint.py` (then print the SVGs to PDF at
1320 × 980 px — the session does this via headless Chromium)
(needs `segno`, `opencv-python-headless`, `Pillow`; writes the SVGs into `docs/signage/`).
