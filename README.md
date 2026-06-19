# AETHON — house of light

The public showcase site for **AETHON House · Paphos** — a private residence on the
western coast of Paphos, Cyprus. The house is a quiet *elevation* of an existing
seafront residence (originally part of the "Faros Beach Houses"), refined while
honouring the original architect's geometry.

The entire site is a single file: **`index.html`** (HTML, styling, and a little
JavaScript are all inside it). There is no build step and nothing to install — the
file *is* the website. This keeps it simple to host and easy to update.

---

## How updates work

You don't edit code by hand. You describe the change in plain language to Claude
(in Claude Code on your laptop, or in chat), Claude edits `index.html`, and the
change goes live automatically a minute or two after it's pushed to GitHub.

Examples of things to just ask for:
- "Swap the placeholder views for these three renders."
- "Soften the green a little / make the hero light warmer."
- "Add a short section about the garden."

## Hosting

Hosted free on **GitHub Pages**, served from this repository.

## Outstanding setup (handled step by step with Claude)

1. **Images** — imagery is woven through the page as placeholders (a hero ambient-loop
   slot, an establishing-film plate, a companion image per narrative section, two
   conceptual floor plans, and the eight-slot Views gallery with an in-code shot brief);
   drop real renders/photos into an `images/` folder and wire them in. Grows to 20–30.
2. **Interest form delivery** — the "Register interest" form needs a free
   [Formspree](https://formspree.io) form ID pasted into `index.html`
   (search the file for `YOUR_FORM_ID`). Until then the form looks correct but
   does not send.
3. **Domain** — `aethon.house` is connected (a `CNAME` is on `main`).

## Decided / in progress

- **Day / Night** — live. A ☀ / ☾ toggle in the header switches the whole page between
  a day and a night mood. Default is day; the choice is remembered between visits.
- **Floor plans** — a conceptual *Plan* section (ground + first floor) now sits after
  *The architecture* as placeholders; awaiting the redrawn, low-detail artwork.
- **Credits** — a colophon before the footer credits the project team (Interior,
  Landscape, Lighting and Feng Shui — now named); the original architect is still to be
  confirmed.
- **Palette** — accent retuned to the real olive leather (BoConcept Nordic Grain Olive
  Green); materials expanded with Venetian plaster, Iroko and Corian "Witch Hazel".
- **Garden** — now has its own section; a subtle lighthouse-locale origins note added to
  *The place*; the day/night mood extends into the garden (lit olive at dusk).
- **Story / copy** — the full narrative is written (place, architecture, garden, the
  interior/withdraw beat, materials); light, comfort, Feng Shui and quiet self-sufficiency
  are woven in by feel, with all specs, systems and amenities kept out of the prose.
  Voice: restraint with a little warmth.

## Still to settle together

- **Hero motion / a short film** — slots are now in place (a hero ambient-loop and an
  establishing-film plate), pending footage and the photo/video brief to commission them. The
  section order is established: Hero → The place → The architecture → The plan → The garden
  → The interior → Materials → Views → Register interest → Credits (the *Plan* sits after
  *The architecture*; *Credits* is a colophon before the footer).

## Brand guardrails (please keep)

- No exact address and **no private detail** — no costs, no equipment or security specs.
- No estate-agent superlatives or "investment opportunity" language.
- The **sunset**, not the lighthouse, is the hero of the story.
- One accent colour only — green, now in two weights: olive-green leather (`#565B3B`;
  `#9CA279` at night — the primary/UI accent) and a softer rosemary-green fabric (curtains
  and some furniture). Everything else is stone — never a blue accent.
