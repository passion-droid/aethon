# AETHON — general site review · 2026-10 (working memo)

Owner-commissioned "general check, no fundamental changes" of the live site (2026-10-12,
main @ `717985b`). Six independent reviewer lenses in parallel, every finding adversarially
re-verified by a separate skeptic, then a completeness critic for what no lens touched.
Mirrors the July audit's working-memo format; continue from here and tick items as they land.

> `docs/` lives on the `internal` branch only — this memo is not public.

## Method
- **Lenses (subagent reviews):** CODE & consistency · FUNCTION (new Playwright regression
  matrix, now kept as `scripts/verify-site.py` on `main`) · AESTHETIC & responsive (48-shot
  screenshot matrix, 360–1440 + landscape phone, both hours) · COPY & voice (proposals only) ·
  BRAND guardrails & palette (mechanical colour/font/logo inventory) · SEO/meta & integrity.
- **Verification:** 34 raw findings → 34 unique → one skeptic per finding, instructed to
  refute, reproduce and check CLAUDE.md decisions: **32 confirmed · 1 settled · 1 refuted**.
  Critic exercised print, JS-off, blocked fonts, forced-colors, text-spacing, 320/1920 px,
  200 % zoom and touch-hover → **7 extra findings** (1 × S2, 6 × S1).
- **Classes:** **A** = objective, non-fundamental, autonomously fixable (batched after the
  owner has seen this memo) · **B** = owner decision or needs research (design / copy / voice —
  the sign-off rule) · **Settled** = documented decision re-confirmed.
- **Severity:** 3 = visitor-visible defect · 2 = real inconsistency · 1 = nit.

## Headline
The site is in good health: the regression matrix ran **194 PASS · 3 FAIL · 3 SKIP** (the FAILs
are the two real defects A-5 and A-14 below; SKIPs are bot-shielded social links), zero console
errors / page errors / failed requests on all four pages in both hours, zero horizontal
overflow at any width, hand-synced token blocks byte-identical, fonts self-hosted with zero
third-party requests, the blue-check clean (every chromatic literal sits at hue 24–69°), JSON-LD
valid, crawl layer consistent, and — new since the memos — **the legal imprint is fully
populated (no `[ ]` placeholders remain)**. What the review found is a layer of real but
contained defects: three S3 items visible on phones and iPad-portrait, a dozen S2 consistency
items, and polish.

## Status
- [x] Six lens reports received (2026-10-12)
- [x] Adversarial verification complete (32 / 1 / 1)
- [x] Completeness critic complete (7 extras, 9 gaps)
- [x] Owner has read this memo — **"go für alle Vorschläge"** (2026-10-12)
- [x] Group B decisions taken (see *Decisions* below)
- [x] Group A + approved B batch implemented + deployed — `main@b5d0d8e`, one push, Pages run 142 `success` (2026-10-12 21:05 UTC), matrix 216 / 0 on the final tree

## Decisions and shipped values (2026-10-12)
- **Group A:** all 23 items applied as specified, with one measurement-driven addition: the
  print block also resets `transition`/`animation` (`*, *::before, *::after` inside
  `@media print`) — on a media switch Chromium starts a transition from the on-screen value,
  so `.reveal` stayed at opacity 0 and the footer kept its dark fill without it.
