# Presentation Builder

A portable agent skill for building **visually distinctive, browser-native, interactive presentations** from whatever content you supply. It synthesizes narrative-first slide design, precise diagrams, controlled motion, optional React/Three.js components, and real-browser QA. Its built-in starter deck is dependency-free and its REQUIRED **publishing output is exactly two files**: `presentation.html` (interactive/offline) and `presentation.pdf` (static 16:9, one page per scene).

## Files included

- `SKILL.md` — trigger, workflow, routing, and deliverable contract
- `references/` — narrative, art direction, visual/animation rules, component integration, explainer analysis, QA, source links
- `templates/interactive-deck/` — runnable themed demonstration with progressive reveals, SVG visualization, adjustable live diagram, chapter navigation and URL state
- `scripts/create_deck.py` — title/style-aware generator for fresh decks
- `scripts/check_deck.py` — Playwright HTTP/deep-link/screenshot/interaction test runner
- `scripts/preview_deck.py` — offline in-memory Chromium preview for restricted browser environments
- `scripts/export_deck.py` — inline all local runtime resources, print multi-page selectable-text PDF
- `scripts/verify_exports.py` — test finished HTML offline and inspect final PDF structure
- `examples/explainer-original/` — all 13 original user-provided files, copied without alteration

## Install

Extract the ZIP and copy the top-level **`presentation-builder` folder** to a skills directory recognized by your coding agent, e.g. `~/.agents/skills/presentation-builder/` for an agents-compatible environment or `~/.claude/skills/presentation-builder/` for Claude Code. The skill is a folder, not a standalone markdown file; preserve its relative paths.

Then ask your agent: **“Use presentation-builder to turn these notes into an interactive 12-slide technical explainer. Pick a vibrant editorial direction; include an explorable diagram and validate with Playwright.”**

## Quick authoring preview (not final delivery)

```bash
cd presentation-builder
python scripts/create_deck.py --title "A Better Way to Explain Ideas" --style signal --output ./my-deck
cd my-deck
python -m http.server 8000
# http://localhost:8000/
```

This optional development server is for the authoring preview only. Run `export_deck.py` to create the final **server-free single HTML and PDF**. Or directly serve `templates/interactive-deck/`. The starter supports `?slide=2&step=1&theme=explainer` for deep links. Theme selector: Signal, Explainer, Nocturne.

## Validation

```bash
python scripts/check_deck.py ./my-deck --out ./deck-qa
```

Requires Python Playwright and Chromium (`pip install playwright && python -m playwright install chromium` if missing). A screenshot contact sheet and report go in `deck-qa/`. In environments that block all browser URL navigation, run `python scripts/preview_deck.py ./my-deck --out ./deck-preview` for interaction/screenshots; that fallback cannot test actual URL/history restoration.

## Technology policy

No mandatory Node modules, internet access, or build process for the starter. The **agent** may upgrade a specific deck to Vite/React, shadcn/ui, 21st.dev, thinking-orbs, Three.js, or HyperFrames if a justified scene needs them. Attribution and license review are required for any third-party components copied into a deliverable.

The bundled explainer example is provided by the user and is not part of the third-party source projects. References summarize ideas and link to upstream skills; third-party repositories are **not** redistributed here.

## One-command publish (v2)

```bash
python scripts/create_deck.py --title "My Talk" --style signal --output ./working
# Edit working/index.html + styles.css + deck.js, then QA
python scripts/export_deck.py ./working --out ./deliverable
# Ship only deliverable/presentation.html and deliverable/presentation.pdf
```

Requires Python packages `playwright` and `pypdf` plus Chromium for publishing (see `references/EXPORT.md`). Then validate final artifacts with `python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf`. The HTML does **not** require Python, Node, or a server to view. The exporter inlines local CSS/JS/assets and rejects unresolved network/runtime dependencies. For source built in React/Vite/GSAP, first compile to browser assets and bundle a single JS entry before running the exporter. For every progressive reveal in the PDF, pass `--include-reveals`. The PDF is intentionally static.

### New integrations

- Official [GSAP skills](https://github.com/greensock/gsap-skills): labeled, seekable, performant animation timelines (optional runtime).
- [Design DNA](https://github.com/zanwei/design-dna): formal profile spanning design system, design style, and visual effects.
- [LottieFiles motion design](https://github.com/lottiefiles/motion-design-skill): intentional choreography, personality, timing and easing; optional Lottie assets.
- [Genjutsu](https://github.com/AThevon/genjutsu): art-direction and interaction theses, `cast` versus `paint` level of effort, visual review and audit.
- [Playwright skill](https://github.com/lackeyjb/playwright-skill): browser QA, accessibility-based interaction locators, screenshots, and verification. Already integrated, now explicitly gates HTML/PDF parity.

All are referenced as design/implementation guides; the skill does **not** copy their full code or require them as installed dependencies. See `references/` for integration decisions.
