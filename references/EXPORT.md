# Offline HTML and PDF export

Default deliverables are `presentation.html` and `presentation.pdf`. Keep authoring modules, test reports, rendered previews, and source assets in the project workspace. An explicit user request can change the output contract.

## Export flow

Use the Python environment prepared in SKILL.md. Commands here run from the skill root; an installed agent should invoke the same scripts by absolute path.

```bash
python scripts/export_deck.py ./my-deck --out ./deliverable
python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf
python scripts/render_pdf.py ./deliverable/presentation.pdf --out ./pdf-review
```

- `--include-reveals` prints every progressive state. The exporter records this mode in the HTML and the verifier checks the corresponding PDF page count.
- `--theme signal|explainer|nocturne` overrides only the PDF theme for starter-based decks.
- `--browser /path/to/chromium` selects a browser executable for export, QA, preview, and verification.
- `--out` must differ from the source directory. Only the two expected filenames are replaced. Failed bundling or rendering preserves previous deliverables.
- Browser packages and Chromium must be installed once; the finished HTML does not need Python, Node, or a server.

## Bundler scope

The bundler supports a trusted `index.html` with quoted local stylesheet/script references, simple CSS imports, CSS `url()` assets, inline CSS, and local images, posters, audio/video, and icons. Paths must remain inside the deck directory. It embeds assets as data URLs and retains HTML text/SVG for browser printing.

It rejects remote runtimes, missing files, escaping paths, unsupported CSS imports, unresolved module imports, unsupported `srcset`, unresolved resource attributes, and local literal `fetch()` paths. Resource requests are blocked and reported during PDF export. Runtime-created URLs and unusual HTML/JS syntax are not universally discoverable statically: visit every reveal, test custom widgets, and run the standalone verifier. External citation links are allowed; they are links for the reader, not offline runtime assets.

SVG symbols should preferably be inline. Small SVG, raster images, and font files are appropriate. Large embedded video/model assets increase HTML size; choose compressed assets and tell the user when size affects sharing. Preserve required third-party notices inside the HTML when copying code or assets.

## Optional compiled frameworks

For React/Vite/GSAP/Three.js/Lottie, compile first. Configure relative asset paths (`base: './'` for Vite), one entry bundle, and no dynamic chunks. Bundle library code and embed data/model/texture/worker dependencies. The exporter is not a module resolver and cannot turn an arbitrary Vite build into a standalone application by itself. Inspect `dist/index.html` and the built JS before exporting the `dist/` folder.

Remote HDRIs, CDN decoders, network fonts, and registry components that fetch assets need local embedded replacements. A library being installed in Node does not make its browser assets offline. Runtime licensing is separate from the bundled reference documentation.

## Custom controller contract

Expose this interface before browser QA/export starts:

```js
window.__presentationExport = {
  frames: () => [
    { index: 0, steps: 3, title: 'Opening' },
    { index: 1, steps: 1, title: 'Result' }
  ],
  goto: async (sceneIndex, revealIndex) => {
    // Render the requested scene/reveal and resolve after framework state commits.
  },
  freeze: async () => {
    // Pause continuous animation; draw a meaningful canvas/video/3D still.
  }
};
```

Indices are consecutive and zero-based; `steps` is a positive integer. `frames()` is synchronous. `goto()` and `freeze()` may return promises. Direct seeking must not depend on earlier interactions. Each `goto()` must restore the intended representative widget state; `freeze()` must be safe to repeat. Custom controllers should also supply navigation/widget assertions with `--interaction-test` for QA.

Render each scene inside `#stage`, a 1600×900 element scaled uniformly to fit the viewport. Custom CSS should preserve this 16:9 contract. Print CSS hides navigation and nonessential controls and supplies any widget explanation needed in the static version. The exporter removes stage transforms and prints at 1600×900px (1200×675pt). For a different canvas contract, adapt and validate the exporter explicitly.

The starter's `__deckDebug` is a compatibility fallback. Prefer the public `__presentationExport` interface for new controllers.

## Review and limitations

The verifier opens the actual `file://` HTML with network access blocked, visits every reveal, checks image loading and stage bounds, tests starter keyboard/deep links, and compares PDF page count and aspect ratio. It requires some extractable PDF text but permits short and image-only individual slides. It cannot judge visual quality or prove unexercised widgets work.

Open every PNG produced by `render_pdf.py`; compare conclusions, charts, and representative widget states to the HTML. The PDF is static and cannot preserve sliders, live animation, or 3D exploration. Browser printing preserves vector text/SVG where supported rather than turning each page into a screenshot.

If file/HTTP navigation is blocked by the host, `verify_exports.py --in-memory` and `preview_deck.py` provide explicit fallbacks. Report that native opening and history were not verified; do not present fallback tests as full validation.
