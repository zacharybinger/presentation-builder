---
name: presentation-builder
metadata:
  version: "2.0.0"
description: Create, redesign, and validate distinctive interactive HTML presentations from a topic, notes, documents, technical architecture, or existing deck. Use for vibrant browser-native talks, conference decks, pitch decks, technical explainers, interactive diagrams, scrollytelling, and animated visual presentations. Produces exactly one self-contained offline HTML presentation and one static 16:9 PDF, with keyboard/reveal navigation, deep links, browser screenshots, and quality assurance. Includes an explainer style derived from the user's interactive neural network teaching prototype.
---

# Presentation Builder — narrative-first interactive decks

**Deliver the finished presentation, not just a storyboard.** Use the user's content as factual ground truth; research externally only when accuracy requires it, and identify assumptions. Read this router, then open only the applicable files under `references/`. Work self-sufficiently even if other third-party skills are unavailable.

## 0. Choose the route

- **New deck from notes/topic:** analyze facts and objective → story → art direction → visuals → interactive build → QA.
- **Enhance an existing deck:** inspect before editing; preserve working controls and factual text; change the smallest necessary surface; regression-test all transitions and links.
- **Explainer/teaching deck:** adopt the progressive *persistent mental model* described in `references/EXPLAINER.md`; use `examples/explainer-original/` as a complete working reference, not as mandatory styling.
- **Static speaking or pitch deck:** create the lightest solution that looks outstanding; do not add controls, libraries, or 3D just to increase complexity.
- **PDF:** mandatory static companion exported from the same HTML, not a screenshot collage; defaults to final-reveal snapshots. See `references/EXPORT.md`. If PPTX/video is separately requested, negotiate this as an additional artifact instead of violating the requested two-file default.

**Required delivery:** exactly `presentation.html` (single offline interactive file) and `presentation.pdf` (one print page per completed scene by default); no external runtime dependencies or separate asset files. Authoring source can remain modular. Read `references/EXPORT.md` and run `scripts/export_deck.py` before final handoff. **Default authoring stack:** 16:9 browser-native HTML, keyboard-accessible, with the `templates/interactive-deck/` starter. For advanced React/shadcn/21st.dev components, switch to React + Vite only if it materially improves the deck. A user asking for a “presentation” does not automatically require React or 3D.

## 1. Understand and structure the content

Extract audience, goal, single desired takeaway, narrative stakes, evidence, source links, time/length/density if supplied, accessibility, brand constraints, and live-demo needs. Make sensible explicit assumptions for missing secondary details; do **not** force a questionnaire. Use `references/STORY.md`.

Write a **slide/reveal matrix** before implementation:

| Slide | One-sentence claim | Evidence/example | Visual metaphor | Audience action | Reveal states |
|---|---|---|---|---|---|

Each slide has a meaningful claim; each reveal must change understanding (introduce a relationship, causality, comparison, or result). Eliminate filler slides. Density choice: speaker-led/low by default; reading-first only if user asks for a self-contained document. Use one persistent visual model where useful.

## 2. Select art direction, not a generic template

Read `references/ART_DIRECTION.md` and `references/DESIGN_DNA.md`. Derive a distinctive design *concept from the subject*: materials, vocabulary, data, shape, texture, existing product or technical system. Write a minimal **Design DNA** in the authoring workspace: measurable design_system, subjective design_style, and feasible visual_effects; state visual and interaction theses before implementation. Specify ground, ink, 1 primary accent, 1 supporting accent, visual language, type hierarchy, grid, and one signature transition. Encode the chosen DNA into the shipped HTML; do not deliver the JSON as a third file. Offer 2–3 actual visual previews when user is exploring a look; when asked to produce immediately, choose confidently and continue. Avoid stock gradient + three identical cards + random glassmorphism.

Style starting points (modify to suit context):
- `explainer`: source prototype's clean technical essay, light ground, semantic colors and progressive SVG.
- `signal`: bold high-contrast editorial / electric color fields, typographic scale and strong diagonal forms.
- `nocturne`: dark cinematic / subdued chroma, spotlighted diagrams and subtle depth.
- `atlas`: information-rich editorial maps, print-grid typography, annotated chart work.

Preserve consistent semantic concept colors throughout the *whole deck*. Run `scripts/create_deck.py` to scaffold a runnable starter with three switchable themes.

## 3. Choose the right rendering technology

Read `references/STACK_AND_COMPONENTS.md`, `references/VISUALS_AND_MOTION.md`, and `references/MOTION_ENGINE.md`. Use LottieFiles motion direction to establish intent/personality, Genjutsu-style interaction theses, and official GSAP timeline patterns only when they improve progressive explanation. Respect pre-existing runtime frameworks.

