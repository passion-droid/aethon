# Fonts — licence

The web fonts in this folder are used under the **SIL Open Font License, Version 1.1**
(<https://scripts.sil.org/OFL>). The OFL permits bundling and serving the fonts with this
website.

- **Jost** — © The Jost Project Authors. Source: <https://github.com/indestructible-type/Jost>
- **Spectral** — © The Spectral Project Authors (Production Type, for Google).
  Source: <https://github.com/productiontype/Spectral>

Only the `latin` subset (woff2) is included — **4 files**:
- `jost-lt.woff2` — Jost is a **variable font** (wght 100–900); one file serves every weight
  the site uses (300/400/500) via a single `@font-face { font-weight: 100 900 }`, so the
  browser downloads it once. (It was previously committed three times under
  `jost-300/400/500-lt.woff2` — identical bytes — which made a multi-weight page fetch it up
  to 3×; deduped.)
- `spectral-300-lt.woff2`, `spectral-300i-lt.woff2`, `spectral-400-lt.woff2` — three static
  Spectral faces (regular 300/400 + 300 italic).

The `latin-ext` subset was dropped because the copy is basic-Latin only; if accented
Western-European text is ever added, regenerate it from the Google Fonts CSS. The full OFL
text accompanies each font at the sources above. Served locally so no visitor IP is sent to
a third-party CDN (GDPR).
