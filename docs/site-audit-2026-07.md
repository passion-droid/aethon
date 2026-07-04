# AETHON — full site audit · 2026-07 (working memo)

Seven-persona deep review of the site (owner-commissioned, 2026-07-03). This memo is the
**working state**: findings land here as each persona reports, then get consolidated and
worked off. Continue from here in future sessions — update the checkboxes as items resolve.

> Note: `docs/` is publicly served on the live domain (see SEO-1 below) — this memo is
> public by nature of the repo. It contains assessments, not secrets.

## Method
- **Personas (subagent reviews):** PRIV privacy/GDPR · SEO · BRD luxury-brand strategist ·
  JRN architectural journalist · VIS affluent QR visitor · DEV web developer · A11Y
  accessibility (WCAG 2.2 AA).
- **Lens:** finished site — placeholders read as future photos; the WIP notice's existence
  is exempt (its code/copy is not).
- **Classes:** **A** = objective, autonomously fixable · **B** = needs research/verification
  first · **C** = owner decision (ALL copy/voice changes are C — sign-off rule).
- **Conflict rule (owner, 2026-07-03):** when views conflict → **visitor (VIS) wins, then
  journalist (JRN), then brand (BRD)**; specialists inform but don't override. Hard
  correctness/legal defects aren't matters of view.
- **Deploy policy:** group-A fixes batch-implemented + deployed after the owner has seen
  the consolidated report.

## Status
- [x] PRIV report received
- [x] SEO report received
- [x] BRD report received
- [x] JRN report received
- [x] VIS report received
- [x] DEV report received — all seven in
- [x] A11Y report received
- [x] Consolidation (dedupe, cross-verify A-claims, apply conflict rule)
- [x] Group-A fixes implemented + deployed (2026-07-03 — see the fix commit; all verified:
      0 console errors / 0 failed requests / 0 h-overflow across 4 pages × 2 themes × 320–1440px;
      WIP + lightbox scroll-lock with restore; skip links first in tab order; menu focuses its
      first link; mobile drift off; preview drift alive at 0.22 over the photo; every
      text-over-imagery pair ≥4.5:1 in BOTH themes (day 5.08–6.71, night 6.49–9.71; tracker
      5.1/5.98; pause 7.9/13.8; frame labels 9.8/14.6); wip CSS/HTML/JS + no-flash blocks
      sha1-identical ×3)
- [x] Group B resolved (2026-07-03): B-1 no-newsletters confirmed; B-2 **no DOI — single opt-in**
      (legal + thank-you corrected; consent = submission); PRIV-1 **Cloudflare proxying confirmed**
      → named in legal *Hosting*; B-3 link-preview share test = owner-side (pending); B-4 logo
      **left as-is** (warm black sanctioned on screen; guide olive = print reference); B-9 Greek
      subset **built + shipped** (fonts/greek-aithon-lt.woff2); B-5 PSI workflow triggered.
- [x] Group C first tranche decided + implemented (2026-07-03): C-1 gallery register link ✓;
      C-2 thank-you completeness line ✓ (no-DOI variant); C-3 WIP rewording ✓ ("This site…");
      C-4 docs moved to the `internal` branch + robots.txt disallows ✓; C-5 **mail@aethon.house LIVE**
      (Cloudflare Email Routing → owner inbox; legal imprint + rights swapped, colophon gained an
      *Enquiries* row = JRN-4/C-11 resolved; owner: NO address beneath the register form — form
      stays form-only); C-6 "Bedrooms — 3" ✓. **Walkthrough 2026-07-04 — ALL remaining items
      decided + shipped (main@60ba6a8):** C-7 pointer after The plan ✓; C-8 evening line = Afterglow
      button ✓; C-9 ↗ on Gallery links ✓; C-10 portrait rewrite ✓; C-12 all 11 edits shipped, "The
      withdraw" + button label kept ✓; C-13 numbering → 07·Views ✓; C-14 OG on gallery+legal ✓;
      C-15 about:Residence node + alternateName array ✓; C-16 gold CLOSED logo-only ✓; C-17 footer
      dot (logo-white ×3) ✓; C-18 WIP session-gated + storage disclosed ✓; C-19 counsel drafts
      shipped in place (lawyer reviews the finished page) ✓; C-20/21/23 parked/accepted confirmed ✓;
      PRIV-3 analytics disclosed (2026-07-04) ✓; B-6 renewal = owner-directed (internal fact,
      credits unchanged) ✓; B-8 "ancient" owner-verified ✓; B-9 Greek subset shipped ✓.
      **Still open: B-3 only** (owner shares aethon.house into WhatsApp/iMessage to confirm
      link previews aren't bot-blocked) + the photography-day checklist (C-22).

**Verification discoveries (recorded for future sessions):**
- A dialog that autofocuses at load *moves the sequential-focus start point to its DOM
  position* — a skip link must therefore sit **after** the `<dialog>` markup, or Chrome tabs
  straight past it. (Also: fixed elements parked off-viewport drop out of Chrome's tab order —
  the skip link uses the clip-path pattern at an in-viewport position.)
- The menu overlay's `visibility` transition must be `0s` on open (`0s 450ms` on close), or
  `focus()` on the first link silently fails while visibility still computes `hidden`.
- The A-9 contrast floor ended up as three parts, ALL scoped to `body.preview` (zero effect on
  the finished plain-ground state): a `--hero-wash` radial behind `.hero-inner`, a lighter/
  stronger day `--hero-band`, and the muted hero smalls (`.descriptor`, `.hero-orient`,
  `.scroll-cue`, `.hero-media`) stepping up to `--ink-soft` over imagery.

**B-4 RESOLVED (researched 2026-07-03):** the styleguide PDF's two drawn logos (the streams
with letterform curves) both fill the letters **olive** (`#4C4F38` extracted ≈ `#4C5039`
nominal) + the gold dot; warm black `#212117≈#222216` appears only as the guide's own label
text and a palette swatch. **The shipped `brand/logo-dark.svg` (warm-black letters) therefore
diverges from the guide's primary logotype.** The black-on-stone rendering was praised (BRD)
and may be a deliberate variant → now **owner decision C-24**: (a) recolour the SVG letters to
olive per the guide, or (b) sanction warm-black as the on-screen variant and note it in
docs/brand-styleguide.md so print/signage uses the guide's olive.

---

## PRIV — privacy / GDPR reviewer

