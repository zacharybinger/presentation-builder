# Visual explanation, diagrams, motion, and 3D

## Diagram selection — semantics before aesthetics

From the diagram-design skill: choose a **semantic behavior** first, then a layout type; favor simple editable HTML/SVG. A few useful mappings:

| Meaning to express | Diagram | Meaningful reveal |
|---|---|---|
| Services, trust zones | architecture / deployment with containment | add nodes → connectors → trust boundary → exception |
| Request handling | data flow / swimlane | request → handoff → queue → response |
| Repeated iterations | feedback loop / flywheel | stage → feedback → changed next pass |
| Alternatives | decision matrix / quadrant | choices → criteria → tradeoff frontier |
| Changed topology | architecture delta | synchronized before/after + highlighted changed links |
| Data distribution | scatter / bar / waterfall | axis and context → observations → insight |
| Time-order | timeline / sequence | participants → events → latency/failure branch |

Show 4–9 active nodes for a typical projector scene; use additional steps or detail pane beyond that. A connector must have an interpretable direction, label, or semantic role. Avoid crossing edges by re-laying out nodes or routing with elbows. Use SVG `viewBox` to keep diagrams sharp. Give accessible `<title>` / `<desc>` and a visible textual summary.

## Motion contract

Borrowing from frontend-slides, taste-skill and HyperFrames:

- Establish a motion **grammar**: one standard easing, a short timing scale, a dominant movement direction, and a reserved signature gesture.
- Connect states causally. For example `input arrives → arrow lights → output grows`; do not animate everything independently.
- Preserve identity. Where one object persists, animate its transform/position/color rather than replacing with a visually unrelated block.
- Entering new material: controlled ease-out; on-screen travel: smooth ease-in-out; tiny press feedback: quick.
- Motion budget: 1 memorable signature motion per chapter, understated subordinate reveals elsewhere. Silence and stillness before an important change increases contrast.
- Avoid idle breathing/wobble, stagger every item indiscriminately, looping flashes, default rotating 3D object with no instructional goal.
- Exit/entry motion on adjacent cinematic scenes should continue along the same vector. Track transitions as a **vector ledger** when planning video exports.

```css
:root {
  --ease-out: cubic-bezier(.22, 1, .36, 1);
  --ease-travel: cubic-bezier(.76, 0, .24, 1);
  --t-press: 140ms;
  --t-reveal: 620ms;
  --t-travel: 800ms;
}
.reveal { transition: opacity var(--t-reveal) var(--ease-out), transform var(--t-reveal) var(--ease-out); }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; } }
```

Use real state variables for a deterministic reveal. Animation must have a meaningful visible end state. A screenshot taken at any deep link must show the correct state after render.

## Interactive technical scene design

Build an interaction specification per widget:

```text
Question: What should the participant discover?
Input: range slider 0–100 (with labeled units)
Feedback: one chart, one numerical output, one explanatory annotation update synchronously
Reset: restore 50 and update output
Navigation: Arrow keys work from the slide, but never steal keys from the slider
Accessibility: label + aria-valuetext + text-equivalent result
```

If the interaction merely changes hue or particle speed without affecting the explanation, remove it or label it decorative. Distinguish **simulation, sampled data, static illustration, and live measurement** clearly.

## 3D guardrail

Only introduce 3D when axial depth, orientation, shape, or rotation is essential. For standard diagrams, SVG is clearer. Set camera framing and focal depth, avoid postprocessing that destroys contrast, prefer controls with clear orbit limits and an explicit reset. Provide a poster/still fallback and a description of the 3D relationship. Dispose WebGL resources on unmount. Limit device pixel ratio and pause when hidden. Ensure a screenshot can still communicate the point.

## Narrated video export

For MP4 via HyperFrames: storyboard exact timestamped beats, convert imperative transitions to **seekable timeline functions** (same frame output regardless of seeking direction), preload fonts/media, maintain opaque composition ground to prevent seam flashes, render test frames at transitions, and inspect the completed output. Continuous vector direction at scene seams matters more than adding dozens of flashy effects. The MP4 companion is not an interactive deck.
