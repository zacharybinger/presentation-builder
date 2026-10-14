> Curated from [taste-skill](https://github.com/Leonxlnx/taste-skill/blob/a60a36dc2bb3bb77ccf17f2f62041f5ca8a458b9/skills/taste-skill/references/type.md), revision `a60a36dc2bb3`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Adapt website heuristics to slides. No mandatory photo counts, website score caps, or upstream inspection scripts apply.

## 3. Setting display type

Large type exposes spacing that is invisible at text size. Apply all of these to anything over 40px:

```css
.display {
  font-size: var(--step-display);
  line-height: 0.95;              /* 0.85–1.05; tighter for capitals and condensed faces */
  letter-spacing: -0.035em;       /* -0.02 to -0.05em; use the value on the direction sheet */
  font-kerning: normal;
  text-wrap: balance;
  max-width: 14ch;                /* choose the measure so lines break where you want */
  margin: 0;
}
```

- **Tracking scales with size.** The larger the type, the tighter it needs to be; a value right for
  120px will choke 32px. Set tracking per step, not once for all headings.
- **Leading below 1.0 needs checking.** Look for collisions between descenders and the ascenders or
  accents of the next line. Two-line headlines make this easy to verify by eye.
- **All capitals** want slightly open tracking (0 to +0.03em) even at display size, and leading around
  0.9.
- **Optical alignment.** Big letters with round or diagonal left edges (O, C, A, T, W) look indented.
  Pull the headline left by about 0.04–0.06em (`margin-left: -0.05em`) so it aligns optically with the
  text beneath it.
- **Viewport-wide type.** For a line that must span the screen, size it in `vw` and verify at 390 and
  1440; set `white-space: nowrap` and let the container clip rather than wrap. Calculate the size from
  the character count: `font-size ≈ container width ÷ (characters × k)` with k from `copy.md` §2.
- Never add a text shadow, an outline stroke, or a gradient fill to display type.

## 6. One family or two

A third of the studied sites use a single family for everything, and it is the safest way to look
coherent. When the dealt system has two faces:

- Give each a job and never swap them: one sets headlines, the other sets everything else.
- Do not introduce a third face for labels, numbers or quotes.
- Do not mix two faces inside one headline.
- Italic is for titles of works and real emphasis inside paragraphs, never as decoration.

## 7. Details that separate set type from typed text

- Curly quotes and apostrophes, real dashes, a real ellipsis (see `copy.md` §7).
- `font-variant-numeric: tabular-nums` for prices, tables, dates in columns; `oldstyle-nums` suits
  serif body text.
- `text-underline-offset: 0.18em; text-decoration-thickness: 0.07em` on links, so underlines clear the
  descenders.
- `hyphens: none` on headings. `overflow-wrap: anywhere` only on long URLs or emails.
- A heading belongs to the text after it: space above a heading is at least twice the space below.
- `::selection { background: var(--accent); color: var(--accent-ink); }` and a visible
  `:focus-visible` outline in the accent, so even the browser's own states belong to the design.
- Do not change weight on hover; the line reflows.

## 8. Mistakes the inspector cannot see

- A headline that passes the two-line rule but breaks badly: one orphan word on line two, or a break
  that splits a phrase ("Stools for small / kitchens"). Author the break.
- Display type so tight that letters touch, or so loose it falls apart.
- A confident hero followed by section headings almost as large. Keep one size dominant per screen.
- Body text set in the display face when that face was drawn for large sizes only.
- Everything bold. If every line is emphasised, none is.