- **B-1 (bar band):** option (ii) — but measured first: six links + mark + toggle cannot share
  one row below ~700 px at any sane size (links ≈ 475 px at 0.62rem/0.1em, mark 80, toggle 44,
  padding), so the **overlay-menu threshold moved 640 → 700** (nav hide, both `.menu` display
  rules, `.js .menu-btn`, the JS resize guard) and the **701–940 band** got the tightened bar
  (`.bar .mark{ flex:none; width:5rem }`, links 0.62rem / 0.1em / `nowrap`, `.bar-right` gap
  0.9rem, nav gap 0.7rem, bar padding `clamp(1.25rem, 4vw, 3rem)`; the Afterglow hint and the
  skip link follow that edge — `header.bar .toggle-hint` / `a.skip-link`, specificity-raised
  because the band block sits before their base rules). iPads (744 / 768 / 820 portrait) keep
  the desktop nav as decided. The upper edge was first 900: the diff review measured a 4 px
  mark-to-nav gap at 901 with a coarse pointer (44 px toggle), clearing only from ~920 — hence
  940. Verified at every 10 px from 700 to 940 plus 744/768/820/901/905/915/941/1024/1440, fine
  and coarse: mark 80 px (96 from 941), one nav row, ≥ 12 px gap, bar < 90 px, hint flush.
  **Second diff-review catch:** a width-only band also matched landscape phones (844 × 390 is in
  range but uses the overlay), shrinking their mark to 80 and pulling the bar 17 px off the
  `--edge` content column — the band is now scoped to where the inline nav shows
  (`and (min-height:501px)`, `and (pointer:fine)`, `and (pointer:none)` — the complement of the
  nav-hide query's coarse + short). 844 × 390 coarse: mark 96, padding 50.64 = `--edge`; a short
  FINE window (800 × 450) still gets the band (inline nav shown there).
- **B-2:** `text-wrap: balance` on `h2.section-title` + legal `h1.title`; `pretty` on
  `.note-source` (`.mat-note` is an inline span — no-op, skipped).
- **B-3:** legal measure 92ch → **72ch** (`.measure` + `p`).
- **B-4:** owner nudges DARK Architectural Lighting (Sectigo DV expired 21 Aug 2026); the credit
  link stays.
- **B-5:** "Last updated **12 October 2026**" — the notice text changed today (toggle wording,
  anchors), so today's date is the honest one; rule recorded: bump whenever the text changes.
- **B-6:** four Oxford commas inserted. **B-7:** touch `.more-link` underlines its text
  (`text-decoration` with `--field-line`, offset .35em) instead of the box-wide border.
  **B-8:** 404 gained `body.night` tokens, the white logo and a saved-preference init (no R4
  clock on an error page). **B-9 / B-10:** deferred to photography day. **B-11:** gallery
  chapter VI → "Materials, **close at hand**" (tracker title + aria-label, intro, eyebrow);
  both briefs already carry "Iroko, close at hand" — untouched. **B-12:** "the Daylight /
  Afterglow (day / night) toggle". **B-13:** The plan → "growing stiller **floor by floor**".
- **B-14 (fallback font), measured:** the LT Museum fallback is set only in UPPERCASE + tracked
  strings; tracking is in em and unaffected by `size-adjust`, so the July whole-glyph fit
  (116.7 %) over-set every string. Against 40 live strings at 1366: 116.7 % → mean deviation
  21.9 %, max 29 %; **90 %** → mean 2.4 %, max 8.3 %, range 92 % ("Iroko" mat-name, 0.06em)
  … 106 % ("Register interest" nav, 0.18em). One value cannot fit all trackings; 90 % is the
  minimum-mean compromise. Shipped in index / gallery / legal. **Diff-review catch:** the
  ascent/descent overrides are percentages of the size-ADJUSTED em (100 px probe: real face
  116 px line; 116.7 % + 81.3/18.2 → 116 px; 90 % + the same overrides → 89 px — every LT
  Museum box 23 % shorter during the swap, the form button 47 → 43 px). Re-scaled together to
  **105.4 % / 23.6 %** (0.9 × 1.29 ≈ 1.161): probe 116 px = real; with `/fonts/` blocked the
  submit / label / more-link / nav-link boxes now hold within 1 px and the nav width within 4 %.
- **B-15:** `html{ color-scheme:light } html:has(body.night){ color-scheme:dark }` on all four
  pages. **B-16 / B-17:** owner-side / deferred (as proposed).
- **Verification before push:** `scripts/verify-site.py` on the final tree — **198 PASS · 0 FAIL ·
  2 SKIP** (DARK's certificate, Facebook's bot shield); a targeted 27-check script for the batch
  (byte-sync of the four hand-synced blocks, band geometry fine+coarse, pair-label contrast 8.05:1
  on the phone at night, gallery caption/ratio/trio geometry at 1440/768/390, print emulation +
  A4 PDF, lightbox ring, touch sticky-hover, no-JS, 404 night, legal anchor arrival through the
  WIP notice, fallback widths ±2.3 %) — **27 / 27**; adversarial diff review (five area reviewers
  + a refutation round) — see *Diff review* below.

## Diff review (adversarial, before the push — 2026-10-12)
Five hunters over the batch diff (index CSS · index JS/copy · subpages · docs/comments ·
regressions), each instructed to break the change in the browser, then a refutation round.
**Four real defects the targeted checks had missed, all fixed before the push:**
- **Touch `.more-link` underline rule was dead** — it sat in the touch media block BEFORE the
  base `.more-link` rule; a media query adds no specificity, so the base rule's
  `text-decoration:none; border-bottom:1px; padding-bottom:4px` won on every touch device (the
  box-wide rule under the wrapped Plan pointer was still there at 390). Moved after the base
  rule (and `padding-bottom:0.4rem` restored, which the base rule had been overriding too).
- **Print block could not reach the header mark** — `.mark` (0,1,0) lost to `.bar .mark`
  (0,2,0): the printed bar carried a blank 96×44 box where "AETHON" should read; `.wip` lost to
  `.wip[open]` (the open notice printed as a card), `.menu-btn` to `.js .menu-btn` on narrow
  paper, `body.night .wordmark` kept the white logo under the hero text. **And Afterglow printed
  pale:** the night tokens stayed in force, so an evening Save-as-PDF (R4 opens every
  no-preference visit after Paphos sunset in Afterglow) came out #EEE7D6-on-white (1.2:1; 2.98:1
  after Chromium's text clamp). Rewritten ×3: selectors repeat the base specificity
  (`.bar .mark, body.night .bar .mark, .wip[open], .js .menu-btn …`), `color-scheme:light`, and
  `body.night{ --bg:inherit; --ink:inherit; … }` hands every role token back to the `:root`
  Daylight value (the tokens all live on `:root`, so `inherit` is page-agnostic). Verified on
  all three pages × both hours with the notice open: computed ink `rgb(44,38,32)`, marks
  text-indent 0 / no background image, A4 PDFs carry the text wordmark (pdfium extracts the
  tracked mark as "A E T H O N") and dark ink.
- **Fallback-font vertical metrics** — see B-14 above (overrides scale with `size-adjust`).
- **Band upper edge 900** — see B-1 above (4 px gap at 901 on touch → 940).
The regressions hunter, re-run against the already-fixed tree, caught **two more**:
- **Band on landscape phones** — see B-1 above (width-only query → scoped to where the nav shows).
- **Printing with the WIP notice open gave ONE truncated page** — `lock()` pins the body inline
  (`position:fixed; top:-sy; left/right:0; width:100%`) while the dialog is open; the print block
  hid the card but inline styles outrank the sheet, so Ctrl+P on a first visit (the likeliest
  print moment) printed one viewport-sized sheet (index 1 page vs 13, gallery 1 vs 7, legal 1 vs
  3; same with the overlay menu or the lightbox open). Fixed ×3 with
  `body{ position:static !important; top/left/right/width … !important }` in the print block;
  the matrix's `print` group now asserts the lock is released (computed `static` with the inline
  `fixed` still set) and that the A4 PDF runs past one page — 3 pages × 2 hours, all green.
