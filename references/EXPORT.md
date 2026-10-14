# Shipping contract: ONE HTML + ONE PDF

**Only final deliverables:** `presentation.html` and `presentation.pdf`. This is the overriding requirement for every generated presentation. Keep any React/Vite modules, assets, source images, references, design-DNA JSON, screenshots, or test reports in a separate authoring workspace, not in the publication folder. Never return a multi-file runtime site as the completed deck.

## Export flow

```bash
# Start from the installable skill root.
python scripts/create_deck.py --title 'The subject' --style signal --output ./working-deck
# Edit working-deck/index.html, working-deck/styles.css, working-deck/deck.js.
python scripts/check_deck.py ./working-deck --out ./internal-qa
python scripts/export_deck.py ./working-deck --out ./deliverable
python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf
# Required: deliverable/presentation.html and deliverable/presentation.pdf
```

The exporter needs **Python Playwright** and **pypdf**, plus a Chromium installation:

```bash
python -m pip install playwright pypdf
python -m playwright install chromium
```

If Playwright cannot launch its browser, provide `--browser /path/to/chromium`. For optionally validating the PDFs visually, install PyMuPDF (`pip install pymupdf`) or use standard PDF renderers such as `pdftoppm`.

- `--include-reveals` creates a PDF page for **every** progressive state, useful for self-study handouts (the default is just each scene's final reveal).
- `--theme signal|explainer|nocturne` selects the *PDF's* visual theme; the HTML theme remains interactive.
- `--out` must differ from the editable source folder. The exporter creates or replaces only these two expected filenames.

## Offline bundler behavior

`export_deck.py` embeds local CSS, JS, and media (`img`/audio/video/source/poster/icon and CSS `url()` fonts/images) into a self-contained HTML. Source should be organized into external local files while authoring. The exporter **fails closed** for remote JS/CSS and unsupported CSS imports, local `fetch()` URLs, unresolved JS imports, and missing local files rather than silently delivering a broken offline artifact. Image/media source code included as JS string data must be embedded by your build system; the generic HTML bundler cannot discover runtime-created network URLs.

**React/Vite/GSAP/shadcn/21st.dev/Three.js/Lottie:** first run a production compiler (`npm run build`) configured for a single JS entry and one CSS output; then point the export script at the compiled `dist/` directory, after checking that it contains a usable `index.html`. Disable code splitting/async imports or implement a complete single-file bundling strategy in the source build. Compiled JS must not retain `import()` or unresolved import/export statements, and external fonts/models/worker files should be embedded. Source components can use multiple files; **published** HTML cannot depend on them.

**Large embedded assets:** data URIs can inflate `presentation.html`. Prefer SVG, compressed raster images, small 3D meshes and small local videos; reject oversized content rather than weakening offline portability. A multimedia presentation may reasonably be tens of MB, but call out the size.

## Export interface for custom deck controllers

The bundled starter exposes `window.__deckDebug` for the PDF exporter. Custom frameworks should instead implement:

```js
window.__presentationExport = {
  frames: () => [
    { index: 0, steps: 3, title: 'Opening' },
    { index: 1, steps: 2, title: 'Explanation' }
  ],
  goto: (sceneIndex, revealIndex) => { /* synchronously render exact stage state */ },
  freeze: () => { /* pause GSAP/video/Lottie/Canvas/3D at meaningful still */ }
};
```

Your `goto()` must support direct access to all states, without relying on a prior click history. `freeze()` must be idempotent; it runs on every PDF frame. The final HTML runs without this API being invoked until export.

## PDF semantics

- Default: **one PDF page per scene**, frozen at the final reveal. Complex interactive widgets may use a chosen representative state; annotate their state in the PDF, and do not claim interactive PDF support.
- Browser print retains vector text and SVG where possible; individual Chromium PDF pages are merged into one multi-page PDF (16:9, 1200×675pt for a 1600×900px stage).
- Scene CSS uses `@media print` and reduced-motion support. Avoid printing a still-invisible animation frame, video fallback without poster, or tooltip-only explanations.
- PDF export is **browser-based**, not a pixel screenshot pasted into a slide; confirm the result has readable, extractable text.

## Quality gates

1. Check single HTML opens offline (use a real local browser when accessible) and all chapters, controls, keyboard reveal, sliders and themes work.
2. Assert no external `<script>` / stylesheet, image URLs, CSS URL loads, local fetch paths, or residual module imports remain. The code-level check is necessary but not a substitute for network-blocked runtime testing.
3. Render the PDF to images and inspect **every** page: no clipping, missing fonts, missing visuals, blank first frames, or invisible progressive content.
4. Verify page count and each PDF page aspect ratio; compare its conclusion to the final HTML reveal.
5. If HTTP/file navigation is administratively blocked, in-memory browser testing can still validate visuals/interactions; specifically disclose that native file-opening and browser history/deep links were **not** verified.
