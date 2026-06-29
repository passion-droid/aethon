# Fonts — licence

The web fonts in this folder are used under the **SIL Open Font License, Version 1.1**
(<https://scripts.sil.org/OFL>). The OFL permits bundling and serving the fonts with this
website.

- **LT Museum** — © 2024 LyonsType, with Reserved Font Name "LT Museum".
  Source: <https://lyonstype4.wixsite.com/lyonstype-beta> (the site serves subsets of the
  Medium + Bold weights, supplied for AETHON).
- **Spectral** — © The Spectral Project Authors (Production Type, for Google).
  Source: <https://github.com/productiontype/Spectral>

Only the `latin` subset (woff2) is included — **5 files**:
- `ltmuseum-lt.woff2` (LT Museum **Medium**) + `ltmuseum-bold-lt.woff2` (LT Museum **Bold**) — the
  display face: Medium for nav / labels / lockups, **Bold** for the section eyebrows. Declared as
  two weight ranges (`@font-face` `font-weight: 100 550` / `551 900`).
- `spectral-300-lt.woff2`, `spectral-300i-lt.woff2`, `spectral-400-lt.woff2` — three static
  Spectral faces (regular 300/400 + 300 italic), the body serif.

The `latin-ext` subset was dropped because the copy is basic-Latin only; if accented
Western-European text is ever added, regenerate it from the Google Fonts CSS. The full OFL
text accompanies each font at the sources above. Served locally so no visitor IP is sent to
a third-party CDN (GDPR).
