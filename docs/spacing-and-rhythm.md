# Spacing & rhythm — AETHON House

How vertical space is decided on this site, so gaps *mean* something instead of
being chosen by feel. Companion to the spacing note under `## How the site is
built` in `CLAUDE.md`. Applies to `index.html`, `gallery/index.html`,
`legal/index.html` and `404.html` — buildless, so the scale is hand-synced into
each file's `:root`, like the colour tokens.

---

## 1 · The principle

Vertical gaps encode **grouping**, via the Gestalt **law of proximity**: items
close together read as one group; a wider gap reads as a new group. Readers
interpret a small gap as "these belong together" and a larger gap as "new topic"
— so whitespace, not rules or boxes, carries the structure.

Two rules follow:

1. **Related items sit closer; group breaks sit wider** — on **one consistent
   ratio** (here, tight ≈ ½ of loose), not arbitrary values.
2. **A label hugs what it labels.** An eyebrow sits closer to its title than two
   body paragraphs sit to each other; a heading sits closer to the text *below*
   it than to the text above; a sub-label hugs its list.

Sources: NN/g, *Proximity Principle in Visual Design*; IxDF, *Gestalt
Principles*; the 8-pt-grid + modular-scale literature (freeCodeCamp, Bounteous).

---

## 2 · The scale

An 8-pt grid with 4-pt sub-steps at the low end, as `--space-*` tokens in each
page's `:root`:

| token | value | px | typical use |
|---|---|---|---|
| `--space-3xs` | 0.25rem | 4 | hairline pairs (swatch name → caption) |
| `--space-2xs` | 0.5rem | 8 | tight pairs (label → input, title → source) |
| `--space-xs` | 0.75rem | 12 | title → its immediate text |
| `--space-sm` | 1rem | 16 | within a group (eyebrow → title) |
| `--space-md` | 1.5rem | 24 | prose flow (paragraph → paragraph) |
| `--space-lg` | 2rem | 32 | sub-heading break (above an h3) |
| `--space-xl` | 2.5rem | 40 | block separation (intro → list / form) |
| `--space-2xl` | 3rem | 48 | group break (above an h2 / a sub-label) |

The **hero** keeps its own fluid pair — `--hero-gap-tight` (≈16px) /
`--hero-gap-loose` (≈40px) = `sm` / `xl` — because its type is large and fluid;
the proximity model is the same.

**Fluid macro-rhythm stays `clamp()`-based** and is *not* tokenised: section
padding (`--section-y`), the two-col gap, and the `.palette` / `.plate` /
`.frames` / `.chapter` gaps. These scale with the viewport by design; the fixed
`--space-*` scale is for component- and content-level spacing.

---

## 3 · The proximity model — which step for which relationship

- **tight pair** (label↔value, title↔source, name↔caption): `3xs`–`2xs`
- **within a group** (eyebrow → title): `sm`
- **prose flow** (¶ → ¶): `md`
- **heading → its text**: bind *down* with `xs`–`sm`; the space *above* the
  heading is the group break (`lg`–`2xl`)
- **group break** (new section / sub-section / sub-label): `xl`–`2xl`

A heading always gets **more space above than below**, so it binds to the text it
introduces (rule 2) — e.g. legal `h2 { margin: var(--space-2xl) 0 var(--space-sm) }`
(48 above / 16 below), `h3 { margin: var(--space-lg) 0 var(--space-2xs) }` (32 / 8).

---

## 4 · The audit it came from (June 2026)

The hero originally had ad-hoc gaps (2.2 / 1.6 / 2.8 / 1.8rem) with no grouping —
*house of light* sat closer to the wordmark than to the line it introduces.
Fixing it (two proximity groups) surfaced the same class of issue site-wide:
~18 one-off rem values, no scale, and a few weak bindings:

- **eyebrow → title** on `index` was 1.4rem = its own paragraph gap (so the label
  didn't bind); the subsites used 1.0rem (drift). → unified to `--space-sm`.
- **credits "The minds behind the house"** floated ~equidistant between the facts
  list and the team list. → now hugs the team list (`sm` below, `2xl` break above).
- **legal h2 / h3** had the right proximity *direction* but ad-hoc values. → on the scale.

Everything migrated onto `--space-*`; the tight component pairs that were already
correct (form label→input, swatch name→caption, etc.) kept their spacing — now named.

---

## 5 · Working with it

- **Adding spacing?** Pick the `--space-*` step whose *relationship* matches (§3),
  not the px that looks right. To separate two related items, jump one step — don't
  invent a value.
- **Buildless sync:** the `--space-*` block is duplicated in each page's `:root`.
  Change one, change all four (same discipline as the colour tokens).
- **Don't** reintroduce raw rem gaps in content / component CSS, or collapse the
  tight↔loose ratio — it is what makes the groups legible.
