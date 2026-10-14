# Design DNA: a repeatable design identity, not a borrowed theme

**Origin:** [zanwei/design-dna](https://github.com/zanwei/design-dna), especially its `SKILL.md` and `references/schema.md`, plus [AThevon/genjutsu](https://github.com/AThevon/genjutsu) `paint` / `cast`. Concepts adapted here; selected reference excerpts are bundled in [the local library](RESOURCE_LIBRARY.md), without requiring those skills.

## Three separate dimensions

Create a small `DESIGN_DNA.json` in **authoring workspace** before building a large deck. This is NOT delivered as a third file; its values and intent are encoded into the final presentation's embedded styles/behavior.

1. **`design_system` — measurable:** background and text colors; semantic palette; actual font families and offline font assets; 16:9 content grid; type scale; safe margins; cards and borders; easing and duration tokens; visual hierarchy.
2. **`design_style` — perceptual:** audience, mood, intentional metaphor, material, era, visual grammar, texture, positive/negative space, imagery and data style, compositional rhythm; what the presentation deliberately **does not** look like.
3. **`visual_effects` — technical:** SVG morphs, GSAP timelines, CSS transitions, Lottie, Canvas, WebGL/Three.js, cursor treatment, interaction density and fallbacks. Explicitly enumerate what renders as a frozen PDF frame.

For a visual reference image, **measure** dominant colors (pixel sampling/clustered palette or direct CSS tokens) rather than guessing hex codes from appearance. For a website reference, inspect screenshots, assets, and styles as evidence; separate measured facts from judgment. When several references disagree, record a priority order and reject attempts to blend every style.

## Thesis before implementation (from Genjutsu)

For a *new style*: write a **visual thesis**: `This talk makes [subject] tangible via [specific metaphor] using [type, composition, material], so [audience] understands [goal].`

For each complex widget/reveal: write an **interaction thesis**: `When the presenter/audience [action], [named object] [state change], revealing [specific relationship].` Art direct behavior before writing animation code. A button without a relationship to learn fails this thesis.

- `paint` contributes identity discipline for the whole deck (a unified design system, staged critique).
- `cast` contributes one specific, tested, responsive micro-interaction or spatial moment.
- `bunshin` is a multi-agent website workflow; it is **not** a required deck dependency or default process.
- Existing slides must preserve brand unless explicitly approved to change it. Avoid unnecessary library installation, especially for one-off motion.

## Minimal design profile

```json
{
  "design_system": {
    "canvas": { "width": 1600, "height": 900, "ratio": "16:9" },
    "palette": { "ground": "#F6F2E9", "ink": "#17253A", "accent": "#3F56ED", "highlight": "#F56D3A" },
    "typography": { "display": "available display family", "body": "available text family", "code": "available monospace" },
    "motion": { "short_ms": 180, "normal_ms": 450, "hero_ms": 750, "ease": "cubic-bezier(0.22, 1, 0.36, 1)" }
  },
  "design_style": {
    "concept": "an idea clarifying as it travels through a system",
    "personality": ["editorial", "technical", "optimistic"],
    "layout": "split-stage, typographic hero, persistent system diagram",
    "avoid": ["same three-card grid everywhere", "gratuitous glow", "decoration without explanation"]
  },
  "visual_effects": {
    "primary": ["SVG progressive reveal", "CSS transitions"],
    "optional": ["GSAP seekable timeline"],
    "interactive_inputs": ["keyboard", "slider", "node inspection"],
    "pdf_fallback": "fully rendered final reveal of each slide",
    "reduced_motion": "show semantic end-state immediately"
  }
}
```

Profile is an original *small subset*, not the full upstream Design DNA schema. If the user's task requires round-tripping a full upstream profile, read the [bundled full schema](upstream/design-dna/schema.md) and use the complete specification.

## Art-direction quality gate

1. Can the style be explained by subject-specific material, not by 'modern tech' adjectives?
2. Could a critic distinguish this deck from a template if the title were removed?
3. Are the color measurements/semantic assignments consistent across scenes?
4. Is the most interesting scene actually the clearest scene?
5. Have you reviewed screenshots and corrected problems rather than trusting code?
6. Does the PDF show the same finished visual claims, not an empty animated start state?
