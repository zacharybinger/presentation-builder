> Curated from [design-dna](https://github.com/zanwei/design-dna/blob/593e39bc9e3652734653bd75544a333d7d43615e/references/generation-guide.md), revision `593e39bc9e36`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Map tokens to a fixed 1600×900 stage; dependencies must be bundled locally.

## Priority Order

When generating a design from DNA JSON + content:

1. **Color & Typography** — define 80% of visual identity
2. **Spacing & Layout** — structural rhythm
3. **Shape & Elevation** — surface treatment
4. **Design Style qualitative fields** — mood, personality, composition approach
5. **Visual Effects** — special rendering layer (Canvas, WebGL, shaders, etc.)
6. **Motion & Interaction** — enhance after static layout and effects are solid

## Dimension 1: design_system → Code

### Tailwind CSS / Utility-First
```
color.primary.hex        → --color-primary / bg-[hex]
typography.font_families → font-family config
spacing.scale            → spacing config values
shape.border_radius      → rounded-{sm|md|lg|full}
elevation.levels         → shadow-{sm|md|lg}
```

### Plain CSS / CSS Variables
Generate a `:root` block with all design tokens:
```css
:root {
  --color-primary: {color.primary.hex};
  --color-secondary: {color.secondary.hex};
  --color-accent: {color.accent.hex};
  --font-heading: {typography.font_families.heading};
  --font-body: {typography.font_families.body};
  --radius-sm: {shape.border_radius.small};
  --radius-md: {shape.border_radius.medium};
  --radius-lg: {shape.border_radius.large};
  --shadow-low: {elevation.levels.low};
  --shadow-med: {elevation.levels.medium};
  --shadow-high: {elevation.levels.high};
  --ease: {motion.easing};
  --duration-micro: {motion.duration_scale.micro};
  --duration-normal: {motion.duration_scale.normal};
  --duration-macro: {motion.duration_scale.macro};
  /* ... map all tokens */
}
```

### Component Decisions
- `components.button_style` → button classes and variants
- `components.card_style` → card container treatment
- `components.navigation_pattern` → nav component choice
- `interaction_feel.hover_behavior` → :hover / :focus states
- `motion.easing` + `motion.duration_scale` → transition properties

## Dimension 2: design_style → Subjective Decisions

| DNA Field | Guides |
|---|---|
| aesthetic.mood | Overall emotional feeling — warm tones, cool precision, etc. |
| visual_language.whitespace_usage | padding/margin generosity |
| visual_language.contrast_level | How much elements pop vs. blend |
| composition.hierarchy_method | What tool to use for emphasis |
| composition.balance_type | Symmetric layout vs. dynamic asymmetry |
| imagery.graphic_elements | Decorative SVGs, gradients, patterns |
| brand_voice_in_ui.tone | Microcopy phrasing |
| interaction_feel.microinteraction_density | How many hover/click effects |

## Quality Checks

Before delivering, verify:
- [ ] Every color in output traces back to DNA palette
- [ ] Font families match DNA specification
- [ ] Spacing rhythm matches DNA scale
- [ ] Border radius matches DNA shape tokens
- [ ] Overall mood matches `design_style.aesthetic.mood`
- [ ] Component patterns match DNA `components` descriptions
- [ ] Contrast ratios meet WCAG AA minimum (4.5:1 body text, 3:1 large text)
- [ ] Visual effects match `visual_effects` specification (type, technology, params)
- [ ] Fallback strategy is implemented for effects
- [ ] `prefers-reduced-motion` is respected
- [ ] No effects render when their `enabled` flag is `false`
- [ ] Canvas/WebGL contexts are properly sized and handle resize
- [ ] Animation loops use `requestAnimationFrame` (no `setInterval`)
