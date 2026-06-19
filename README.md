# AETHON — house of light

The public showcase site for **AETHON House · Paphos**, a private residence on the
western coast of Paphos, Cyprus.

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

1. **Renders** — drop image files into an `images/` folder and Claude wires them
   into the three view slots.
2. **Interest form delivery** — the "Register interest" form needs a free
   [Formspree](https://formspree.io) form ID pasted into `index.html`
   (search the file for `YOUR_FORM_ID`). Until then the form looks correct but
   does not send.
3. **Domain** — connect `aethon.house` once registered.

## Brand guardrails (please keep)

- No exact address, no floor plans.
- No estate-agent superlatives or "investment opportunity" language.
- The **sunset**, not the lighthouse, is the hero of the story.
- One accent colour only: the deep green leather (`#34463B`).
