# Readability & Visual-Quality Memo — Standards + AETHON Targets

*Compiled June 2026. The yardstick for auditing AETHON's pages (desktop and mobile, day and night). General best-practice first; an AETHON-tuned layer at the end.*

## Purpose & how to use
This memo collects benchmarked, sourced targets for **readability, contrast, spacing/whitespace, font sizes, header/nav and section structure** — split **desktop vs mobile** — so we can audit `index.html` against concrete numbers rather than taste. Part A is the handful of anchors everything else derives from; Parts B–D are the targets by context; Part E is the do/don't checklist; **Part F translates it all into AETHON-specific targets and a current-state snapshot** for the audit that follows.

## Method & confidence
Five parallel research passes (typography; contrast/dark-mode; spacing/whitespace; header-nav/sections; mobile/responsive), then cross-checked. Sources weighted to authorities: **W3C/WCAG, WebAIM, Nielsen Norman Group, Google web.dev / Material Design, Apple HIG, Baymard, Butterick's Practical Typography, Smashing, A List Apart**. Direct page fetches were HTTP-403 in this environment, so figures come from cross-corroborated search extracts of those primary sources. **High confidence:** the WCAG ratios, the 16px/1.5/50–75-CPL anchors, Apple/Material platform numbers, the 8px grid. **Flagged soft (directional):** the "+20% comprehension from whitespace" figure (single 2004 study, second-hand), the sticky-header speed-ups (NN/g source unverified), exact reading-distance and thumb-zone percentages, and APCA's draft Lc thresholds.

---

## Part A — Universal anchors (memorise these five)
1. **Body ≥ 16px**, and 1.5× line-height is the readable floor (WCAG 1.4.12). For an editorial serif, 18–20px desktop reads better.
2. **Measure 50–75 characters per line, ~66 ideal**; hard cap 80 (WCAG 1.4.8). This sets the reading-column width.
3. **Contrast: 4.5:1 body, 3:1 large text, 7:1 = AAA/premium** (WCAG 1.4.3/1.4.6). Non-text/UI 3:1 (1.4.11).
4. **Spacing comes from one scale** (4/8px base) and is **uneven on purpose** — more above a heading than below; more between paragraphs than between lines.
5. **Each theme passes independently**, and **mobile is the harder constraint** — design to it, relax on desktop.

---

## Part B — Desktop targets

