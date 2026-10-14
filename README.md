# Presentation Builder

An agent skill for making distinctive interactive presentations that work offline. Give your agent notes, documents, a topic, or an existing deck. It builds a browser-native presentation and a static 16:9 PDF, then checks the result in Chromium.

The package includes a working starter, 23 curated upstream guides, export and review tools, and a four-chapter technical explainer example. No other skills, paid services, or JavaScript framework are required for the default workflow.

## Install

Once this repository's release files are pushed to GitHub:

```bash
npx skills add zacharybinger/presentation-builder --skill presentation-builder
```

Add `--global` for a user-wide installation or `--agent codex` / `--agent claude-code` to select an agent. These options follow the [official skills CLI](https://github.com/vercel-labs/skills#install-a-skill). The installer copies the skill resources; it does **not** install Python dependencies or Chromium.

For a local checkout:

```bash
npx skills add ./presentation-builder --skill presentation-builder
```

You can also copy the entire folder into your agent's skills directory. Keep `SKILL.md`, `references`, `scripts`, `templates`, and `examples` together. The local `resources/` research clones are unnecessary and excluded from distribution.

## Use

> Use presentation-builder to turn these notes into a 12-slide technical explainer. Use a bold editorial style, a diagram I can explore, and a static PDF companion. Validate the finished files.

More starting points are in [examples/PROMPTS.md](examples/PROMPTS.md). The default outputs are `presentation.html` and `presentation.pdf`. Open the HTML in a browser. Arrow keys/Space navigate, Home/End jump, and F toggles fullscreen. The PDF contains each scene's final reveal, with an option to include every reveal.

This skill creates HTML and PDF. Native editable PowerPoint and Google Slides need another authoring workflow. A projector-style 16:9 deck scales to a phone but is best read on a larger screen.

## Local authoring and export

Requirements: Python 3.10+, the packages below, and Playwright Chromium. Node/npm is needed only for `npx skills` or optional JavaScript integrations. Viewing the finished HTML requires only a modern browser.

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python scripts/create_deck.py --title "My Talk" --style signal --output ./my-deck
# Edit my-deck/deck.js and my-deck/styles.css.
.venv/bin/python scripts/check_deck.py ./my-deck --out ./deck-qa
.venv/bin/python scripts/export_deck.py ./my-deck --out ./deliverable
.venv/bin/python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf
.venv/bin/python scripts/render_pdf.py ./deliverable/presentation.pdf --out ./pdf-review
```

On Windows use `.venv\Scripts\python.exe`. Linux may need browser system libraries: `python -m playwright install --with-deps chromium`. Browser tools accept `--browser /path/to/chromium` except the PDF renderer, which uses PyMuPDF.

Inspect the QA screenshots and every rendered PDF page. Add widget-specific checks with `--interaction-test path/to/deck_interactions.py`; the bundled `scripts/starter_interactions.py` tests the original example. Export with `--include-reveals` for a PDF of every progressive state. The verifier detects that mode automatically.

The starter needs no build process. Optional React, GSAP, Lottie, and Three.js routes require their own libraries and bundling; see [EXPORT.md](references/EXPORT.md). The exporter embeds supported local CSS, scripts, fonts, and media, blocks network requests during printing, and rejects unresolved resources. It is a packager for trusted authoring input, not a general JavaScript compiler. QA covers exercised states; custom widgets still need appropriate assertions.

## What's included

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent entrypoint and workflow |
| [references/RESOURCE_LIBRARY.md](references/RESOURCE_LIBRARY.md) | Task-based index of 23 bundled guides from nine upstream projects |
| `references/` | Story, art direction, diagrams, motion, integration, export, and QA |
| `templates/interactive-deck/` | Five-scene starter with three themes, progressive reveals, inspector, and slider |
| `scripts/` | Scaffold, browser QA, offline bundling, PDF export/rendering, package validation |
| `examples/explainer-original/` | Original interactive neural-network teaching prototype, retained as an example |
| `agents/openai.yaml` | Optional agent UI metadata |

## Maintaining and releasing

```bash
.venv/bin/python scripts/validate_skill.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/smoke_test.py
.venv/bin/python scripts/package_skill.py --out ./dist/presentation-builder.zip
```

CI runs these checks from a fresh checkout. The package command uses an explicit file list and validates relative links and vendored hashes. It excludes research clones, generated decks, caches, tests, and CI files. The archive contains one `presentation-builder/` directory with everything needed by the skill. Publish the repository files to enable the GitHub install command above; no npm package is needed.

Upstream snapshots are pinned in [manifest.json](references/upstream/manifest.json). To update a guide, review its new source and license, preserve the scope/provenance header, and update its revision, source hash, vendored hash, and license hash. Do not copy upstream skill entrypoints under a second `SKILL.md` name.

## License and credits

Original project material is under [MIT](LICENSE). Bundled upstream excerpts retain their own licenses and copyright notices; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). [SOURCES.md](references/SOURCES.md) records inclusion decisions and material kept as links only. Guidance licenses do not automatically cover optional runtime libraries, fonts, or images.
