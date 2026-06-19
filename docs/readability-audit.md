# Readability & Visual-Quality Audit — `index.html`

*Analytical audit, measured directly from the CSS. June 2026. Yardstick: [`readability-and-visual-quality.md`](./readability-and-visual-quality.md). Both themes, desktop and mobile.*

## Verdict
The page is in strong shape. **All text contrast passes** in both themes (most at AAA), type sizes / measure / line-height meet targets, the fluid caps are zoom-safe, and the mobile fundamentals (16px inputs, 44px toggle, viewport, reduced-motion, `:focus-visible`, `aria-current` scroll-spy) are correct. The audit found one genuine accessibility gap (non-text contrast on form/control borders) and one brand-judgment call (section padding), plus minor polish. All actioned items below are resolved in the accompanying change.

## What passes (measured)
**Text contrast — day** (bg `#E9E7E0`): body 12.1:1 · ink-soft 8.0:1 · accent 5.7:1 · muted 4.5→**5.1:1** (raised) · footer 12.1:1 / 6.7:1.
**Text contrast — night** (bg `#1A1410`): body 14.8:1 · ink-soft 10.5:1 · muted 6.0:1 · accent 6.8:1 · submit text 7.0:1 · footer 15.5:1 / 6.4:1.
- **Type:** body `clamp(1.02rem,.6vw+.95rem,1.18rem)` → 17.4px mobile / 18.9px desktop; line-height 1.7; h2 25.6→36.8px @ 1.25; measure 60ch ≈ 62–68 CPL desktop / ~36–42 mobile. All within target bands.
- **Fluid caps:** every clamp ≤ 2.5× min (wordmark 2.4× closest) — safe at 200% zoom.
- **Focus / active states:** `:focus-visible` ring and active-nav underline use `--accent` = 5.7:1 day / 6.8:1 night — pass non-text 3:1.
- **Header:** ~70px desktop (64–80 ✓), ~79px mobile (~12% of viewport, < 15% ✓); 5 visible desktop nav items, not a hamburger.
- **Mobile fundamentals:** inputs 16px (no iOS zoom); toggle 44px ≤640px; `width=device-width, initial-scale=1`, no `user-scalable=no`; no fixed-width elements that would overflow 320px.

## Findings

### 1 · [Medium — WCAG 1.4.11] Input & control borders failed non-text 3:1 — **resolved**
Measured at rest: `--rule-strong` border = **1.73:1 day / 2.41:1 night** (need 3:1). The form inputs were the real issue (the `border-bottom` is the field's only boundary). The ☀/☾ toggle shared the weak border but was rescued by its high-contrast glyph; focus already used `--accent` (passes).
**Resolution:** introduced a dedicated `--field-line` token — `rgba(44,38,32,0.55)` (**3.31:1** day) / `rgba(238,231,214,0.40)` (**3.33:1** night) — and applied it to the input underline and the toggle border. Decorative hairlines (`--rule` / `--rule-strong`: swatch frames, `.rule` divider) left unchanged — they're exempt and intentionally subtle.

### 2 · [Medium — judgment call] Section padding above the best-practice bands — **resolved (mobile only, per decision)**
Measured: `--section-y` = 80px mobile floor → ~176px desktop max. Memo bands: desktop 96–140, mobile 48–64.
**Resolution (keep desktop, reduce mobile):** lowered only the floor — `clamp(5rem,12vw,11rem)` → `clamp(3.5rem,12vw,11rem)`. Mobile sections now ~56px (in-band); the desktop maximum (176px) and the museal feel are unchanged.

### 3 · [Minor] Day muted text sat exactly at the 4.5:1 floor — **resolved**
`--ink-mute #6E675B` = 4.52:1 (zero margin; erodes under outdoor/mobile glare — the QR-at-property case).
**Resolution:** darkened to `#665F53` = **5.10:1** (5.44:1 on bg-soft). Affects eyebrows, form-note, scroll-cue, mat-note. Night muted unchanged (6.0:1).

### 4 · [Minor / optional] Eyebrows small (~11.5px) — **applied (conservative)**
Jost uppercase kickers; contrast fine, but small for mobile/older eyes.
**Resolution:** `.eyebrow` 0.72rem → **0.78rem** (~12.5px). Tracking unchanged. *(Aesthetic; easily reverted.)*

### 5 · [Minor / optional] Paragraph spacing tight against the 1.7 leading — **applied (conservative)**
`p` margin-bottom 1.2rem (~19px) under a ~32px line box.
**Resolution:** → **1.4rem** for clearer paragraph separation. *(Aesthetic; easily reverted.)*

### 6 · [Deliberate — no action] Mobile has no section nav
Below 640px the nav is hidden with no menu; only the toggle remains. Acceptable for a short, linear QR-arrival page (scrolling is the intended path). Revisit only if the page grows.

## Deferred / future
- **Hero & woven images (WCAG F83):** when real photos land, apply a scrim and re-check text over the *busiest* region — `--hero-band` is already the scrim hook.
- **Header translucency:** on-scroll bar is 82% opaque + backdrop-blur, so nav stays legible — not an F83 risk; no change needed.

## Change summary (this commit)
| # | Change | Before → After |
|---|---|---|
| 1 | New `--field-line` token on input + toggle borders | 1.73/2.41:1 → 3.31/3.33:1 |
| 2 | `--section-y` mobile floor | `5rem` → `3.5rem` (desktop max unchanged) |
| 3 | Day `--ink-mute` | `#6E675B` (4.52:1) → `#665F53` (5.10:1) |
| 4 | `.eyebrow` size | `0.72rem` → `0.78rem` |
| 5 | `p` spacing | `1.2rem` → `1.4rem` |