| Aspect | Target | Source / confidence |
|---|---|---|
| Body size | 16px floor; **18–20px** ideal for a serif at ~50–70cm reading distance | Butterick, NN/g, greadme — high |
| Body line-height | **1.5–1.75** (lean higher as the measure widens) | WCAG 1.4.12, Pimp my Type — high |
| Heading line-height | **1.1–1.2** (display can go ~1.05) | A List Apart, Pimp my Type — high |
| Type scale | base × **1.2–1.333** (editorial/confident band) | A List Apart — high |
| Measure | **~66ch** (50–75 CPL); cap the prose column ~**640–760px**, let media go wider | Baymard, Bringhurst — high |
| Section padding (vertical) | **~96–120px** for a calm site (Material default 64px; luxury sits higher) | Material + blog consensus — medium |
| Page gutters | grow with viewport (Material: 32dp→~200dp); text column stays capped, **margins absorb the width** | Material — high |
| Paragraph spacing | **~0.9–1.4em**, clearly greater than the line gap; don't indent *and* space | type refs — high |
| Heading space | **above ≈ 1.5–2× below** (the "floating heading" bug) | NN/g Proximity — high |
| Contrast | ≥4.5:1 body, ≥3:1 large; **aim 7:1** for a premium read | WCAG/WebAIM/Apple — high |
| Header | **64–80px**, logo top-left→home; static or sticky both fine; **shrink-on-scroll** good for a tall hero | NN/g — high (sizing); sticky %s soft |
| Nav | **keep visible** (don't hamburger desktop nav — ~39% slower, discoverability halved); ~5–9 self-evident items | NN/g — high |
| Scannability | front-load headings/eyebrows (F-pattern + layer-cake); one **h1**, sections **h2**, sub-beats **h3**, never skip levels | NN/g — high |
| Click targets | 24px comfortable for mouse; ~44px generous | WCAG 2.5.8 — high |

## Part C — Mobile targets

| Aspect | Target | Source / confidence |
|---|---|---|
| Body size | **≥16px** (Apple Body 17pt / Material 16sp); **form inputs ≥16px** or iOS auto-zooms on focus | Apple, Material, CSS-Tricks — high |
| Body line-height | **1.5–1.65** | WCAG 1.4.12 — high |
| Heading line-height | **1.15–1.25** (mobile headings wrap 2–3 lines) | type refs — medium |
| Type scale | same ratio, **smaller base** (compress); a 44px desktop h1 ≈ 28–32px mobile | learnui.design — medium |
| Measure | viewport − margins; accept **~35–50 CPL**; don't force 66 onto 360px, don't run edge-to-edge | Baymard — high |
| Section padding | **~40–64px** (desktop ÷ 2–2.5) | blog consensus — medium |
| Side margins | **≥16px** (Material floor); 20–24px for an airier feel | Material — high |
| Touch targets | primary controls **44–48px** (Apple 44pt / Material 48dp); **≥8px** apart; **WCAG 24px** is the floor, not the goal | Apple/Material/WCAG 2.5.8 — high |
| Thumb zone | primary action / submit in the **bottom-centre**; keep critical taps out of top corners | Smashing/NN/g — pattern high, %s soft |
| Header | lean (**~48–56px**), well under **~15% of viewport**; **hide-on-scroll** to reclaim space; un-fix in landscape/zoom (WCAG C34) | NN/g, W3C C34 — high (C34); 15% soft |
| Nav | hamburger acceptable but ~15% slower + halves discoverability — **prefer a "combo"** (1–3 visible items + a *labelled* "Menu", not icon-only) | NN/g — high |
| Fluid type | `clamp(min, pref, max)` with **max ≤ 2.5× min** (or 200% zoom fails WCAG 1.4.4) | web.dev, Smashing — high |
| Viewport | `width=device-width, initial-scale=1`; **no** `user-scalable=no` / `maximum-scale<2`; **no horizontal scroll at 320px** | MDN, Deque — high |
| Images | `srcset`/`sizes`, modern formats, lazy-load below fold; key images ideally **<100KB** for the QR/cellular arrival | MDN, web.dev — high |
| Performance | **LCP ≤ 2.5s** (75th pct); identity legible in **~10s**, first visual ~50ms | web.dev, NN/g — high |

---

## Part D — Contrast & colour (day + night) — applies to both viewports
- **Ratios are size-based, not device-based:** body **4.5:1**, large **3:1** (large = **≥24px, or ≥18.66px bold**), AAA **7:1 / 4.5:1**. Bias **above** the minimum for the mobile/outdoor-glare (QR-at-property) case.
- **Non-text/UI 3:1 (1.4.11):** buttons, **input borders**, **focus rings**, icons that carry meaning, and **toggle states** (the ☀/☾ switch) must clear 3:1 against adjacent colour.
- **Muted/secondary text floor:** **#767676 on white = exactly 4.5:1** — the lightest a small grey may go; go darker (#595959 ≈ 7:1) for comfort.
- **Links in text:** ≥3:1 vs surrounding text **plus a non-colour cue** (underline/hover) — colour alone fails 1.4.1.
- **Text over images:** add a **scrim** (warm-neutral, in AETHON's oyster/sand register) and verify the **busiest region** behind the text, not the average (F83).
- **Dark mode:** **avoid pure #000/#fff** — warm-dark base (Material #121212; AETHON #1A1410) with **off-white** body text; **desaturate + lighten the accent** on dark (Material 200–50 range) — this is exactly why AETHON's green is lighter at night. Pure white on near-black causes halation (worst for astigmatism).
- **Emphasis via opacity (Material):** light = primary 87% / secondary 54–60% / disabled 38%; dark = primary 100% / secondary 70% / disabled 50%.
- **Audit both themes separately** — passing day says nothing about night.

---

## Part E — Dos & don'ts (consolidated)
**Do**
- Anchor on 16px+ body / ~1.5 line-height / ~66ch, then derive headings from one ratio (1.2–1.333).
- Make spacing uneven on purpose; cap the prose column and let margins absorb extra desktop width.
- Use `clamp()` for fluid type with **max ≤ 2.5× min**; size all inputs ≥16px.
- Keep desktop nav visible; expose the active section with **`aria-current`** (not colour alone); keep anchors keyboard-focusable.
- Hit ≥4.5:1 body / ≥3:1 large + non-text; re-check **both themes**; scrim any text-over-image.
- Size primary mobile targets 44–48px, ≥8px apart; put the key action in the thumb zone.

**Don't**
- Don't run body past ~75–80 CPL or below ~16px; don't set mobile inputs <16px.
- Don't give headings equal space above/below; don't let paragraph spacing collapse toward the line gap.
- Don't over-space past ~**40%** whitespace (content fragments/disperses) — generous, not dispersed.
- Don't hamburger the desktop nav; don't rely on an icon-only menu or colour-only active state.
- Don't use pure black/white in dark mode or saturated accents on dark; don't push muted grey past its 4.5:1 floor.
- Don't disable zoom; don't let a fixed header eat >~15% of a mobile viewport.

---

## Part F — AETHON targets & current-state snapshot
AETHON's stack: **Jost** (display/labels) + **Spectral** (serif body), a `clamp()` fluid type system, a 60ch measure, role-token colours with a day/night theme. The numbers below are the general targets tuned to that stack, with AETHON's current values mapped against them. **This is the yardstick — the detailed pass/fix audit follows separately.** Legend: ✓ meets · ⚠ watch / examine in audit.

| Aspect | AETHON now | Target | Read |
|---|---|---|---|
| Body size | `clamp(1.02rem, .6vw+.95rem, 1.18rem)` ≈ **16.3→18.9px** | ≥16 mobile / 18–20 desktop | ✓ |
| Body line-height | **1.7** | 1.5–1.75 | ✓ (generous, suits the serif) |
| Fluid cap ratio | max/min = **1.16×** | ≤2.5× | ✓ |
| Measure | **60ch** (`p`, captions) | 50–75 CPL / 60–66ch | ✓ (slightly tight = premium) |
| Section padding | `clamp(5rem,12vw,11rem)` = **80→176px** | desktop ~96–140; mobile ~48–64 | ⚠ mobile floor **80px** and desktop **176px** both sit *above* the bands — likely fine for a museal site, but the audit should check it doesn't tip into dispersion (esp. mobile) |
| Gutters | `clamp(1.5rem,6vw,7rem)` = **24→112px** | ≥16 mobile, grow on desktop | ✓ |
| Section title (h2) | `clamp(1.6rem,3vw,2.3rem)` = **25.6→36.8px**, LH **1.25**, 1.6rem below | step-down scale, LH 1.1–1.25, asymmetric space | ✓ (space *above* comes from section padding) |
| Eyebrow / labels | Jost **~11.5px**, 0.32em tracking, `--ink-mute` | small caps OK if ≥4.5:1 | ⚠ legible but small — consider ~12–13px |
| Day body contrast | ink `#2C2620` on `#E9E7E0` ≈ **12:1** | ≥4.5 (aim 7) | ✓ |
| Day muted | `--ink-mute #6E675B` ≈ **4.5:1** | ≥4.5 | ✓ (at the floor) |
| Day accent | `#565B3B` on bg ≈ **5.75:1** | ≥4.5 | ✓ |
| Night body | `#EEE7D6` on `#1A1410` ≈ **14:1** | ≥4.5 | ✓ (off-white on warm-dark — correct) |
| Night muted / accent | `#9E9376` ≈ 6:1 · `#9CA279` ≈ 6.8:1 | ≥4.5 | ✓ (accent lighter on dark — correct) |
| Non-text contrast | toggle & input borders use `--rule-strong` (~**1.6:1** vs bg) | ≥3:1 (1.4.11) | ⚠ the border itself is low-contrast; the ☀/☾ glyph and labels carry identification, but consider strengthening the border / focus ring |
| Tap targets | toggle **35px** desktop / **44px** ≤640px | 44–48 primary mobile; 24 floor | ✓ (mobile 44; desktop mouse) |
| Inputs | **16px**, no `user-scalable=no` | ≥16px | ✓ (no iOS zoom) |
| Header | fixed, **~70px**, solidifies on scroll | 64–80 desktop; <15% mobile | ✓ (~12% on mobile; no hide-on-scroll = optional) |
| Desktop nav | **5 visible items** + `aria-current` scroll-spy | visible, 5–9, aria-current | ✓ |
| Mobile nav | **hidden, no menu** (<640px) | combo / labelled menu preferred | ⚠ acceptable for a short single-scroll page; audit to decide if a minimal anchor menu is worth it |
| Viewport / motion | `width=device-width, initial-scale=1`; `prefers-reduced-motion` + `:focus-visible` handled | required | ✓ |

**Hotspots the audit should focus on** (not conclusions yet): (1) mobile **section-padding floor** (80px) and desktop max (176px) vs the whitespace-dispersion bound; (2) **non-text 3:1** on the toggle/input borders and focus ring in both themes; (3) **eyebrow/label size** (~11.5px); (4) whether **mobile needs any nav**; (5) re-confirm every contrast pair in **night** mode, not just day.

---

## Sources
**Typography & readability** — Butterick's Practical Typography (point size / line length): https://practicaltypography.com/point-size.html · https://practicaltypography.com/line-length.html · Baymard, Optimal Line Length: https://baymard.com/blog/line-length-readability · NN/g, Serif vs Sans on HD screens: https://www.nngroup.com/articles/serif-vs-sans-serif-fonts-hd-screens/ · NN/g, Legibility/Readability/Comprehension: https://www.nngroup.com/articles/legibility-readability-comprehension/ · NN/g, Glanceable fonts: https://www.nngroup.com/articles/glanceable-fonts/ · A List Apart, More Meaningful Typography: https://alistapart.com/article/more-meaningful-typography/ · Pimp my Type, line length & height: https://pimpmytype.com/line-length-line-height/ · web.dev, fluid type: https://web.dev/articles/baseline-in-action-fluid-type · Smashing, accessible fluid type: https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/

**Contrast & dark mode** — W3C Understanding 1.4.3: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum · 1.4.11 Non-text Contrast: https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html · 1.4.1 Use of Color: https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html · F83 (text over images): https://www.w3.org/TR/WCAG20-TECHS/F83.html · WebAIM Contrast: https://webaim.org/articles/contrast/ · Material Dark theme: https://m2.material.io/design/color/dark-theme.html · Material text legibility: https://m2.material.io/design/color/text-legibility.html · Apple HIG Dark Mode: https://developer.apple.com/design/human-interface-guidelines/dark-mode · NN/g, Dark vs Light Mode: https://www.nngroup.com/articles/dark-mode/

**Spacing & whitespace** — Material spacing methods: https://m2.material.io/design/layout/spacing-methods.html · Material responsive grid: https://m2.material.io/design/layout/responsive-layout-grid.html · NN/g Proximity: https://www.nngroup.com/articles/gestalt-proximity/ · NN/g Whitespace: https://www.nngroup.com/videos/whitespace/ · Refactoring UI, too much whitespace: https://archive.org/stream/RefactoringUIStartWithTooMuchWhiteSpace/Refactoring%20UI%20-%20Start%20with%20too%20much%20white%20space_djvu.txt · Portent, less is not always more: https://portent.com/blog/content/less-is-not-always-more-how-too-much-white-space-can-harm-user-experience.htm · Bringhurst applied: http://webtypography.net/2.1.2

**Header, nav & sections** — NN/g Hamburger/hidden nav: https://www.nngroup.com/articles/hamburger-menus/ · NN/g, discoverable mobile nav: https://www.nngroup.com/articles/find-navigation-mobile-even-hamburger/ · NN/g F-pattern: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/ · NN/g Layer-cake scanning: https://www.nngroup.com/articles/layer-cake-pattern-scanning/ · W3C C34 (un-fix sticky): https://www.w3.org/WAI/WCAG21/Techniques/css/C34.html · Sara Soueidan, scrollspy + aria-current: https://www.sarasoueidan.com/blog/css-scrollspy/ · Miller's Law (Laws of UX): https://www.oreilly.com/library/view/laws-of-ux/9781492055303/ch04.html

**Mobile & responsive** — Apple HIG: https://developer.apple.com/design/human-interface-guidelines/ · Android touch targets: https://support.google.com/accessibility/android/answer/7101858 · Material touch target: https://m2.material.io/develop/web/supporting/touch-target · WCAG 2.5.8 Target Size: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum · 16px input/iOS zoom (CSS-Tricks): https://css-tricks.com/16px-or-larger-text-prevents-ios-form-zoom/ · MDN viewport: https://developer.mozilla.org/en-US/docs/Web/HTML/Viewport_meta_tag · web.dev clamp: https://web.dev/articles/min-max-clamp · NN/g Breakpoints: https://www.nngroup.com/articles/breakpoints-in-responsive-design/ · MDN responsive images: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images · web.dev LCP: https://web.dev/articles/lcp · NN/g First impressions: https://www.nngroup.com/articles/first-impressions-human-automaticity/