**Verdict (short):** unusually strong posture; **measured reality matches the written
claims** — zero cookies in any state, zero third-party requests on load, one localStorage
key (`aethon-theme`, written only by the toggle), WIP dialog stores nothing; only external
host ever contacted is Brevo's `06e3f483.sibforms.com`, only on submit, carrying exactly
the disclosed fields + `SOURCE=aethon.house`. Legal placeholders now **filled** (SIGNGUARD
APP LTD, HE 492256, TIN 60360992J, Kissonerga address); counsel review still pending.

- [ ] **PRIV-1 · Major · B** — If the domain is Cloudflare-proxied (docs suggest yes), the
  notice's "no third party beyond the host above" (legal/index.html:168,171) is false —
  Cloudflare sees every visitor IP + runs bot scoring. → Owner confirms orange-cloud; if
  proxied, name Cloudflare beside GitHub in *Hosting*.
- [ ] **PRIV-2 · Major · B** — "A confirmation email completes your sign-up"
  (legal/index.html:162) asserts Brevo **double-opt-in**, which is a dashboard setting
  invisible to the repo; the checkbox-less consent design leans on it. → Owner verifies DOI
  is ON + the confirmation template matches the no-marketing promise; else reword.
- [ ] **PRIV-3 · Minor · B** — No analytics shipped today (verified); but Cloudflare can
  **auto-inject** its beacon with zero repo diff, silently falsifying "uses no analytics".
  → Standing rule: enabling the beacon ships a same-day notice update.
- [ ] **PRIV-4 · Minor · C** — Notice omits form-step technical metadata: hidden
  `SOURCE=aethon.house` tag + submitter IP/user-agent received by Brevo (consent evidence).
  → One clause in *How the form is delivered* (counsel batch).
- [ ] **PRIV-5 · Minor · B** — "Sendinblue SAS" is the pre-2023 entity name (now **Brevo
  SAS**); flat "within the European Union" may overreach current subprocessor list
  (legal/index.html:165). → Verify vs Brevo DPA; update name; hedge transfers if needed.
- [ ] **PRIV-6 · Minor · C** — Retention "until the list is no longer maintained" is
  open-ended (legal/index.html:174). → Lawyer: bounded criteria (withdrawal / 24-month
  review / list end).
- [ ] **PRIV-7 · Minor · C** — DSAR/rights channel runs through a consumer outlook.com
  mailbox (no DPA). → Owner: business-grade mail or accept knowingly. (Pairs with BRD-2.)
- [ ] **PRIV-8 · Nit · C** — AJAX success copy is optimistic (no-cors = delivery ≠
  acceptance) and never mentions the confirmation email. → Copy sign-off; pairs with BRD-1.
- [ ] **PRIV-9 · Nit · C** — "sets no advertising or analytics cookies" undersells the
  truth (zero cookies of any kind, verified). → "sets no cookies at all" (copy sign-off).
- [ ] **PRIV-10 · Nit · A** — Internal "pending counsel" HTML comment ships in public
  page source (legal/index.html:143–147). → Trim the comment.
- [ ] **PRIV-11 · Nit · C** — mailto plain-text harvestable (3× legal). → Recommend leave.
- [ ] **PRIV-12 · Nit · C** — 404 has no footer/legal link (verified harmless — no JS, no
  storage). → Optional one-line footer parity.

