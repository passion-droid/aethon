# AETHON — house of light

The public showcase site for **AETHON House · Paphos** — a private residence on the
western coast of Paphos, Cyprus. The house is a quiet *elevation* of an existing
seafront residence (originally part of the "Faros Beach Houses"), refined while
honouring the original architect's geometry.

The site is four self-contained pages — `index.html` (the house), `gallery/` (a longer
look), `legal/` (imprint & privacy) and `404.html` — each carrying its own styling and a
little JavaScript. There is no build step and nothing to install — the files *are* the
website. This keeps it simple to host and easy to update.

---

## How updates work

You don't edit code by hand. You describe the change in plain language to Claude
(in Claude Code on your laptop, or in chat), Claude edits the page, and the change goes
live automatically a minute or two after it's pushed to GitHub.

Examples of things to just ask for:
- "Soften the green a little / make the hero light warmer."
- "Reword the garden paragraph."
- "Add a plate to the gallery's evening chapter."

## Hosting

Hosted free on **GitHub Pages**, served from this repository and delivered through
Cloudflare at **aethon.house**.

## Where things stand

- **Photography** — every photo slot on both pages is wired and currently shows
  abstract Daylight / Afterglow light studies as stand-ins; the real photography lands as a
  file swap (see `images/README.md`).
- **Interest form** — live. Submissions are delivered by Brevo; the inline thank-you is
  the receipt (single opt-in, no confirmation email).
- **Daylight / Afterglow** — live. The ☀ / ☾ toggle switches the whole site between the
  two hours; a first visit after sunset at the house opens in Afterglow, and an explicit
  choice is remembered between visits.
- **Floor plans, materials, credits, legal** — complete.
- **Checks** — `python3 scripts/verify-site.py` runs the site's regression matrix
  (Playwright + Chromium; ~2 minutes).

## Brand guardrails (please keep)

- No exact address and **no private detail** — no costs, no equipment or security specs.
- No estate-agent superlatives or "investment opportunity" language.
- The **sunset**, not the lighthouse, is the hero of the story.
- One accent colour only — green, in two weights: olive-green leather (`#565B3B`;
  `#9CA279` at night — the primary/UI accent) and a softer rosemary-green fabric (curtains
  and some furniture). Everything else is stone — never a blue accent.
