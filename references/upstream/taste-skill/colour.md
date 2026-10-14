> Curated from [taste-skill](https://github.com/Leonxlnx/taste-skill/blob/a60a36dc2bb3bb77ccf17f2f62041f5ca8a458b9/skills/taste-skill/references/colour.md), revision `a60a36dc2bb3`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Adapt website heuristics to slides. No mandatory photo counts, website score caps, or upstream inspection scripts apply.

## 2. The roles

```css
:root {
  --bg: …;          /* the ground: most of the surface */
  --surface: …;     /* one tone step from the ground: filled panels, form fields, tiles */
  --ink: …;         /* main text and the strongest marks */
  --muted: …;       /* secondary text; still passes contrast on --bg */
  --accent: …;      /* the one accent */
  --accent-ink: …;  /* text on the accent */
  /* --field-1 … --field-n and their inks, when the palette has section fields */
}
```

Use the tokens for every colour in the build. A raw hex in a component is a second palette starting.
Do not add greys between the roles: if you need a quieter text, it is `--muted`; if you need a quieter
surface, it is `--surface`.

## 3. Proportion

Decide the shares before colouring anything and check them in the screenshot:

- **Ground:** 70–90% of the page.
- **Ink:** text and perhaps one inverted section (ink as ground, ground as ink).
- **Accent:** under 5% of any screen. It marks the action and at most one other recurring thing. The
  moment it appears in five places it stops meaning "here".

Palettes with fields (flat-loud, pastel) work differently: each section is one field at full strength
and the proportion rule applies inside each section (field, its ink, nothing else).

The accent is not for headings, icons, bullets, borders or underlines unless the direction sheet says
so. A headline is ink.

## 6. Dark pages

- Put `color-scheme: dark` on the root so form controls and scrollbars follow.
- The ground is a deep tone with a slight tint from the palette, and the ink is a soft light, not
  `#fff` on `#000`, unless the palette deals exactly that for a stark two-tone direction.
- Secondary text is where dark pages fail: check `--muted` against the ground (4.5:1).
- Depth on dark comes from a lighter surface step, never from glows or coloured light.
- Use lighter font weights than you would on a light page.

## 8. Contrast

- Body text 4.5:1 or better; display type and large numerals 3:1 or better; the dealt palettes meet
  7:1 for ink on ground.
- `inspect.mjs` computes contrast for text on flat grounds and fails anything under 2.6:1. It cannot
  see text over photographs: check those in the screenshots yourself.
- Do not lower opacity on text to make it "soft" unless you have checked the resulting ratio.
- Focus states and hover states increase contrast, never reduce it.