**Works (don't break):** claims=measurements; point-of-collection note + privacy link at
the form; notice skeleton above par (named controller+reg, consent+withdrawal, full rights,
Art. 77 + Cyprus Commissioner, hosting/transfer disclosure); no secrets in repo/history
(146 commits scanned); no-address guardrail holds everywhere; sitemap/noindex/legal-link
parity consistent.

---

## SEO — technical + editorial SEO

**Verdict (short):** the decided meta strategy is shipped **exactly** (lockup titles,
deduped og/twitter, "AETHON · House of Light" site-name across all machine surfaces, valid
JSON-LD, textbook crawl layer). Engine still cold (1 impression, pos 27) but markup isn't
the bottleneck. Two real risks are not tags: the public strategy docs (SEO-1) and
unverified link-preview bots (SEO-2).

- [ ] **SEO-1 · Major · B** — **Internal docs are live on the brand domain**: GH Pages
  serves all of `main`, so `aethon.house/CLAUDE.md` (names the private sale intent),
  `docs/seo-and-search.md` (the whole playbook), imagery brief, signage PDFs are crawlable
  + unblocked; robots.txt allows everything; `.md` is prime AI-crawler food; GH Pages has
  no `X-Robots-Tag`. → Mitigation: robots.txt `Disallow: /docs/`, `/scripts/`, `/*.md$`
  (trade-off: robots.txt is public and advertises paths). Real fix (owner): keep internal
  docs out of the published branch. Note: private repo would NOT fix Pages serving.
- [ ] **SEO-2 · Major · B** — Link-preview scrapers (WhatsApp/iMessage/Slack/
  facebookexternalhit) may be 403'd by the same bot protection that blocks automation —
  would nullify the whole OG layer for a share-driven site. → One-time manual test: share
  the URL in WhatsApp/iMessage/Slack; check Cloudflare verified-bots exemption; also
  confirm www→apex 301 + https enforcement.
- [ ] **SEO-3 · Minor · A** — Legal page `<title>` drops the decided lockup
  (legal/index.html:6 "AETHON — Legal & privacy"). → "AETHON House — legal & privacy";
  same treatment gallery/404 (cosmetic, noindex).
- [ ] **SEO-4 · Minor · A** — `docs/seo-and-search.md` §5 still describes the pre-#52 meta
  state (poetic og:title) — a future editor would "restore" it. → Sync doc to shipped state.
- [ ] **SEO-5 · Minor · A** — WIP dialog text is first-in-DOM on indexable pages; Google
  can quote "AETHON is still being finished" as the SERP snippet. → Add `data-nosnippet`
  to `.wip-card` (zero visual change).
- [ ] **SEO-6 · Minor · B** — No OG block on legal; no description/OG on gallery — shared
  links render bare (noindex governs indexing, not previews; gallery is exactly the page
  people forward). → Minimal OG on both; B because owner may prefer the quiet page bare.
- [ ] **SEO-7 · Minor · B** — JSON-LD types the *website*, never the *thing*: a
  rule-compliant `about: { @type: Residence, addressLocality: Paphos }` node would attack
  the Almyra/House-of-Aion collision directly (zero new disclosure vs shipped geo tags);
  also make `alternateName` an array incl. plain "AETHON House". Never grow
  streetAddress/geo (guardrail).
- [ ] **SEO-8 · Nit · A** — Pre-wired social block lacks a commented `twitter:image:alt`
  (index.html:28–37). → Add now so activation day inherits it.
- [ ] **SEO-9 · Nit · A** — Future-image wiring templates say `alt="…"` (index.html:719,
  gallery:268) — that placeholder is what gets copy-pasted on photography day. → Pre-draft
  museal, entity-anchored alts in the comments (exact wording C, drafting A).
- [ ] **SEO-10 · Nit · A** — `lang="en"` on gallery/legal/404 vs decided `en-GB` on index.
  → en-GB everywhere.
- [ ] **SEO-11 · Nit · B** — sitemap has no `lastmod`; add only at the photography
  relaunch, and only if maintained truthfully.
- [ ] **SEO-12 · Nit · C** — Gallery `noindex, nofollow` → textbook would be `noindex`
  alone (page-level nofollow dead-ends its links back to / and /legal/). ~Nil impact;
  may express intent.

**Works (don't break):** title system shipped exactly; crawl layer textbook (robots
permits crawling the noindex gallery — required; sitemap = the 2 indexable URLs; slashes
match canonicals); machine layer honours guardrails (region-only geo, no address in
JSON-LD, no "luxury/for sale" anywhere); one h1/page; extractable "In brief" `<dl>` fact
block; credits' team links followed (backlink strategy intact); image-replacement patterns
cloak-safe; full favicon set = SERP-favicon eligible.

---

## BRD — luxury-brand strategist

**Verdict (short):** "the most disciplined private-residence brand work I've reviewed in
years" — the system holds from the travertine plate to the phone; Afterglow is a second
portrait, not a dark mode; the plan spread is the crown jewel. **The leak is at the
conversion**: the confirmation-email receipt is unannounced (silent list attrition) and
the only human channel is an outlook.com address. "The house has been given a voice; the
correspondence has not yet been given a desk."

- [ ] **BRD-1 · Major · C** — Thank-you never announces the confirmation email ("the real
  receipt"); filtered inboxes = people who believe they're on the list and aren't.
  → Add one sentence to `#register-thanks` (sign-off); verify DOI (pairs PRIV-2/PRIV-8).
- [ ] **BRD-2 · Major · C** — outlook.com is the only human channel, visible only in
  legal. → Recommend `mail@aethon.house` via Cloudflare Email Routing (free, forwards to
  the existing inbox; configure Outlook send-as), then surface it under the form + footer.
- [ ] **BRD-3 · Major · C** — No expectation of who replies / horizon → one private-office
  line, e.g. "Correspondence is read and answered personally." (sign-off)
- [ ] **BRD-4 · Minor · B** — **Logo letter-colour conflict:** shipped `brand/logo-dark.svg`
  letters are warm black `#222216`; styleguide memo + CLAUDE.md record olive `#4C5039`
  letters + gold dot. Physical reproductions would drift. → Reconcile against Oli's PDF;
  correct whichever is wrong. (Verify — was classed A by persona, held as B pending the
  PDF check.)
- [ ] **BRD-5 · Minor · C** — WIP card line "AETHON is still being finished" can read as
  *the house* being unfinished (brushes the no-under-construction guardrail; mildly
  contradicts "Completed in 2026"). → Proposed rewording for sign-off: "This site is still
  being finished — photography of the house is on its way. …"
- [ ] **BRD-6 · Minor · C** — Afterglow toggle (brand's best interactive moment) hides
  behind an unlabelled ☾. → Recommend one in-copy invitation at the end of *The interior*
  ("See the house in its evening — the small moon, above."), museal, where evening desire
  peaks.
- [ ] **BRD-7 · Minor · C** — The signature "walls slide back → one space" claim is buried
  mid-paragraph. → When photography lands: first pause plate = the open-threshold shot,
  caption owning the claim.
- [ ] **BRD-8 · Minor · C** — "SIGNGUARD APP LTD" jars at the moment of scrutiny.
  → Recommend softening clause "(the operating company of AETHON House)" via counsel
  batch; renaming/SPV = owner's cost call.
- [ ] **BRD-9 · Minor · C** — **Gold question (standing):** keep gold logo-only —
  reaffirmed with rendered evidence (the dot works because it's the only saturated point;
  ≈2:1 contrast kills UI use anyway). Sanctioned exceptions: physical gilding, future
  og-image. If it must travel: the "2026 · Renewed" timeline dot — and still advised
  against.
- [ ] **BRD-10 · Minor · C** — Footer uses whiteout (dot-less) mark while night header
  keeps the gold dot — the closing placement loses the signature. → Recommend footer =
  `logo-white.svg` ("on screen the dot is always gold"; whiteout reserved for one-colour
  physical).
- [ ] **BRD-11 · Minor · C→A overlap** — Subpage titles drop the lockup + `lang` drift
  (= SEO-3/SEO-10; conflict rule note: BRD + SEO agree — treat as A for title/lang).
- [ ] **BRD-12 · Minor · C** — Header bar mark + hero wordmark = same logotype twice in
  the first viewport (name ×3 with the descriptor). → Option: fade `.bar .mark` in with
  the existing `.scrolled` state, making the hero lockup ceremonial.
- [ ] **BRD-13 · Nit · C** — Two credit links point at Facebook/Instagram inside a museal
  colophon. → Keep (real presences + backlink play); upgrade to first-party sites when
  they exist; the ask itself nudges the backlink.
- [ ] **BRD-14 · Nit · C** — Motif saturation: "quiet" ×12, "warm" ×11, "light" ×15 —
  thin 2–3 "quiet"s in the next owner-reviewed voice pass only (never auto; don't re-open
  the kept items).
- [ ] **BRD-15 · Nit · C** — "Register interest" is the one estate-portal phrase; instantly
  understood though. → Default keep; quieter alternative for the button only: "Leave your
  name".
- [ ] **BRD-16 · Nit · C** — Gate-at-dusk scan lands on the Daylight theme. → Once
  afterglow pairs exist: option to default *first* visit to Afterglow after local sunset
  (toggle + stored preference always win). Prototype, don't ship blind.

**Works (don't break):** one mark/one system everywhere incl. the physical seam (plate →
first viewport); the plan spread; trust architecture (named team, the sketch artifact,
legal in brand voice, no socials reading as discretion); the refusal posture ("not a
listing… by invitation, in time"); Afterglow as brand asset; the quotable lines that
survive a WhatsApp forward.

---

## JRN — architectural journalist

**Verdict (short):** "Almost" coverable — high praise for a private house with no PR
machine. Reads as a small exhibition catalogue; the materials wall is magazine-ready, the
muted plans + Afterglow are the most distinctive rendering move, the toggle *is* the
architectural thesis. What blocks commissioning: **the 2026 renewal has no named design
author**, no maker's voice anywhere, and no door for a journalist to knock on. Prose is
one editing pass from excellent.

- [ ] **JRN-1 · Major · C** — The WIP notice says the *house* is unfinished: "AETHON is
  still being finished…" (index:678, gallery:224, legal:120) vs "Completed in 2026"
  (index:772). AETHON names the house everywhere else; drifts against the
  no-under-construction rule. → Reword (sign-off; converges with BRD-5): "This site is
  still being finished — the photography is on its way. …"
- [ ] **JRN-2 · Major · B** — The renewal has no design author: credits list "Renovation —
  G. Patsalides Construction & Renovation" (a contractor, index:1119); the architectural
  claim rests on Vardastudio's 2018 building; renewal reads contractor-led. → Establish +
  credit who directed the renewal *design* (row or naming sentence).
- [ ] **JRN-3 · Major · C** — "AETHON is the portrait of one seafront residence"
  (index:743) makes the name mean the *website*; 11 lines later it means the house
  (index:754). → Proposed: "This is the portrait of AETHON — one seafront residence…"
- [ ] **JRN-4 · Minor · C** — No route for editorial/press enquiries (only the sale form +
  legal email). → One colophon line: "Enquiries — <address>".
- [ ] **JRN-5 · Minor · B** — Not one sentence in a maker's voice (credits are names
  only). → Secure one restrained pull-quote (Vardas / Savva / Tan) for *The architecture*;
  also creates the backlink occasion SEO wants.
- [ ] **JRN-6 · Minor · C** — The parti is announced 3× in four sections (index:774,
  802/806, 871). → Let *The interior* open at its second clause.
- [ ] **JRN-7 · Minor · C** — "X, not Y / X rather than Y" cadence ×7 in *The
  architecture* alone (769–775; +805, 871). → Vary two (proposal in report; the kept
  "built, not furnished" stays).
- [ ] **JRN-8 · Minor · C** — "Gather" does three jobs (parti verb, fire-pit, palette) and
  Materials' title says "drawn" while its body says "gathered" (894 vs 897). → Reserve
  *gather* for the plan; palette "drawn" in both; fire-pit "holds the evening".
- [ ] **JRN-9 · Minor · C** — "…the sea" pile-up in *The garden* (841/850/854 — same
  participle 2×, 3× in one screen). → Vary one.
- [ ] **JRN-10 · Minor · B** — "ancient olive trees" (index:853) is the page's one
  testable adjective; memo + rest of site say "old/mature". → Verify provenance or align
  to "old olives".
- [ ] **JRN-11 · Minor · B** — The one Greek word "Αἴθων" (index:756) renders outside the
  brand typography (fonts subset latin-only) — system-serif fallback, worse on lean
  Android. → Option: 5-glyph Greek micro-subset woff2, or accept knowingly; test on
  devices.
- [ ] **JRN-12 · Minor · C** — "A Mediterranean lime, pressed like the sea." (index:923,
  gallery:365) inverts its image (the sea isn't pressed; the *surface* is wave-structured
  — the alt text has it right). → "…pressed into waves."
- [ ] **JRN-13 · Minor · C** — **Photography-day launch checklist:** "A curated selection,
  forthcoming…" (1016), "Photographs in time." (gallery:255), and the "· forthcoming"
  suffixes (737, 760, 792, 841, 859, 876, 884) must be rewritten/removed in the same
  commit as the images, or the finished monograph reads as awaiting itself.
- [ ] **JRN-14 · Minor · A** — `lang="en"` vs `en-GB` drift (= SEO-10/BRD-11). → en-GB ×4.
- [ ] **JRN-15 · Minor · C** — Serial-comma style mixed (Oxford in the locked hero,
  743, 871, gallery:255/300; absent index:806, 853 — two near-identical lists disagree).
  → Adopt Oxford as house style, one sweep (sign-off).
- [ ] **JRN-16 · Minor · C** — Chapter numbering stops at "06 · The material language";
  *Views* arrives unnumbered (CSS counter covers #place…#materials only, index:584–588).
  → Extend to 07 or accept the catalogue ending at Materials (pairs VIS-12).
- [ ] **JRN-17 · Minor · B** — "Sendinblue SAS" stale (= PRIV-5).
- [ ] **JRN-18 · Nit · C** — "the shining one" is the soft translation of Αἴθων (lexicon:
  "blazing, fiery"; Odysseus' alias in *Odyssey* 19). → "the blazing one", or keep and
  expect the letter to the editor.
- [ ] **JRN-19 · Nit · C** — "It lies along the coast from the Tombs of the Kings"
  (index:754) — idiom wants "just along the coast from" (one-word point, not re-opening
  the PR #36 sentence).
- [ ] **JRN-20 · Nit · C** — "You are warmly welcome to be in touch below." (index:1057)
  stacks two idioms; reads translated. → "You are welcome to leave a note below."
- [ ] **JRN-21 · Nit · C** — "The withdraw" as noun (gallery tracker + "V · The withdraw")
  — knowing coinage some subs read as error. → "The retreat", or keep with intent.
- [ ] **JRN-22 · Nit · A** — "Faros beach" (meta/OG/JSON-LD, index:7/23/47) vs "Faros
  Beach" (body, index:754). → Capitalise consistently (the SERP snippet is first-read
  copy).
- [ ] **JRN-23 · Nit · C** — Legal footer drops the Gallery link (legal:193–197) while
  other footers cross-link fully. → Add for a closed loop.
- [ ] **JRN-24 · Nit · C** — "Japandi" (index:773) is the one trade coinage that will
  date the text (standing decision to name it — for the record only, with an alternative
  phrasing filed).

**Works (don't break):** the materials wall (publishable as-is — never tidy it into a spec
sheet); the muted plans + afterglow halo; the Cliff Tan sketch as *artifact* (get more
artifacts; change nothing about this one); the colophon's plain honesty; sentence-level
voice discipline runs the full depth (incl. 404 and legal); the toggle as thesis.

---

## VIS — affluent QR visitor

**Verdict (short):** "the best thirty seconds of arrival I've had from a QR code" —
orientation solved inside one screen; the ask at the end is small, honest, safe-feeling
("I typed my details in without hesitation, which almost never happens"); would show the
spouse the Afterglow view tonight. Two flaws for someone like them: **the gallery
dead-ends the most-persuaded visitor**, and the thank-you may quietly lose their name
(confirmation-email seam). Attention thinned mid-*Architecture* and through the materials
wall (18 screens on a phone).

- [ ] **VIS-1 · Major · B** — The thank-you can be false: no-cors submit treats any
  completion as success; the confirmation-email step is never announced (converges
  PRIV-2/PRIV-8/BRD-1 — **four personas**); email field also accepts TLD-less typos
  (`type=email` allows `name@me`). → Verify Brevo DOI; surface "watch for a confirmation
  email" in `#register-thanks` (sign-off); consider a stricter email `pattern`.
- [ ] **VIS-2 · Major · C** — `/gallery/` ends at peak persuasion ("…by invitation, in
  time.") with **no path to register** — only "Back to the house" ×3 + "Legal"; on a phone
  that means re-scrolling ~13,000px. → One quiet "Register interest" link under the
  closing line (VIS outranks: high priority within C).
- [ ] **VIS-3 · Minor · A** — Gallery tap targets miss the homepage's mobile padding rule:
  footer "← Back to the house" 160×**14px**, "Legal" 43×**14px** (index's equivalent rule
  at ~:286 gives 32px); header "← The house" 80×21px. → Port the `@media (max-width:640px)`
  `.foot-meta a` padding to gallery (below WCAG 24px minimum as-is).
- [ ] **VIS-4 · Minor · A** — "Descend" scroll cue measures 116×**18px** at 390×844.
  → Invisible block padding (~12px) on `.scroll-cue`; no visual change.
- [ ] **VIS-5 · Minor · C** — First in-flow register affordance at ~83% of an 18-screen
  phone page (12,684px of 15,302px); overlay menu carries it but only if opened. → One
  quiet mid-page line (after *The plan* or *The garden*) pointing to the list (sign-off).
- [ ] **VIS-6 · Minor · C** — Afterglow undiscoverable for this demographic (unlabeled ☾;
  the placeholder badge that names Daylight/Afterglow disappears with photography).
  → Converges BRD-6; one subtle owner-approved hint.
- [ ] **VIS-7 · Minor · C** — Contact is form-only; the only address (legal) is consumer
  Outlook under a brand that owns aethon.house — "a small crack in the veneer".
  → Converges BRD-2/PRIV-7: `contact@`/`mail@aethon.house` aliasing the same inbox.
- [ ] **VIS-8 · Minor · C** — "A short and private list is kept" — by whom? SIGNGUARD APP
  LTD's relation to the house is never stated. → One clause ("the family company that
  keeps the house") pre-empts the only who-am-I-writing-to doubt (pairs BRD-8; counsel
  batch).
- [ ] **VIS-9 · Minor · C** — The one fact a serious prospect wants next: **bedrooms**.
  "Bedrooms — 3" in *In brief* discloses no price/address/area and saves every follow-up
  email. → Owner's call under the withholding strategy ("where withholding tips from
  graceful to effortful").
- [ ] **VIS-10 · Minor · C** — In the overlay menu, "Gallery" silently leaves the
  one-pager (four sibling links scroll; this one navigates; identical styling — lost their
  place mid-read). → Small distinguishing mark (arrow / separator group).
- [ ] **VIS-11 · Nit · C** — Desktop gallery chapter nav "I II III IV V VI" is cryptic
  (meanings hover-only, ~17×26px). → If meant to be used, too shy; consider labels on
  hover-independent surfaces.
- [ ] **VIS-12 · Nit · C** — Numbering stops mid-book (01–06 then unnumbered sections) —
  "I noticed the count just… ending" (= JRN-16).

**Works (don't break):** ten-second orientation genuinely solved (whole lockup inside the
first mobile fold, ~578px); the proportionate ask (2 required fields + optional note, 16px
inputs, honest framing, privacy link under the button); the trust chain (real facts, six
named practitioners, filled legal page); Afterglow superb once found (≥5.5:1 sampled night
contrast, plans' candle-glow halo, choice persists); fast where it matters (~218 KB first
load, zero console errors, instant on cellular at the gate); the overlay menu suits older
thumbs (27px type, ~58px rows, single olive CTA).

## DEV — web developer

**Verdict (short):** unusually healthy shipped code — statics near-perfect (no duplicate
IDs, no undefined custom properties, every href/src resolves, no orphaned images, zero
console errors / failed requests / h-overflow at 320–1920 both themes, full reduced-motion
compliance; WIP block sha1-verified byte-identical ×3). Risks cluster in recently shipped
interaction code: the mobile-drift cascade bug, missing modal scroll-lock, and the
occluded preview hero. Live PSI 100s predate the WIP/preview commits — re-measure.

- [ ] **DEV-1 · Major · A** — Mobile "no drift" rule defeated by cascade order: the
  `@media (max-width:640px)` `.hero::before{ animation:none }` (index:285) sits *before*
  the base `animation: drift 30s…` (index:304); equal specificity → later wins. Measured
  at 390px: `animationName:"drift", playState:running`. A 30s infinite animation on the
  battery-sensitive QR audience (currently also invisible → pure GPU cost, see DEV-3).
  → Move the block below :307 or raise specificity.
- [ ] **DEV-2 · Major · A** — Neither modal scroll-locks: with `#wip` open, wheel →
  scrollY 800, PageDown → 1587 (dialog still open); same for the lightbox. Native
  `<dialog>` inerts but doesn't block scroll; a swipe on the notice strands the mobile
  visitor mid-page after "Look around". → Lock scroll while a modal is open (mind the
  scrollbar shift: currently zero layout shift on open — preserve via
  `scrollbar-gutter:stable` or padding compensation; or reuse the menu's fixed-body
  pattern).
- [ ] **DEV-3 · Major · A** — Preview hero: drift layer fully occluded by `.hero-photo`
  (both z0; pseudo paints first) — screenshots 4s apart differ by **0 bytes** with the
  photo, 127k without; AND `body.preview .hero::before{ opacity:0.22 }` is dead because
  the `drift` keyframes animate `opacity` (computed 0.765). Will reproduce with the real
  hero photo per the in-code wiring instructions. → `z-index:1` on the drift layer in
  preview; drop `opacity` from the keyframes (transform only) so the damping applies.
- [ ] **DEV-4 · Minor · A** — Overlay menu never focuses its first link: `a.focus()` runs
  while `.menu`'s `visibility` transition still computes `hidden` → focus stays on the
  Close button (= A11Y-20, measured deterministic on open). → `requestAnimationFrame`
  before focus, or `visibility 0s` on open.
- [ ] **DEV-5 · Minor · A** — Menu close "whooshes": `window.scrollTo(0, scrollY)` under
  `scroll-behavior:smooth` animates ~700px on every mid-page close. →
  `scrollTo({top:scrollY, behavior:'instant'})`.
- [ ] **DEV-6 · Minor · A** — Form status silent + focus dropped (= A11Y-1, independently
  found). → `role="status"`/`role="alert"` + focus management.
- [ ] **DEV-7 · Minor · A** — Gallery placeholder glow hard-codes `#F2DDBE`
  (gallery:132–136) — ignores Afterglow; index's counterpart uses `var(--light-glow)` and
  adapts. Violates the role-token rule. → Add `--light-glow` (day+night) to gallery
  tokens and use it.
- [ ] **DEV-8 · Minor · A** — `.plates.trio` lead-plate sizing (flex/min-height/aspect
  auto, gallery:126–127) sits *outside* its `@media (min-width:680px)` block → at 390px
  the lead plate is arbitrarily taller (342×288 vs 342×228). → Move into the query.
- [ ] **DEV-9 · Minor · A** — No-JS mobile: dead "Menu" button (nav display:none, button
  renders, does nothing; = A11Y-14). The `.js` gate exists. → Show `.menu-btn` only under
  `.js` at ≤640px.
- [ ] **DEV-10 · Minor · B** — Live PSI 100s (2026-06-27) predate the WIP dialog +
  full-preview + logo commits (2026-07-02): new at first paint = full-viewport
  backdrop blur, top-layer dialog, all preview sections, the (bugged) mobile drift.
  → Trigger the seo-insights workflow after this batch and re-check mobile TBT/LCP.
- [ ] **DEV-11 · Minor · A** — `lang` drift (= SEO-10/JRN-14/BRD-11 — four personas).
  → en-GB ×4.
- [ ] **DEV-12 · Minor · B→A** — Legal `.foot-inner` max-width **64rem** vs 84rem on
  index/gallery — visibly narrower footer on wide screens; matches neither the site wrap
  nor legal's own 66rem column (reads as a typo). → Sync to 84rem after a visual check.
- [ ] **DEV-13 · Nit · A** — Legal no-flash script omits the `.js` class add (breaks the
  identical-block contract; traps a future `.reveal`); drops the `// sun : moon` comment;
  and no no-flash script syncs `theme-color` (night visitors see the day toolbar until
  end-of-body JS). → One-line syncs ×3.
- [ ] **DEV-14 · Nit · A** — Dead text-wordmark-era rules: `@media (max-width:360px)`
  styles `.wordmark`/`.bar .mark` letter-spacing/font-size on elements that are now
  image-replaced (index:370). → Delete.
- [ ] **DEV-15 · Nit · A** — CLAUDE.md fonts paragraph stale (still describes Jost as the
  display face; shipped = LT Museum ×2 + Spectral ×3). → Verify + update (may already be
  partially fixed — check before editing).
- [ ] **DEV-16 · Nit · C** — `100vw` full-bleed plates sit ~15px under classic desktop
  scrollbars (no scroll leak thanks to overflow-x:clip). Cosmetic; acceptable.
- [ ] **DEV-17 · Nit · C** — Repo-root working docs publicly served (= SEO-1); flagged so
  it stays a *conscious* decision as docs accumulate (this memo included).
- [ ] **DEV-18 · Nit · C** — `<strong>` on legal renders synthetic bold (no Spectral 700
  by design). Acceptable; or restyle within loaded faces.

**Drift table:** tokens/body.night/--space/@font-face metrics/WIP block/favicon set —
**PASS** (WIP sha1-identical ×3); theme-toggle IIFE near-pass (legal comment); no-flash
DRIFT (legal `.js`); footer width DRIFT (legal 64rem); `lang` DRIFT; reveal IO threshold
0.16 vs 0.12 (reads deliberate — C note).

**Works (don't break):** zero-defect baseline (console/network/overflow); airtight theme
system (round-trips everything incl. theme-color + plan shadow swap); anchors land exactly
at the bar's lower edge; lightbox complete (23 plates, keys, focus restore); honeypot +
native-POST fallback intact; lean weights (index 353KB fully scrolled incl. fonts;
gallery 104KB; legal 111KB; 404 39KB).

## A11Y — accessibility specialist (WCAG 2.2 AA)

**Verdict (short):** close to the AA claim and structurally better than most — both native
dialogs get trap/Esc/restore right, the overlay menu is "a model implementation", the
honeypot is properly neutralized, reduced-motion coverage is complete, 320px reflow +
text-spacing pass everywhere, and the readability audit's token numbers all reproduce
(5.1–14.8:1). **axe-core 4.12: 0 violations** — everything below is beyond axe's reach.
Three real risks: the form is silent for screen readers; focus is invisible at two key
moments; text-over-imagery has no guaranteed contrast floor (the F83 failure waiting for
photography day).

- [ ] **A11Y-1 · Major · A** — Form result never announced: `#register-thanks`/`#register-error`
  toggle `hidden` with **zero live regions on the page**; success also drops focus to
  `<body>` (index:1092–1097, JS:1274–1289). SR users hear nothing → re-submit or abandon.
  WCAG 4.1.3. → `role="status"` on thanks, `role="alert"` on error, `focus()` the
  thank-you.
- [ ] **A11Y-2 · Major · A** — Form fields suppress the focus ring: `input:focus…{
  outline:none }` (index:490); remaining cue = 1px underline hue-shift at **1.81:1
  day / 1.91:1 night**. WCAG 2.4.7. → Delete the `outline:none` (global ring passes
  6.1:1) or ≥3px focused underline.
- [ ] **A11Y-3 · Major · A** — Daylight focus ring invisible on the dark footer: olive
  `#565B3B` vs `#2C2620` = **2.10:1** (night 7.13 ✓); affects all footer links on every
  page. → Scoped `footer :focus-visible{ outline-color: var(--footer-ink) }` (12.1:1).
- [ ] **A11Y-4 · Major · A** — Gallery chapter tracker fails contrast both themes: idle
  `--ink-mute` at opacity .55 → **2.21:1 day / 2.68:1 night** at 11.5px
  (gallery:92). → Idle opacity ≥0.8 or drop the dimming (straight --ink-mute = 5.1:1).
- [ ] **A11Y-5 · Major · A** — Text over imagery has no contrast floor (measured over the
  shipped preview gradients, day: hero descriptor 3.38, tagline 3.48, orient 2.62,
  scroll-cue 2.92, media label 1.80; night descriptor 3.88; `.pause-label` 3.95 day;
  Views `--frame-label` down to 2.76 across the gradient). The hero scrim hook is 16%
  alpha — **the F83 failure waiting for photography** (the imagery brief itself warns).
  WCAG 1.4.3. → Strengthen the text-zone scrims in CSS now (guarantee ≥4.5:1 independent
  of image); re-sample per photo at delivery.
- [ ] **A11Y-6 · Minor · A** — No skip link anywhere; index costs WIP dialog + 8 header
  stops before content, gallery 9. WCAG 2.4.1. → Visually-hidden-until-focused "Skip to
  content".
- [ ] **A11Y-7 · Minor · A** — Lightbox slide changes unannounced (caption swaps, no live
  region; gallery:393–402). → `aria-live="polite"` on `.lb-cap`; consider "n of 23".
- [ ] **A11Y-8 · Minor · A** — `Αἴθων` (index:756) lacks `lang="el"` — SRs mangle it with
  English phonetics. WCAG 3.1.2. → `<em lang="el">`.
- [ ] **A11Y-9 · Minor · A** — Theme toggle mixes `aria-pressed` with a *swapping* action
  label → announces "Switch to the daylight view … pressed" (contradiction; index:694 +
  mirrors). → Fixed label "Afterglow view" + aria-pressed, or swapping label without
  pressed.
- [ ] **A11Y-10 · Minor · A** — Tracker links named bare "I"…"VI" (names only in mouse
  `title`; gallery:232–237). WCAG 2.4.4. → `aria-label="Chapter I — Arrival"` etc.
- [ ] **A11Y-11 · Minor · A** — Materials alt text duplicates the figcaption ×8
  (index:913–996) — every swatch announced twice. → Alts describe the *photograph* (macro
  texture) or `alt=""` and let captions speak.
- [ ] **A11Y-12 · Minor · A** — Fixed header overlaps reverse-tab focus targets (measured:
  a credits link 23px of 29px under the blurred bar). Sections have scroll-margin;
  focusables don't. → `a, button, input, textarea{ scroll-margin-top: 6rem }`.
- [ ] **A11Y-13 · Minor · C [WIP-dialog]** — The notice re-seizes focus on every load AND
  every internal navigation (3 dismissals to cross the site) — a real tax on keyboard/SR/
  cognitive users. Dialog itself is fully conformant. **Owner explicitly chose every-load
  (2026-07-02)** — filed as a revisit option: a `sessionStorage` once-per-visit gate keeps
  the notice, removes the repetition.
- [ ] **A11Y-14 · Minor · B→A?** — No-JS mobile renders a dead "Menu" button (and no nav;
  content still scrollable so no hard failure). → Hide `.menu-btn` unless `html.js` (the
  `.js` gate already exists). Verify then treat as A.
- [ ] **A11Y-15 · Minor · A** — 404 has zero landmarks (`body > h1/p/a`); also ignores a
  saved night preference (deliberately minimal — landmark wrap is still right). → Wrap in
  `<main>`; night support optional (C).
- [ ] **A11Y-16 · Nit · A** — Toggle border 2.96:1 sampled over the preview hero (3.31 on
  plain bg ✓; the 8.75:1 glyph carries it). Watch when photos land.
- [ ] **A11Y-17 · Nit · C** — Sub-44px vs the site's own convention: scroll-cue 116×18,
  tracker 17×26 (both pass 2.5.8 via spacing exception; everything else measured ≥44).
  → Padding bump aligns with house standard (= VIS-4 for the cue).
- [ ] **A11Y-18 · Nit · A** — "The minds behind the house" is a styled `<p>`
  (index:1116) — SR heading nav can't find the team credits. → `<h3 class="eyebrow
  credits-sublabel">`.
- [ ] **A11Y-19 · Nit · C** — `target="_blank"` external links (credits, sketch, DPA) have
  no "(opens in new tab)" cue (`rel="noopener"` ✓). Advisory, not an AA failure.
- [ ] **A11Y-20 · Nit · B** — Menu focus-on-open races the 450ms transition (keyboard-open
  → first link; mouse-open → Close button; trap holds either way). → `requestAnimationFrame`
  before `focus()` for determinism.

**Contrast table:** in the full report (task output); key failures only — focus ring vs
footer 2.10 (day), tracker idle 2.21/2.68, frame-label on gradient midpoint 3.95→2.76
(day), hero small text over preview media 1.80–3.48 (day) / 3.88–4.11 (night), input
focus-state change 1.81/1.91. Everything token-on-token passes 5.1–14.8:1 both themes.

**Works (don't break):** both modals genuinely right (native traps verified, focus
restore, 44×44 labeled ✕); the overlay menu (trap wrap, inert, scroll restore,
close-on-tap); honeypot properly neutralized (tabindex -1, aria-hidden, off-screen, not
reached in a 45-stop walk); motion/reflow clean (nothing animates under reduced-motion;
no h-scroll at 320px; text-spacing safe; 16px inputs); sound semantics (one h1/page, no
skipped levels, labeled navs, aria-current scroll-spy, counters read fine); forms
fundamentals (bound labels, autocomplete tokens, error by text not colour).

---

## Consolidated groups (all seven reports in; A-claims cross-verified 2026-07-03)

Verification notes: DEV-1/2/3, A11Y-2/3/4, VIS-3, PRIV-10, JRN-22, SEO-3, DEV-12 all
confirmed at the exact lines (contrast numbers recomputed — tracker needs opacity 1.0 in
day, not 0.85). **DEV-15 dropped as a false positive** (CLAUDE.md's "Jost" mentions are
historical — "LT Museum replaced Jost").

### Group A — implemented in this session's batch (see the fix commit)
Cross-file: **A-14** toggle aria (fixed label "Afterglow view" + aria-pressed, markup+JS ×3) ·
**A-22** `lang="en-GB"` ×4 (DEV-11/SEO-10/JRN-14/BRD-11) · **A-27** subpage titles get the
"AETHON House" lockup (SEO-3) · **A-28** `data-nosnippet` on `.wip-card` ×3 (SEO-5) ·
**A-3** modal scroll-lock (WIP dialog ×3 + gallery lightbox; fixed-body pattern, DEV-2) ·
**A-8** footer focus-ring override ×3 (A11Y-3) · **A-11** skip links ×3 (A11Y-6) ·
**A-17** focusable scroll-margin ×3 (A11Y-12) · **A-24** no-flash sync (legal `.js` +
theme-color early-set ×3, DEV-13).
index.html: **A-1** mobile drift specificity (DEV-1) · **A-2** preview drift z-index +
keyframes opacity removal (DEV-3) · **A-4/A-5** menu focus rAF + instant scroll restore
(DEV-4/5) · **A-6** form `role="status"/"alert"` + focus management (A11Y-1/DEV-6) ·
**A-7** drop input `outline:none` (A11Y-2) · **A-9** text-over-media contrast floor:
`--hero-wash` behind `.hero-inner`, day hero band lightened, day `--frame-label`
solidified (A11Y-5; **visual — owner may veto, screenshots in session**) · **A-13**
`lang="el"` on Αἴθων (A11Y-8) · **A-16** materials alts describe the macro, not the
caption (A11Y-11) · **A-25** dead wordmark rules deleted (DEV-14) · **A-26** "Faros
Beach" capitalised in meta/OG/JSON-LD (JRN-22) · **A-29** commented `twitter:image:alt`
(SEO-8) · **A-30** drafted alts in the two wiring comments (SEO-9) · **A-34** scroll-cue
hit-area padding (VIS-4) · **A-35** email `pattern` requiring a dotted domain (VIS-1
part).
gallery: **A-10** tracker idle opacity → 1 (A11Y-4) · **A-12** `.lb-cap`
aria-live (A11Y-7) · **A-15** tracker aria-labels (A11Y-10) · **A-19** `--light-glow`
token replaces hard-coded glow (DEV-7) · **A-20** trio rules into their media query
(DEV-8) · **A-33** mobile padding for footer/back links (VIS-3).
legal: **A-23** foot-inner 64→84rem (DEV-12) · **A-31** counsel comment stripped
(PRIV-10). 404: **A-18** `<main>` wrap + lang + title (A11Y-15).
index+gallery: **A-21** menu-btn behind `.js` gate (DEV-9/A11Y-14 — gallery has no menu
btn; index only). docs: **A-32** seo-and-search §5 synced to shipped meta (SEO-4).

### Group B — needs research / verification (who: owner ◦ / agent ●)
- [ ] **B-1 ◦** Cloudflare orange-cloud status (PRIV-1) → then notice names Cloudflare, or record "not proxied".
- [ ] **B-2 ◦** Brevo double-opt-in ON? + confirmation template wording (PRIV-2/VIS-1/BRD-1).
- [ ] **B-3 ◦** Link-preview bots not 403'd: share aethon.house in WhatsApp/iMessage/Slack; check Cloudflare verified-bots exemption; confirm www→apex 301 (SEO-2).
- [ ] **B-4 ●** Logo letter colour: shipped SVG `#222216` vs styleguide "olive `#4C5039`" — reconcile vs Oli's PDF (BRD-4). *Researched this session — see addendum below when done.*
- [ ] **B-5 ●** Re-run PSI/seo-insights workflow post-batch (DEV-10).
- [ ] **B-6 ◦** Renewal design author — who directed the 2026 design? (JRN-2) → credit row.
- [ ] **B-7 ◦** One maker pull-quote (Vardas/Savva/Tan) for *The architecture* (JRN-5).
- [ ] **B-8 ◦** "Ancient" olives provenance or align to "old" (JRN-10).
- [ ] **B-9 ●** Greek micro-subset woff2 for Αἴθων (JRN-11) — agent can build on request.
- [ ] **B-10 ◦** Brevo DPA/subprocessor check → notice entity/transfer wording (PRIV-5, lawyer batch).

### Group C — owner decisions (ranked; conflict rule applied)
1. [ ] **C-1 (VIS-2, top-ranked)** — a quiet "Register interest" path at the gallery's end.
2. [ ] **C-2 (VIS-1/BRD-1/PRIV-8 — 4 personas)** — thank-you announces the confirmation
   email. Proposed: "A short note of confirmation is on its way — it completes your
   registration."
3. [ ] **C-3 (JRN-1/BRD-5)** — WIP notice wording: "**This site** is still being finished —
   the photography is on its way. What you see is the shape of it; please, look around."
   (Current wording owner-approved 2026-07-02; two senior personas flag the house-unfinished
   misread.)
4. [ ] **C-4 (SEO-1/DEV-17)** — public internal docs on the domain: robots.txt disallow
   (/docs/, /scripts/, /*.md$) now, and/or move internals out of the published branch.
5. [ ] **C-5 (VIS-7/BRD-2/PRIV-7)** — mail@aethon.house via Cloudflare Email Routing;
   surface under the form + footer.
6. [ ] **C-6 (VIS-9)** — "Bedrooms — 3" row in *In brief*?
7. [ ] **C-7 (VIS-5)** — one quiet mid-page pointer to the list (after *The plan* or
   *The garden*).
8. [ ] **C-8 (VIS-6/BRD-6)** — Afterglow discovery line at the end of *The interior*.
9. [ ] **C-9 (VIS-10)** — mark "Gallery" as leaving the page in the overlay menu.
10. [ ] **C-10 (JRN-3)** — fix the "AETHON is the portrait" line (proposal filed).
11. [ ] **C-11 (JRN-4)** — a quiet enquiries line in the colophon (pairs with C-5).
12. [ ] **C-12 (JRN batch)** — copy-craft pass for sign-off: parti ×3 (JRN-6), "X not Y"
    density (JRN-7), gather/drawn (JRN-8), "…the sea" pile-up (JRN-9), "pressed into
    waves" (JRN-12), Oxford-comma sweep (JRN-15), "just along the coast" (JRN-19),
    "warmly welcome" (JRN-20), "The withdraw" (JRN-21), "blazing" (JRN-18), quiet-thinning
    (BRD-14), "Register interest"/"Leave your name" (BRD-15).
13. [ ] **C-13 (JRN-16/VIS-12)** — chapter numbering: extend to 07·Views or accept.
14. [ ] **C-14 (SEO-6)** — minimal OG on legal + gallery (shared-link previews).
15. [ ] **C-15 (SEO-7)** — JSON-LD `about: Residence` node + alternateName array
    (collision defence; locality-only).
16. [ ] **C-16 (BRD-9)** — gold stays logo-only: **reaffirm** (recommendation filed).
17. [ ] **C-17 (BRD-10)** — footer mark keeps the gold dot (`logo-white.svg`)?
18. [ ] **C-18 (A11Y-13)** — WIP notice: keep every-load (your explicit choice) or
    session-gate it (once per visit) for keyboard/SR comfort.
19. [ ] **C-19 (VIS-8/BRD-8)** — one clause relating SIGNGUARD APP LTD to the house
    (counsel batch, with PRIV-4/6/9 notice edits + PRIV-3 beacon rule).
20. [ ] **C-20 (BRD-12)** — hide bar mark until scrolled: **parked** — conflicts with
    VIS's praise of the first screen; conflict rule → VIS wins.
21. [ ] **C-21 (BRD-16)** — sunset-default Afterglow on first visit: prototype only,
    after photography.
22. [ ] **C-22 (JRN-13/A11Y-5)** — photography-day launch checklist: strip "forthcoming"
    labels + transitional lines in the same commit as the images; re-sample text-over-photo
    contrast per delivered image; re-check A11Y-16 toggle border over the real hero.
23. [ ] **C-23 (DEV-16/DEV-18/SEO-12)** — recorded as accepted quirks (100vw scrollbar,
    synthetic bold on legal, gallery nofollow) unless you say otherwise.
