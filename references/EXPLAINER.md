# Extracted "Explainer" design pattern — from the attached prototype

The user supplied a working four-chapter educational HTML presentation: `index.html` (neural networks), `tokens.html`, `attention.html`, `training.html` and matching CSS/JS, plus `STYLE_GUIDE.md`. Exact originals are in `examples/explainer-original/`.

## Structural DNA

- Top persistent chapter navigation; active chapter is distinct.
- Single claim headline updated each reveal, one-sentence supporting copy, and a main content shell containing diagram and concept/equation annotation panel.
- Progressive idea development: networks (5 steps), tokens/embeddings (5 steps), attention (9 steps), training (8 steps); the interaction state is data-driven in `steps[]` objects with `title`, `copy`, `kicker`, `equation`, `detail`, with extra captions where needed.
- SVG is the primary instructional medium (network connectivity, token plots, attention lines and arrows). Some modules use HTML flow cards, probability bars and plots.
- Active concept colors are stable within a chapter, semantic labels accompany them; details introduced in earlier states persist when relevant.
- Back/Next buttons, progress indicator, Arrow keys/Space, browser history via `?step=`; specific controls change an explanatory diagram, not just decoration.
- Example `attention.js`: live next-token decoding parameters / comparison of multiple heads. Example `training.js`: probability states with cross-entropy loss and a loss curve. Example `tokens.js`: cosine similarity comparison. These are pedagogical *simplifications* and should be labeled as such when reused.

## What's worth retaining

The strongest aspect is **one visual thought unfolding**. The user does not have to re-parse a brand-new layout on each click; shapes persist and acquire semantic meaning. Keep the chapter/reveal model and the conceptual sidecar, with URLs that resume an exact point.

## What to generalize or improve

- The uploaded implementation has a separate HTML/CSS/JS per chapter; for a new deck use a **shared controller** and data-driven scene modules so navigation and state updates are not copied four times.
- The example is primarily low-key white/light with familiar system fonts. Treat it as an **Explainer direction**, not as the global look. For vibrant requests, add subject-specific imagery, typography, one accent field, and clear contrast without sacrificing readable teaching diagrams.
- Prioritize a fixed 16:9 stage; the uploaded CSS uses a width-constrained `min-height:100vh` document layout. For projection use a stage that scales uniformly, not a deck that unexpectedly reflows or scrolls.
- Animation should remain causally explanatory. Avoid automatic transitions that hide interactive content before a live operator can inspect it.
- Keep the exact scientific/source wording only for the provided sample, and review examples/assumptions before using in a new pedagogical context.

## Mapping a new subject to the pattern

1. List 3–6 concepts and assign durable names/colors.
2. Build a baseline SVG showing only the first component.
3. Create reveal states that add *relationships* (not more decorative text).
4. Add a sidecar that switches between intuition, formula/pseudocode, and concrete example.
5. Add a real experiment: select a node, adjust a threshold, play/pause a trace, inspect a probability distribution, toggle before/after.
6. Verify direct links to later steps, browser back/forward, keyboard focus, and that the densest reveal fits the stage.