Plus ten stale leftovers: the index SHOT BRIEF still called the Views "grey placeholders"; the
gallery lightbox comments still described placeholder plates; `images/README.md` step 3 claimed
the evening layers are `aria-hidden` with their wrapper (only the hero wrapper is — and it hides
the DAY image too, so photography day must remove it) and pointed to a gallery alt draft the
batch had deleted; CLAUDE.md said "641–890 band", "WIP opened on every load", "lightbox dormant
until a real img", and deferred the fallback numbers to this memo's (stale) B-14 row; the matrix
label said "<640px". All corrected; the matrix gained `bar` (band geometry fine + coarse,
hint alignment, the landscape phone) and `print` (3 pages × 2 hours, lock release, page count)
groups so these stay covered — final tree: **208 PASS · 0 FAIL** on the full matrix before the
last two fixes, then `bar` 6/6 + `print` 18/18 + the 20-check targeted suite re-run green.
**Accepted as-is:** `/gallery/#ch-…` arrivals rest ~19 px short of `scroll-margin-top` because
the chapters are themselves `.reveal` boxes (measured mid-transform) — pre-existing, identical to
native in-page navigation, heading well clear of the bar.
**Lesson recorded in CLAUDE.md:** a batch that touches the cascade or the hand-synced blocks gets
a skeptic pass over the DIFF, not only targeted checks — three of the four defects were
specificity/order errors that "the rule is present" checks cannot see.

