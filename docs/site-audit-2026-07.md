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
- [ ] DEV report
- [ ] A11Y report
- [ ] Consolidation (dedupe, cross-verify A-claims, apply conflict rule)
- [ ] Group-A fixes implemented + deployed
- [ ] Group B researched
- [ ] Group C decided with owner

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
*(pending)*

## A11Y — accessibility specialist
*(pending)*

---

## Consolidated groups (built after all seven report)
*(pending — will list: **Group A** no-brainers to fix autonomously · **Group B** research
items · **Group C** owner decisions, deduped, with the conflict rule applied and each
A-claim cross-verified against the code before fixing)*