- **HTML/CSS/SVG** first for accessible, sharply rendered diagrams, text, charts and reveal sequences. SVG lines must encode data/relationships, not decoration alone.
- **React/Vite** when scene state is complex, or when integrating `shadcn/ui`, `21st.dev`, canvas component libraries, Motion, or R3F. Select components by need, audit third-party licenses/dependencies, and adapt them to the chosen design system.
- **thinking-orbs** only when demonstrating a real AI/agent activity state or concept. It is an animated state indicator, not a generic background or a substitute for explanatory motion.
- **GSAP** when multi-element SVG/DOM animation needs coordination, reverse/seek, or timeline labels; compile it into the local JS bundle. Use CSS for simpler effects. **Lottie** when a prepared vector animation is warranted; vendor player/assets, and freeze a meaningful still in PDF.
- **Three.js** only for spatial concepts where rotating, zooming, or exploring a three-dimensional relationship teaches something. Provide a textual/SVG fallback, dispose geometry/materials, and pause offscreen or for reduced-motion mode.
- **HyperFrames** is an optional *deterministic HTML-to-video rendering workflow*, not the runtime for clickable presentation widgets. For a prerecorded narration or MP4, produce a separate video version with seekable motion; validate seam direction and frame stability.

Model interactions as visible state transitions with explicit behavior; never fake a slider or button that has no effect. A live demonstration needs reset and clear state labels.

## 4. Scaffold and implement

From the skill directory:

```bash
python scripts/create_deck.py --title "My Interactive Talk" --style signal --output ./my-deck
# Edit modular sources in ./my-deck and QA.
python scripts/check_deck.py ./my-deck --out ./internal-qa
python scripts/export_deck.py ./my-deck --out ./deliverable
python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf
# Ship exactly ./deliverable/presentation.html and presentation.pdf
```

Starter files use **no external runtime dependencies**. Replace example narrative and SVG in `deck.js`, not the controller plumbing unless necessary. Edit `styles.css` design tokens, adding scene-specific layout as needed. State model: chapter/slide + local reveal + widget state; shareable `?slide=N&step=M&theme=...` deep links; `ArrowRight`/Space next, `ArrowLeft` previous; navigate with buttons and slide menu; `F` fullscreen, `Home`/`End` jump. Never intercept keypresses inside interactive controls. Changes should preserve history, focus and reduced motion.

**Interactive technical explainer:** `examples/explainer-original/` contains the user's four-chapter neural-net/tokens/attention/training prototype and style guide. Read its `STYLE_GUIDE.md` and inspect original JS state machines when extending that style; do not reproduce its scientific examples as universally accurate. See `references/EXPLAINER.md` for the extracted pattern.

## 5. Test in a real browser before delivering

Read `references/QA.md`. For any new deck or meaningful layout/interaction change:

```bash
python path/to/presentation-builder/scripts/check_deck.py ./my-deck --out ./deck-qa
```

The checker serves the deck, uses Playwright/Chromium, exercises forward/back navigation, deep linking and widget controls, checks browser errors, captures a screenshot of each slide and a mobile view, and checks stage bounds. If browser URL navigation is blocked by the environment, run `scripts/preview_deck.py` for in-memory screenshots/interaction checks, then clearly disclose that URL/history still need full testing. Install Playwright and browser if needed; see `references/QA.md`. Also **visually review** every captured image at 16:9 and at least one small/large viewport; automated checks cannot judge art direction, typography, crowded final states, or diagram meaning. Iterate until legible, coherent, and free of overflow. Confirm all facts against the supplied context, and cite external research in the speaker notes or sources when used.

## 6. Mandatory HTML + PDF publishing

Read `references/EXPORT.md` and run `python scripts/export_deck.py ./my-deck --out ./deliverable`. This bundles runtime CSS/JS/local media into ONE HTML and prints ONE 16:9 PDF covering completed reveal states. The HTML must run without network access, CDN imports, separate JS or CSS files, or a local server. For React/GSAP/Three.js/shadcn work, compile first and reject unresolved dynamic imports or external network assets. PDF is static; do not claim it preserves sliders, video, live animation, or 3D interaction. Browser review and print/PDF checks are mandatory.

## 7. Delivery contract

Return **two directly downloadable files** — `presentation.html` and `presentation.pdf` — plus a brief deck map and creative direction, what was actually tested, how to open/navigate, and any missing/unverified content. Skill installers may receive the entire skill folder/ZIP; individual *presentations* must never require a folder or ZIP at runtime. Do not call a deck interactive unless its controls are implemented and checked. Favor a complete good deck over an over-engineered unfinished one. For reuse as a skill, install this entire `presentation-builder/` folder under your agent's skills directory so its `SKILL.md`, `references/`, `scripts/`, and `templates/` remain together.

**Do not:** import entire upstream skills automatically, depend on online CDNs during a live presentation, ship slide clipping/scrollbars, assert unverified claims, treat a video as interactive, invent test results, or use motion without semantic purpose.

## Reference routing

- Narrative design: `references/STORY.md`
- Style discovery & templates: `references/ART_DIRECTION.md`
- UI/component choices: `references/STACK_AND_COMPONENTS.md`
- Integration code recipes: `references/RECIPES.md`
- Technical diagram, animation & 3D rules: `references/VISUALS_AND_MOTION.md`
- Uploaded user example adaptation: `references/EXPLAINER.md`
- Choreography/GSAP/Lottie motion engine: `references/MOTION_ENGINE.md`
- Design DNA / Genjutsu art direction: `references/DESIGN_DNA.md`
- Single HTML/PDF export and freeze contract: `references/EXPORT.md`
- Browser QA, exports, accessibility: `references/QA.md`
- Resource survey, upstream attribution: `references/SOURCES.md`
