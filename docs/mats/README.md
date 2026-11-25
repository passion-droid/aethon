# Door mats — decision record (2026-11-12 → 2026-11-25)

Physical brand, not part of the website. Eight custom logo mats for the house, ordered from a
Cypriot supplier (En Oiko Dimiourgies). Two catalogue qualities are in play: **Prado** (printed
nylon, 7 mm, PVC backing, catalogued for indoor use) and **Azure** (vinyl loop, PVC backing,
outdoor-rated). No address appears in any of these files.

## The order as specified (owner's decision, 2026-11-16; edge and mat 4 settled 2026-11-25)

| No. | Label | Qty | Width × depth (cm) | Quality | Base | Logo | Logo width |
|---|---|---|---|---|---|---|---|
| 1 | ENTRANCE-OUT | 1 | 100 × 80 | Azure | Beige | Brown | 50 cm |
| 2 | KITCHEN-OUT | 1 | 70 × 60 | Azure | Beige | Brown | 35 cm |
| 3 | VERANDA | 1 | 200 × 100 | Prado | Beige 2 | Brown 12 | 100 cm |
| 4 | ENTRANCE-IN | 1 | 100 × 110 | Prado | Beige 2 | Brown 12 | 50 cm |
| 5–7 | BALCONY 1 · 2 · 3 | 3 | 100 × 60 | Prado | Beige 2 | Brown 12 | 50 cm |
| 8 | BALCONY-IN | 1 | 70 × 60 | Prado | Beige 2 | Brown 12 | 35 cm |

- Logo: the AETHON wordmark from the logo file (never typeset), one colour including the dot,
  centred, 50 % of the mat width.
- Edge (settled 2026-11-25): the six Prado mats without edging, because Prado edging exists only in
  black; the two Azure mats with the 2.5 cm edging in beige. Finished sizes as ordered.
- Floors: 1, 3, 5–7 lie on travertine (3 and 5–7 covered); 2 on a dark anthracite stone; 4 and 8
  on marble.
- Mat 4 is 100 wide and 110 deep (owner, 2026-11-25): the 100 cm side lies along the door, the
  counterpart to mat 1 outside, and the logo runs along it.

**Open with the supplier (as of 2026-11-25):** the revised artwork for approval, then the order
form and the deposit. Production takes about three weeks from artwork approval and order
confirmation. The quotation is accepted; its figures stay in the owner's mail and are not stored
here.

### The supplier's reply and the owner's answer (2026-11-19)

1. **Reverse the Prado colours** (Brown 12 base, Beige 2 logo — dirt shows less on a dark base).
   Declined. Rendered on the real stone a brown base is a wine-red slab at 3.4–4.6:1 against the
   floor (`supplier-proposal-compared.jpg`). The light base and its cleaning are accepted.
2. **Keep the 2.5 cm edging** on loose-laid mats (fraying, tearing). Accepted — this retires the
   earlier "borderless if only black" rule. Azure: edging in beige. Prado: beige if her supplier
   has it, otherwise brown to match the logo.
3. **Prado on the veranda and balconies.** She asked whether they are fully protected from sun and
   rain. The owner confirmed they are deeply covered and get no direct sunlight; Prado stays as
   ordered.
4. **Logo dimensions** may vary slightly for balance and production; proofs come for approval.

The sample fan labelled 12 mm was outdated, so the thickness question was dropped.

### Her artwork and quotation, and the owner's answer (2026-11-25)

Prado edging exists only in black; Azure edging in beige or brown. Measured from her drawing, the
logos sat at 72–84 % of the mat width instead of the ordered 50 % (146 cm on the veranda mat;
59 cm on the Prado 70 × 60, about 3 cm from the edging), the veranda logo about 5 cm above centre,
and mat 4 was rotated (110 wide × 100 deep). `supplier-artwork-2026-11-25-compared.jpg` shows her
drawing beside the order on the real stone. The owner's answer, sent the same day:

1. **Prado without edging**, all six, knowingly against her durability advice. A 2.5 cm black frame
   is about three times as wide as the letter strokes and far darker than the brown: it becomes
   the loudest element of the mat. The rule is back to "edging only where it can be tone-in-tone".
2. **Azure edging beige**, on both mats.
3. **Logo smaller**: about half the mat width, as small as the print raster allows ("more subtle
   and elegant"); slightly larger only if production needs it, with the size reported back.
4. **Logo centred** on every mat.
5. **Mat 4**: 100 cm along the door, 110 deep.
6. No price questions; the quotation stands.

### Checking the next artwork

Measure it, do not judge it by eye: `python3 tools/measure_artwork.py <drawing.png> --ref-cm 200`
prints size, edging and logo width per mat. Expected: logo about 50 % of the mat width (100 cm on
the 200 × 100, 50 cm on the 100 cm mats, 35 cm on the 70 × 60, or the smallest size production
reports as clean), centred; no edging on the six Prado mats; beige edging on the two Azure mats;
mat 4 drawn 100 wide × 110 deep; one colour including the dot; the wordmark from the logo file.

## How the decision moved

1. Supplier mock-ups: black or dark green ground with gold or beige lettering.
2. Brand reading: gold is the dot only (as on the stone signage), the catalogue "gold" is an ochre.
   First proposal: dark green ground, beige letters.
3. Owner: a dark mat is too strong on light stone. Measured: dark grounds sit at 7–14:1 against
   the floor, light and mid grounds near 2:1. Direction turned to a light ground with a dark mark.
4. Placement corrected by the owner: five of eight mats lie on travertine, one on anthracite, two
   on marble. The owner accepts Prado on the covered veranda and balconies, and reads the
   supplier's "maximum one side 150 cm" correctly as a cap on the short side.
5. Research across five lenses (function and standards, interior rules, logo-mat practice, stone
   compatibility, Feng Shui): `research-report-de.md`, notes in `research-notes/`.
6. Real samples photographed on the marble and the travertine with a white sheet of paper, then
   measured (below).
7. Owner's own check in real light settled it: Beige 2 + Brown 12 (Prado), Beige + Brown (Azure),
   logo at 50 %.

## Measured colours

sRGB after converting the phone's Display P3 and balancing on the paper (88 % reflectance
assumed). Area means. Phone tone-mapping and uneven light make these approximations of about
±15 %; ratios inside one photo are the reliable part. Full values: `measured.json` (marble photo,
diffuse light), `measured-trav.json` (travertine photo, direct low sun).

