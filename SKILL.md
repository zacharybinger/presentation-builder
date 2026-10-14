---
name: presentation-builder
description: Create, redesign, and validate distinctive interactive HTML presentations from notes, documents, a topic, or an existing deck. Use for browser-native talks, pitch decks, technical explainers, and progressive diagrams. Exports a self-contained offline HTML deck and a static 16:9 PDF. Use another workflow for native editable PowerPoint or Google Slides.
license: MIT
metadata:
  version: "2.0.0"
---

# Presentation Builder

Deliver a finished presentation with a coherent story, distinctive visual direction, and working interactions. Default deliverables are `presentation.html` and `presentation.pdf`; follow an explicit user request for different formats or scope. The starter and all core guidance are bundled here. Other skills, online component registries, and paid services are optional.

Read only the references needed for the current task. Paths below are relative to this skill's installed directory. Run helpers by their absolute installed paths; put generated work in the user's project, not inside the installed skill.

## 1. Choose the route

- **New talk or pitch:** establish the audience and takeaway, structure the story, select art direction, build, then review.
- **Existing deck:** inspect content and behavior first. Preserve facts, brand, and working controls unless the brief asks to change them.
- **Technical teaching:** use a persistent visual model and progressive reveals. Read [EXPLAINER.md](references/EXPLAINER.md). The [bundled prototype](examples/explainer-original/STYLE_GUIDE.md) demonstrates this pattern; its subject, claims, and styling are examples.
- **Static speaking deck:** use the same export flow with little or no interaction. A one-slide request means one slide; no automatic cover or conclusion.
- **Video companion:** read the video recipe in [RECIPES.md](references/RECIPES.md) only when requested. A video does not retain live controls.

For core authoring, use HTML/CSS/SVG and the [interactive starter](templates/interactive-deck/index.html). Choose React, GSAP, Lottie, or Three.js only when a scene benefits from them. Their runtimes are not bundled; see [STACK_AND_COMPONENTS.md](references/STACK_AND_COMPONENTS.md) and [RECIPES.md](references/RECIPES.md) for optional integrations.

## 2. Establish the story

Use supplied content as factual ground truth. Extract the audience, purpose, evidence, requested duration/slide count, brand, and desired audience action. Proceed with reasonable secondary assumptions; ask only when a missing answer would change the result. Research when needed for accuracy, and retain source links with the relevant claim.

Read [STORY.md](references/STORY.md). Before coding, outline each scene's purpose, evidence, visual, and reveal states in the authoring workspace. A plain topic title is appropriate for setup; use a takeaway title when the evidence establishes a finding. Each reveal should introduce a relationship, comparison, cause, or result. Keep units, uncertainty, and caveats that affect interpretation. Label invented demonstration data as illustrative.

## 3. Define the visual direction

Read [ART_DIRECTION.md](references/ART_DIRECTION.md) and [DESIGN_DNA.md](references/DESIGN_DNA.md). Derive the visual language from the subject or supplied reference. Choose ground/ink colors, semantic accents, typography, grid, image/diagram treatment, and one characteristic transition. Keep a small design profile in the authoring workspace; encode it into the deck's styles.

When the user is exploring, show a few actual visual directions. When asked to produce immediately, choose and continue. Vary composition with the story instead of repeating identical card grids. Keep concept colors stable across scenes, ensure strong contrast, and shorten copy before shrinking type.

The starter includes `signal`, `explainer`, and `nocturne` themes; these demonstrate tokens, not limits on design. For more options, read the [local resource index](references/RESOURCE_LIBRARY.md): it routes to bundled typography, color, style presets, diagram geometry, and motion recipes. Upstream website conventions are reference material, not universal presentation requirements.

## 4. Build the presentation

Set `SKILL_DIR` to this skill's actual installed path. Python 3.10+ is required for the helpers. Scaffolding uses the standard library; browser QA and export need the packages in [requirements.txt](scripts/requirements.txt) and Chromium. Install them in a virtual environment if missing; do not install into a managed system Python.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "$SKILL_DIR/scripts/requirements.txt"
.venv/bin/python -m playwright install chromium
.venv/bin/python "$SKILL_DIR/scripts/create_deck.py" \
  --title "My Talk" --style signal --output ./my-deck
```

On Windows use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

Replace demonstration content in `my-deck/deck.js`; adapt layout and tokens in `styles.css`. The controller supports arbitrary scene/reveal counts, a slide picker for long decks, accessible controls, and `?slide=N&step=M&theme=...` links (one-based URL values). Arrow keys/Space move through reveals, Home/End jump, and F toggles fullscreen. Inputs consume their own keyboard events.

For motion, read [VISUALS_AND_MOTION.md](references/VISUALS_AND_MOTION.md) and [MOTION_ENGINE.md](references/MOTION_ENGINE.md). Use motion to explain state changes. Each widget needs visible output, a meaningful reset, and keyboard access. Reduced motion must show the same information. Preserve text equivalents for charts and diagrams. Optional canvas/3D/video scenes need a meaningful PDF still.

For a custom controller, implement the async-capable export interface and `#stage` sizing contract in [EXPORT.md](references/EXPORT.md). Direct access to any scene/reveal must work without replaying earlier clicks.

## 5. Review in a real browser

Read [QA.md](references/QA.md). Run:

```bash
.venv/bin/python "$SKILL_DIR/scripts/check_deck.py" ./my-deck --out ./deck-qa
```

The generic checker visits every reveal, checks stage/text bounds and browser errors, captures each completed scene, and checks several viewport sizes. For the starter controller it also tests keyboard navigation, deep links, and browser back/forward. Add task-specific widget assertions with `--interaction-test ./deck_interactions.py` or test those widgets manually. [starter_interactions.py](scripts/starter_interactions.py) is an example for the original demo only.

Open every screenshot. Check line breaks, label collisions, contrast, missing media, chart meaning, content coverage, and composition. A passing script is not a visual review. Fix observed problems and rerun affected checks. Use [preview_deck.py](scripts/preview_deck.py) only if URL navigation is blocked, and disclose which navigation/widget checks remain untested.

## 6. Export and deliver

Read [EXPORT.md](references/EXPORT.md). Keep authoring sources, screenshots, and reports outside the deliverable folder.

```bash
.venv/bin/python "$SKILL_DIR/scripts/export_deck.py" ./my-deck --out ./deliverable
.venv/bin/python "$SKILL_DIR/scripts/verify_exports.py" \
  ./deliverable/presentation.html ./deliverable/presentation.pdf
.venv/bin/python "$SKILL_DIR/scripts/render_pdf.py" \
  ./deliverable/presentation.pdf --out ./pdf-review
```

The HTML embeds its runtime assets and opens without a server or network. The default PDF captures one completed state per scene with selectable text; `--include-reveals` captures every reveal instead. Review every rendered PDF page, including any frozen widgets. For a compiled React/Vite deck, first bundle dependencies, data, fonts, models, and media into local assets as described in EXPORT.md. Unsupported runtime imports or unresolved assets must be fixed before delivery.

Return links to the two completed files, a short description and navigation instructions, and any material limitations or unverified claims. Do not claim interactivity, offline support, or successful checks that were not exercised. If the environment cannot render or export, explain that limitation instead of marking the artifact complete.

## Supporting resources

- [Resource library](references/RESOURCE_LIBRARY.md): choose local upstream guides by task; load only relevant files.
- [Sources and exclusions](references/SOURCES.md): upstream revisions, what was incorporated, and optional external integrations.
- [Third-party notices](THIRD_PARTY_NOTICES.md): licenses to preserve when reusing reference code or distributing the skill.
