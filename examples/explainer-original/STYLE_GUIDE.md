# LLM Presentation Style Guide

Reference inspiration: [The Highest Loop](https://loopcraft.swyxio.workers.dev/)

## Design principle

Treat the presentation as an interactive technical essay, not a sequence of disconnected slides.

Each advance should transform or extend the audience's current mental model. Preserve previously introduced information whenever the relationship between old and new material matters.

## Visual direction

- Use a white background and dark charcoal text.
- Prefer generous whitespace over decorative elements.
- Establish hierarchy through scale, spacing, borders, nesting, and color.
- Use large, heavy headings with tight letter spacing.
- Use a system sans-serif for prose and a monospace font for tokens, code, and model internals.
- Keep shadows subtle. Favor thin borders and pale tinted backgrounds.
- Use rounded cards and pill labels consistently.
- Give every recurring concept a stable accent color across the entire presentation.
- Design primarily for a 16:9 projector viewport.

### Starting design tokens

```css
:root {
  --ink: #1f2430;
  --muted: #6b7280;
  --border: #d8dde6;
  --surface-subtle: #f5f6f8;
  --background: #ffffff;

  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, Helvetica, Arial, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, Consolas, monospace;

  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-fast: 300ms;
  --duration-standard: 600ms;
}
```

These are starting values, not a requirement to reproduce the reference exactly.

## Typography

- Title: `clamp(44px, 9vw, 92px)`, weight 800, line-height near 1.
- Chapter heading: approximately 28–36px, weight 700–800.
- Diagram labels: approximately 14–16px.
- Navigation and supporting annotations: approximately 12–14px.
- Code: approximately 14–16px with a comfortable line height.
- Avoid long paragraphs on the presentation stage.

## Layout

- Keep a persistent chapter navigation bar near the top.
- Center title and single-concept scenes.
- Use a constrained content width, generally 760–1040px.
- Keep controls in a stable location between the heading and visualization.
- Avoid moving permanent interface elements between reveal steps.
- Ensure the densest state fits within the intended projector viewport, or deliberately provide controlled scrolling.
- Allow navigation to wrap or collapse cleanly at narrower widths.

## Color system

Assign colors by concept, not by slide.

For an LLM presentation, possible mappings include:

- Tokens: warm orange
- Embeddings: blue
- Attention: green
- Transformer layers: violet
- Logits and probabilities: pink or red
- Generated output: gold
- Training-only concepts: a distinct neutral or secondary palette

Use a pale tint of each concept color for its card background. Preserve the same mapping in diagrams, code, labels, and later callbacks.

Do not rely on color alone. Repeat the concept name, icon, border style, or position.

## Narrative and information design

### Progressive accumulation

Begin with the smallest useful unit and add one conceptual layer at a time:

1. Text
2. Tokens
3. Embeddings
4. Attention
5. Transformer layer
6. Layer stack
7. Logits and next-token probabilities
8. Autoregressive generation

Whenever possible, keep the existing visualization on screen and animate it into its new role.

### Multiple representations

Render the same underlying concept in several forms:

- Intuitive visual model
- Technical diagram
- Minimal pseudocode
- Concrete example
- Human analogy
- Summary or application

These representations should share terminology, ordering, and colors.

### One reveal, one idea

Each advance should introduce one meaningful change:

- Add a component
- Connect two components
- Change a state
- Reveal a result
- Reframe the current model

Avoid advancing merely to animate decoration.

## Motion

Animation should explain structure, causality, flow, or state change.

### Standard entrance

Use a short fade-and-rise for genuinely new material:

```css
@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

.enter {
  animation: rise var(--duration-standard) var(--ease-out) both;
}
```

### Motion rules

- Keep most transitions between 400 and 700ms.
- Use one shared easing curve throughout the deck.
- Animate existing objects between states instead of removing and recreating them visually.
- Use FLIP-style transforms when an existing diagram changes position or scale.
- Crossfade preloaded images rather than loading them during a reveal.
- Avoid animating every element simultaneously.
- Prefer `transform` and `opacity` for performance.
- Support reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Interaction model

Support:

- Right Arrow or Space to advance
- Left Arrow to go back
- Visible Back and Next buttons
- Click on the presentation stage to advance
- Direct chapter navigation
- A local progress indicator

Click-to-advance must exclude links, buttons, selectable code, and other interactive elements.

Represent the current chapter and reveal step in the URL so that refresh, browser history, and shared links preserve the exact presentation state.

## Technical architecture

Use a small data-driven presentation system rather than hard-coding every state independently.

Recommended structure:

```text
index.html
src/
  app.js
  content.js
  stepper.js
  renderers/
    tokens.js
    embeddings.js
    attention.js
    transformer.js
  styles/
    tokens.css
    presentation.css
assets/
```

### Single source of truth

Store recurring concepts in shared data:

```js
export const concepts = [
  {
    key: "tokens",
    label: "Tokens",
    color: "#d2691e",
    background: "#fdeee2",
    description: "Text fragments processed by the model"
  }
];
```

Render diagrams, code, labels, and summaries from this data to prevent inconsistencies.

### Rendering contract

Each chapter should expose a renderer based on presentation state:

```js
function render(step, previousStep) {
  // Update the current visualization.
}
```

A shared controller should own keyboard input, buttons, progress, URL state, and bounds checking.

## Accessibility

- Use semantic headings, navigation, buttons, lists, and figures.
- Provide text alternatives for every diagram.
- Announce important dynamic changes through an appropriate live region.
- Maintain visible keyboard focus.
- Ensure controls have sufficiently large targets.
- Meet WCAG contrast requirements.
- Never encode meaning through color alone.
- Avoid unexpected advancement while the audience is interacting with content.
- Test the full deck using keyboard-only navigation.

## Presentation-specific features

Consider adding:

- Presenter notes
- Overview or chapter grid
- Fullscreen mode
- Elapsed-time display
- Speaker-only controls
- A reset-to-start shortcut
- Deep links to every reveal
- Print or PDF fallback

## Avoid

- Independent slides that repeat an almost identical diagram.
- Animation used only for visual novelty.
- Dense final states that overflow accidentally.
- Small navigation designed for laptop viewing rather than projection.
- Duplicated navigation or styling in every chapter file.
- Reveal state that disappears after refresh.
- Loading images or fonts during a live transition.
- Long prose blocks competing with the speaker.

## Pre-build checklist

- [ ] Define the chapter-level narrative.
- [ ] Identify the core mental model that will accumulate.
- [ ] Define stable concept names and colors.
- [ ] Create the shared presentation data.
- [ ] Design the densest final state first.
- [ ] Confirm it fits a 16:9 viewport.
- [ ] Decide what changes on every reveal.
- [ ] Implement keyboard, button, and stage controls.
- [ ] Add URL-addressable state.
- [ ] Add reduced-motion behavior.
- [ ] Add diagram descriptions and keyboard accessibility.
- [ ] Preload required media.
- [ ] Test at projector resolution.
- [ ] Test refresh, back, forward, and direct links.
- [ ] Test the entire talk without a mouse.

## Guiding question

For every reveal, ask:

> Does this change help the audience understand how the system works, or does it merely make the screen move?

If it only makes the screen move, remove it.