## Group A — safe fixes (non-fundamental, no sign-off needed)
| # | Sev | Where | Finding → fix |
|---|---|---|---|
| A-1 | 3 | index.html:509-512 (phone guardrail) | Afterglow on phones: the four paired-plate labels render pale-on-pale (1.26–1.52:1) because the guardrail shows the DAY layer but the label keeps the night colour → add inside the guardrail block `body.night #gallery .frame.shot-pair .label, body.night .plate .frame.shot-pair .label{ color: rgba(34,29,24,.96) }` (verified 5.8–7.7:1). |
| A-2 | 3 | gallery/index.html:174 | Grid plates stretch to the figure height: pictures eat the caption's row — captions sit 30 px below the figure and vanish behind the next plate on phones; ratios off-brief (1.39 instead of 3:2, 0.77 instead of 4:5) → `.plate picture{ height:auto }` (img keeps 100 %; trio lead keeps its flex override). Verified at 1440/1024/768/390. |
| A-3 | 2 | gallery/index.html:217 | Lightbox focus ring uses `--accent` on the fixed dark backdrop: day olive = 2.03:1 (< 3:1) → `.lb-btn:focus-visible{ outline-color:#EEE7D6 }` (the buttons' own colour). |
| A-4 | 2 | index.html:1287-1339 | Views `sizes="(min-width:620px) 46vw"` vs the `.frames` two-column breakpoint at 760 px → 800w served into a 1310-device-px frame on iPad-mini portrait → `(min-width:760px) 46vw, 92vw` ×24 attributes. |
| A-5 | 2 | WIP IIFE ×3 (index:1752-1759, gallery, legal) | A deep link with a fragment (`/#interest`, `/gallery/#ch-evening`) is lost when the WIP notice opens: `unlock()` restores scrollY 0 → honour `location.hash` (scrollIntoView, respects scroll-margin) else restore; keep the three copies byte-identical. |
| A-6 | 2 | CLAUDE.md:735 | The publicly served CLAUDE.md still contains the outlook.com address the project rule says never to publish → scrub to "the owner's inbox (mail@aethon.house since 2026-07-03)". |
| A-7 | 2 | all three pages | **No print stylesheet** (critic): Save-as-PDF on arrival yields 13 blank pages (`.js .reveal` opacity 0 is never released for print), the fixed bar repeats on every page, CSS-background wordmarks and the dark footer vanish → one hand-synced `@media print` block: reveal visible, bar static, hero height auto, hide toggle/menu/chip/scroll-cue/skip-link, expose the wordmark text. No on-screen change. |
| A-8 | 1 | index.html:586 vs 731 | Hero Daylight/Afterglow chip has no visible hover in preview mode (specificity) → `body.preview .hero-media:hover{ color:var(--ink) }`. |
| A-9 | 1 | index:61-62; WIP CSS header ×3; gallery:7, :333-355 | Stale source comments: "LT Museum is one weight 100–900" (it ships Medium + Bold in two ranges); WIP header says "no localStorage gate / every load" (it is session-gated); gallery head comment; gallery runbook comment still mentions `.ph`/evening-01 → rewrite in place, identically in all three files where byte-synced. |
| A-10 | 1 | index.html:531 | Hold-to-preview token flip drifts: `--light-warm` #EACA9C vs `:root` #E9C79B (inert today, but the "hand-synced" contract is false) → set #E9C79B. |
| A-11 | 1 | index:194, :208-212; gallery:162-179; legal:112 | Dead CSS: `.measure`/`.hairline` (index), the `.ph` placeholder family (gallery — all 23 slots hold pictures), `.ph` (legal — imprint filled) → delete; keep `.lb-ph` (live lightbox fallback). |
| A-12 | 1 | index:1366-1373, :1389, :892-904, :1029-1030, :1107-1108; gallery:364-365 | View-source leaks internal operations notes: the "other site" sharing the Brevo account, the list name, master-file workflow, pointers to `docs/` paths that live on `internal` → trim to mapping facts; point at `images/README.md`. Do NOT touch the SHOT BRIEF blocks (they stay by decision). |
| A-13 | 1 | legal:231, :240 | Three typewriter apostrophes (`'`) where every other page sets `’` → mechanical substitution. |
| A-14 | 1 | index.html:1599 | A honeypot-caught (bot) submission still counts as `form-submit` (beacon listener fires before the AJAX handler discards it) → mirror the honeypot guard in the beacon listener. |
| A-15 | 1 | README.md:8, :34-38 | Publicly served README is stale (Formspree ID, "a single file") → refresh, brand-neutral, no internals. |
| A-16 | 1 | index.html:1146-1231 | Materials swatches `sizes=22vw` but render ~27vw → 400w upscaled on 125 % desktops → `(min-width:760px) 27vw, 45vw` ×24 attributes. |
| A-17 | 1 | index.html:336 vs toggle / chip / evening-line / hold-hint | Without JavaScript five controls render as dead affordances while only the menu button is `.js`-gated (critic) → gate them the same way; make the hold-hint `.js`-only. |
| A-18 | 1 | legal (no section ids); index.html:1399 | The form's "privacy notice" link lands on the imprint — the legal page has no anchors (critic) → `id="imprint" / "privacy" / "storage"` on the three h2 + scroll-margin, form note → `/legal/#privacy`. |
| A-19 | 1 | hover rules, all pages | Hover styles are unconditional, so on touch a blocked tap leaves the submit button inverted (critic) → wrap hover-only rules in `@media (hover:hover)`; `:focus-visible` stays outside. |
| A-20 | 1 | index.html:609-615 | Browser autofill paints Name/Email in Chrome's light-blue tint — the one colour the guardrail forbids (critic) → `:-webkit-autofill` override onto `--bg-soft` / `--ink`. |
| A-21 | 1 | site.webmanifest | No `start_url`/`id`: "Add to Home screen" from /legal/ pins the legal page (critic) → `"start_url":"/"`, `"id":"/"`. |
| A-22 | 1 | images/README.md + CLAUDE.md checklist | Parked but process-relevant: every photo slot ships `alt=""` and the runbook promises "no HTML edits" — real photographs would land as decorative → add the per-frame alt pass to the photography-day runbook now (docs only). |
| A-23 | — | CLAUDE.md | Record: legal placeholders filled; `scripts/verify-site.py` is the regression matrix; this memo. |

**Deliberately NOT applied (looked safe, is not):** a `.nojekyll` file (critic gap) — it would
stop Jekyll's dot-path exclusion and newly expose `.github/` and dotfiles on the brand domain.
Left as is.

## Group B — owner decisions (design / copy / voice) with recommendations
| # | Sev | Finding | Options · recommendation |
|---|---|---|---|
| B-1 | **3** | **641–890 px band (iPad / iPad-mini portrait included): the bar logo is squeezed to 0–94 px and "Register interest" wraps to two lines** (index.html:228-251) — the most visible defect of the review; 200 % zoom on a 1366 laptop lands in the same band. | (i) raise the overlay-menu threshold to ~900 px — contradicts the documented "iPads keep the desktop nav"; (ii) keep the inline nav and make it fit the band: `.bar .mark{ flex:none }`, `nav.links a{ white-space:nowrap }`, tighter gap/letter-spacing ≤ 900 px. **Recommend (ii).** |
| B-2 | 2 | 5 of 9 section titles end on a lone word at 1440 (e.g. "Where the coast turns / west."); legal h1 too — the only display headings without `text-wrap:balance` (hero already has it). | Add `text-wrap:balance` to `h2.section-title` + legal `h1.title`; `pretty` on `.note-source`. **Recommend yes.** |
| B-3 | 2 | Legal reading measure runs 101–111 characters per line at ≥ 1024 px (memo yardstick 50–75, hard cap 80); the CSS comment shows the wide measure was deliberate ("fewer line breaks, less scrolling"). | Keep, or set `.measure`/`p` to ~72ch (≈ 80 CPL). **Recommend 72ch** — the project's own standard. |
| B-4 | 2 | The Lighting credit's site (www.dark-cy.com) has had an expired TLS certificate since 21 Aug 2026 — clicking yields the browser interstitial. | Owner nudges DARK to renew; keep the link meanwhile (external fault) or temporarily plain-text the credit. **Recommend: nudge, keep link.** |
| B-5 | 2 | Legal "Last updated 4 July 2026" predates the 5 and 9 July notice changes (storage paragraph, event-counter disclosure). | Set to 9 July 2026 now; bump again at the counsel pass. **Recommend 9 July 2026**, plus the rule: bump whenever the notice text changes. |
| B-6 | 2 | Four series without the Oxford comma against house style (index 960, 961, 962, alt 1088). | Insert the four commas — completes the C-12 sweep. **Recommend yes.** |
| B-7 | 1 | Two-line `.more-link` on phones draws a full-width rule under the block instead of an underline (touch `inline-block`). | `text-decoration: underline; text-underline-offset:.35em` for the touch variant. **Recommend yes.** |
| B-8 | 1 | 404 page ignores a saved Afterglow preference (no night tokens, no init line; "404 left minimal" referred to fonts). | Add the `body.night` tokens, white logo under night, saved-preference init line. **Recommend yes** (parity). |
| B-9 | 1 | Ten micro-label type steps between 10.5 and 13.8 px; several below the memo's 12 px watch line (labels, captions, scroll cue, chip, hint). | Consolidate to three steps. **Recommend defer to photography day** (labels get re-tuned over real frames). |
| B-10 | 1 | Three plate labels dip to 4.2–4.4:1 against the darkest/brightest 5 % of light-study pixels (means pass AA). | Scrim or full-alpha labels. **Already on the photography-day contrast re-check — defer.** |
| B-11 | 1 | "close at hand" (two Iroko lines) vs "close to hand" (gallery chapter VI title ×3). | Harmonise one way. **Recommend "close at hand"** (the caption shipped in the brief). |
| B-12 | 1 | Legal calls the toggle "day / night" while the site says Daylight / Afterglow. | "the Daylight / Afterglow (day / night) toggle". **Recommend yes** (counsel batch). |
| B-13 | 1 | "as the house rises" verbatim in The plan (996) and The interior (1078), with "kept for rest" in both. | Vary The plan's clause (e.g. "growing stiller floor by floor"); The interior keeps the line. **Owner's voice call.** |
| B-14 | 1 (conf .7) | The LT Museum metric-matched fallback over-sets uppercase tracked text by 6–19 % (nav 679 → 805 px) on a slow-network swap; Spectral's fallback is exact. | Re-fit `size-adjust` against the uppercase strings. **Measured + shipped: 90 % (the ~98–104 % guess was far off — up to 29 % over-set) with the ascent/descent overrides re-scaled to 105.4 / 23.6 % — see *Decisions*.** |
| B-15 | — | `color-scheme` never declared: UA chrome (classic scrollbars, form-control internals, validation bubbles) stays light in Afterglow (critic gap). | `:root{ color-scheme:light }` + `body.night{ color-scheme:dark }`. **Recommend yes** (small, visible only in UA-drawn parts). |
| B-16 | — | Security headers (HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy): GitHub Pages sets none; only Cloudflare can (Transform Rules → Modify Response Header; HSTS under SSL/TLS). | Owner-side, when convenient. |
| B-17 | — | Data-saver: the cellular guardrail keys on viewport/pointer, not `prefers-reduced-data` / Save-Data. | Optional extension of the guardrail. **Defer.** |

## Settled / refuted (documented decisions re-confirmed)
- Legal's three `<strong>` words render in synthesized faux bold (no bold Spectral face shipped) — **accepted quirk**, settled.
- Pair-slot captions name an evening hour but show the daylight composition by day — the deliberate **pair-naming convention**, refuted.

## Critic gaps that only the owner / a real device can close
- Real iOS Safari: long-press on the hold plates (callout suppressed?), the dusk sweep, 100svh.
- Assistive technology: nobody listened with NVDA/VoiceOver — the hold plates, WIP notice and toggle are DOM-verified only.
- Forced-colors with a DARK system theme (Windows High Contrast Black).
- Live-origin facts the sandbox cannot see: real 404 status, cache/compression headers, the Cloudflare beacon injection, that `/CLAUDE.md` and `/README.md` return 200 (inferred from Pages/Jekyll defaults; robots disallows them).

## Clean bill (what the lenses checked and found right)
HTML validity ×4 · hand-synced blocks byte-identical (WIP markup/CSS/IIFE, no-flash init, sweep,
theme swap, token values, --space-* scale) · script order · zero dead JS; beacon names = worker
allowlist · theme / R4 clock (11 cases incl. DST) / sweep direction (frame-burst monotonic) /
hold / overlay menu + landscape / lightbox / WIP (12 close combinations) / AJAX form success +
failure + honeypot / beacons incl. DNT = zero / cellular guardrail request log / keyboard order /
505 asset references + 37 anchors on disk · spacing scale on the proximity rule · token contrast
≥ 5.1:1 everywhere · hover/focus states · gallery tracker geometry · en-GB spelling, sentence
case, no exclamation marks, no banned content, names + dates consistent, Greek word renders ·
212 colour literals inventoried, none blue, accent olive-only, gold logo-only, fonts
self-hosted, logo variants per context, favicon set + manifest files exist · JSON-LD valid,
outline/landmarks, sitemap/robots, preload hints exact, first-load weight 222 KB at 1440.

## Artifacts
- Consolidated findings: scratchpad `review/consolidated.json` (session-local).
- Screenshot matrix (48) + crops: lens `aesthetic/`; contact sheets `review-defects.png`,
  `review-overview.png` (sent to the owner 2026-10-12).
- Regression matrix: `scripts/verify-site.py` (main) — run `python3 scripts/verify-site.py`,
  ~2 min, 200 checks; expect 3 FAIL until A-5 / A-14 land.
