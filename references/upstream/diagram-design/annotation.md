> Curated from [diagram-design](https://github.com/cathrynlavery/diagram-design/blob/11b08eade8049c441ed3df1895e3b527c26c0fbe/skills/diagram-design/references/primitive-annotation.md), revision `11b08eade804`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Serif marginalia is one optional voice. Keep annotation leaders visually distinct from data-flow arrows.

# Annotation Callout (italic-serif aside)

Use for editorial asides — the "italic pointer" that marks a detail without competing with the primary diagram grammar. Think marginalia: *"structure IS the index"*, *"no imports, no configuration"*.

## Grammar

```svg
<!-- 1. Italic serif text: the `callout` role from style-guide.md -->
<text x="904" y="36" fill="{ink}" font-size="14" font-style="italic"
      font-family="{callout}" text-anchor="end">no imports, no configuration</text>
<!-- 2. Dashed Bézier leader -->
<path d="M 820 44 Q 700 84 520 216" fill="none"
      stroke="{ink @ 0.40}" stroke-width="1" stroke-dasharray="4,3"/>
<!-- 3. Landing dot -->
<circle cx="520" cy="216" r="2" fill="{ink}"/>
```

## Rules
- Italic + serif together signal "editorial voice" against the diagram's sans/mono body. Don't substitute italic sans or italic mono — the combination is load-bearing.
- Dashed path (`stroke-dasharray="4,3"`) distinguishes the callout leader from primary arrows (which are solid).
- Place callouts in margins (top-right, bottom-left). Never inside the active diagram area.
- Max 2 callouts per diagram. More becomes commentary, not signal.

## Colors

| Intent | Text | Leader |
|---|---|---|
| Neutral aside | `ink` | `ink @ 0.40` |
| Focal / accent | `accent` | `accent @ 0.50` |
| Tertiary (muted) | `muted` | `ink @ 0.30` |

## Anti-patterns
- Solid arrow leader (reads as a flow arrow).
- Italic sans or italic mono — the serif is load-bearing.
- Callouts crossing primary arrows / lifelines — offset to a clear margin.
- Using a callout to label something the diagram should label directly — put the label on the element.