| Sample | Diffuse light | Low sun | Note |
|---|---|---|---|
| Prado White 1 | `#d4d4c6` | `#c4c6af` | near marble, pale and cool |
| Prado Beige 2 | `#e5c4af` | `#cba789` | rosé in shade, warm tan in sun |
| Prado Light Grey 4 | `#bab5b1` | `#9e988c` | warm-neutral stone grey |
| Prado Dark Grey 13 | `#857c7c` | `#645b57` | taupe |
| Prado Dark Green 14 | `#557d53` | `#445e3a` | forest green, not the brand olive |
| Prado Brown 12 | `#954d4d` | `#723734` | red-brown |
| Prado Black 16 | `#232428` | `#1c1b1b` | cool charcoal |
| Vinyl beige | `#a48a65` | – | true sand, the travertine's hue |
| Vinyl grey | `#75706b` | – | warm mid grey |
| Vinyl brown | `#24201f` | – | near-black brown |
| Vinyl green | `#064627` | – | deep emerald, cool |
| Marble | `#e6e0cd` | – | as light as the palette token, slightly warmer |
| Travertine | – | `#d9be8d` … `#e4cfa4` | golden sand, more saturated than `#DCCDB3` |

Contrast of mat against floor, same photo: Light Grey 4 on marble 1.5:1, on travertine 1.6:1 in
sun and about 1.1:1 in shade; Beige 2 on travertine 1.2:1 in sun and about 1.1:1 in shade.
Lettering: Dark Green 14 on Light Grey 4 2.3–2.5:1, Black 16 on Light Grey 4 6–7.7:1.

## What is worth remembering

- Catalogue swatches mislead. The printed Prado green was far darker than the yarn. Measure real
  samples, with white paper in the frame, and compare mat and floor inside one photo.
- Pile looks darker in raking sun than in shade because the fibres shade themselves.
- The wordmark's strokes are 1.4–1.9 % of its width: 7–9 mm at a 50 cm logo, 5–6.5 mm at 35 cm.
  Published vinyl-loop inlay minima are 9.5–10 mm stroke and 50–76 mm letter height.
- Gold on a light ground reads at 1.2–1.7:1. On light mats the mark is one colour.
- From the research: the house's own Feng Shui consultant has published the advice not to put a
  mark you value on a doormat; a 7–9 mm borderless edge is above every trip threshold found
  (ADA 6.4 mm, BG BAU 4 mm), though none binds a private house; PVC-backed mats on porous stone
  want lifting to dry (weekly indoors, after rain outdoors); printed nylon is not sun-rated.
- A tolerance given in words is read generously. "Feel free to slightly increase in case it's too
  thin" came back as logos half again as large. Give a number.
- "Width × depth" in an order sheet needs the door side spelled out. Mat 4 came back rotated.
- The catalogue already answered the edging question: Prado lists a "black plastic perimeter
  finish of 2.5 cm (optional)", Azure a plastic finish without naming a colour.
- Reading the price list: Prado with logo runs at about €155–165 per m², Azure 9 mm at about
  €250–290. The "€230 per m² for customized dimensions" line belongs to Elysium. Custom sizes are
  priced above the pro-rata rate, towards the next list size, so the list sizes (60 × 90, 80 × 90,
  90 × 120 …) are the economical ones.
- Without edging the catalogue caps one side at 145 cm (150 cm with it).

## Files

- `AETHON-mats-order-2026-11-16.pdf` — the one-page order sheet sent to the supplier (English).
  Source: `aethon-mats-order.html` (expects the repository's `fonts/` at `/home/user/aethon/fonts/`;
  print with headless Chromium, A4 landscape).
- `research-report-de.md` — the research report (German), with `research-notes/` behind it.
- `samples-measured.jpg` — measured samples as flat colours, candidate combinations per floor.
- `samples-on-real-stone.jpg` — mats composed from the real photo textures on the real stone.
- `supplier-proposal-compared.jpg` — the supplier's reversed colours and the edging variants beside
  the order, on the real stone.
- `supplier-artwork-2026-11-25-compared.jpg` — her drawing of 2026-11-25 beside the order: black
  edging against none, drawn logo size against 50 %. The Azure edging tones and the anthracite
  stone in it are assumptions.
- `measured.json`, `measured-trav.json`, `composite-info.json` — the measurements.
- `tools/measure_artwork.py` — measures a supplier drawing: mat size, edging, logo width, centring.
- `tools/` — the other measuring scripts, kept for the method. They point at the session's upload
  paths, which no longer exist; the source photos are not stored here.
