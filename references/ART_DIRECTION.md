# Art direction for presentation decks

## Design from an idea, not a default UI

Build an inventory of 8–12 native nouns, shapes, numbers, metaphors, and materials in the subject. The style should belong to *this talk*. E.g. distributed queues → lanes, currents, pulsing edges; agent memory → palimpsest, time strata, indexed cards; genomics → paired strands and annotation grids. Do not turn every tech talk into a generic violet gradient.

## Four reusable directions, NOT locked presets

| Direction | Ground / ink | Accent logic | Composition | Motion |
|---|---|---|---|---|
| **Explainer** | porcelain / charcoal | stable semantic colors by concept | large thesis + constrained interactive diagram + evidence rail | cumulative SVG/path reveals, restrained 400–700ms |
| **Signal** | warm ivory / midnight | high-saturation cobalt + tangerine / citrine | giant editorial headline, dense asymmetric color blocks | one crisp mask reveal, directional flow |
| **Nocturne** | dark ink / bone | lime or electric cyan used sparingly | spotlight stage, emissive diagram, atmospheric field | depth changes / connected-object motion, no idle glow |
| **Atlas** | off-white / ink | data-dependent accent + cartographic red | column grid, annotation margins, charts, infographics | measured data and small multiples progressively drawn |

Choose ONE dominant direction; variant scene compositions create rhythm. Avoid generic three cards, tiny centered labels, fake glass blur, permanent blobs, and every-entry-identical slide-ups.

## Token contract

```css
:root {
  --ground: #f7f5ef;
  --ink: #17253a;
  --muted: #617087;
  --primary: #3656eb;
  --secondary: #ff763a;
  --highlight: #f3d448;
  --surface: #fffdf7;
  --hairline: rgba(23,37,58,.15);
  --ease-reveal: cubic-bezier(.22,1,.36,1);
  --ease-travel: cubic-bezier(.76,0,.24,1);
}
```

Define semantic roles, not literal blue-500 dependencies. Add concept roles (`--concept-input`, `--concept-transform`, `--concept-output`) consistently across slides. Before using 21st.dev/shadcn assets, remap their tokens to the deck. Never import a component's entire visual aesthetic if it fights the surrounding art direction.

## Typography

Three coherent roles: 1 intentional display face (can be local/fallback), 1 highly legible body face, 1 monospace for code/telemetry. Use distinctive display typography if assets are available and properly licensed; make a good local fallback for offline projection. Build a typographic scale (not arbitrary `clamp` within a fixed canvas): cover 110–165px, scene headings 62–84px, body 28–36px, diagram labels 18–26px. Check at 1280×720 scaled and projector distance.

## Visual discovery

When a design choice is genuinely open, draw **three contrasting one-slide previews** in a browser (one safe, one expressive, one unexpected) and compare screenshots. If the user already asks for direct delivery, choose a plausible direction and implement without requiring a style-selection conversation.

## Style critiques

Ask: Does the layout encode the story? Is the dominant shape specific to the subject? Does a single color convey a clear concept? Are there at least two complementary visual rhythms? Would this deck still be recognizable if its text were removed? If no, revise composition and art direction rather than adding gratuitous animation.
