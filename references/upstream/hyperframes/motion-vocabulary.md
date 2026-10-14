> Curated from [hyperframes](https://github.com/heygen-com/hyperframes/blob/74e17fa9cf81f8ef632eb49c3741c9ce420c2f3f/skills/motion-graphics/references/motion-vocabulary.md), revision `74e17fa9cf81`. Apache-2.0; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: For an explicitly requested video companion. These primitives are not a dependency on the HyperFrames CLI or registry.

## Entry

| primitive                     | GSAP recipe (into CSS end-state)                               | suits                     |
| ----------------------------- | -------------------------------------------------------------- | ------------------------- |
| `slide_bottom/top/left/right` | `from({ y:±150 / x:±200, opacity:0, ease:"power4.out" })`      | calm, build, professional |
| `scale_grow`                  | `from({ scale:0, opacity:0, duration:.6, ease:"power2.out" })` | calm, gentle              |
| `scale_punch`                 | `from({ scale:.6, opacity:0, ease:"back.out(2.2)" })`          | impact, energetic         |
| `fade_in`                     | `from({ opacity:0, duration:.4 })`                             | subtle                    |
| `fade_blur`                   | `from({ opacity:0, filter:"blur(14px)" })`                     | cinematic, dreamy         |
| `typewriter`                  | reveal via clip/`SplitText` width step                         | technical, narrative      |
| `word_reveal`                 | per-word `from({opacity:0,y:..}, stagger:.1)`                  | storytelling              |
| `wave`                        | per-letter `from({y:..}, stagger:{each:.04})`                  | flowing, musical          |
| `bounce_in`                   | `from({y:-120}, ease:"bounce.out")`                            | playful                   |
| `slam`                        | `from({ y:-300, ease:"power4.out" })` + shake on land          | impact, heavy             |

## Emphasis (in place, often on a beat)

| primitive     | GSAP recipe                                                          | suits              |
| ------------- | -------------------------------------------------------------------- | ------------------ |
| `scale_pulse` | `to({ scale:1.12, yoyo:true, repeat:1, ease:"sine.inOut" })` at beat | rhythmic, peak     |
| `shake`       | `to({ keyframes:[{x:-9},{x:9},{x:0}], ease:"none" })`                | urgent, intense    |
| `glow`        | `to({ textShadow:"0 0 46px <ink/accent>", yoyo:true, repeat:1 })`    | important, magical |
| `color_shift` | `to({ color:"<accent>" })` (or accent on the word in CSS)            | dynamic            |

## Exit

| primitive   | GSAP recipe                                        | suits      |
| ----------- | -------------------------------------------------- | ---------- |
| `fade_out`  | `to({ opacity:0, duration:.4, ease:"power2.in" })` | ending     |
| `slide_out` | `to({ y/x: off, opacity:0, ease:"power2.in" })`    | transition |
| `scale_out` | `to({ scale:1.06, opacity:0, ease:"power2.in" })`  | transition |

## Accent graphics (not text)

`underline_sweep` `fromTo({scaleX:0},{scaleX:1}, transformOrigin:"left center")` · `bar_wipe` · `hold_breath` `to({scale:1.015, ease:"sine.inOut"})`.
