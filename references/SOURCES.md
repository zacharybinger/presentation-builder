# Upstream research and provenance (reviewed 2026-10-13)

This skill synthesizes **design ideas and workflow guidance**, with links to upstream projects; third-party skills and component code are not copied into this package. If you choose to incorporate external implementation code later, inspect the current upstream license, attribution, dependencies and security.

| Resource | Contribution to this skill | Important distinction |
|---|---|---|
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | fixed 16:9 viewport, bold art direction, visual previews, slide navigation, review after changes | upstream favors standalone zero-dependency HTML; our skill adds an optional React route |
| [taste-skill](https://github.com/leonxlnx/taste-skill) | anti-generic subject-specific art direction, type/color decisions, browser screenshot critique, intentional motion budgets | upstream targets website design; adapted for stage-based presentations |
| [diagram-design](https://github.com/cathrynlavery/diagram-design) | semantic pattern → visual grammar, editability, SVG architecture/flow/chart guidance and density rules | draw diagrams only when they communicate more than prose |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | deterministic HTML-to-video export, continuous motion and seam craft for MP4 companions | video rendering **is not live deck interactivity** |
| [threejs-skills](https://github.com/cloudai-x/threejs-skills) | geometry, animation, raycasting, camera interaction, shaders and performance disciplines for spatial explanations | optional; don't use 3D for ordinary flowcharts |
| [playwright-skill](https://github.com/lackeyjb/playwright-skill) | real browser inspection, accessible-role interaction tests, screenshots, runtime error tracking | the bundled checker is independent, built on Python Playwright |
| [21st.dev](https://21st.dev/) | curated expressive React UI, shaders, motion/hero compositions, copyable source | a registry/catalog, not one universal npm package |
| [shadcn/ui](https://ui.shadcn.com/) | accessible, customizable component source for controls and panels | use Vite setup/registry install only when needed |
| [thinking-orbs](https://github.com/Jakubantalik/thinking-orbs) | 2D canvas React activity orb for actual agent processing states | not a WebGL globe and not a default background |
| **User-provided LLM Presentation Style Guide** | persistent visual mental model, per-concept stable colors, clickable reveals, step URL, interactive attention/token/training diagrams | exact user materials copied unchanged under `examples/explainer-original/` |

Further documentation: [shadcn Vite](https://ui.shadcn.com/docs/installation/vite), [shadcn registries](https://ui.shadcn.com/docs/registry/getting-started), [HyperFrames slides](https://hyperframes.heygen.com/guides/slideshow), [thinking-orbs demo](https://orbs.jakubantalik.com).

## Integration policy

No implied endorsement or license transfer. The package is an original synthesis and contains a user-provided example. When using borrowed source code, honor original licenses, note file-level provenance and avoid copying large upstream examples wholesale without checking rights.

## New resources incorporated (2026-10-13/14)

| Resource | Reviewed portions | Applied here |
|---|---|---|
| [Official GSAP Skills](https://github.com/greensock/gsap-skills) | `gsap-core`, `gsap-timeline`, `gsap-performance`, `gsap-plugins` | labeled, seekable SVG/DOM timelines, compositor-friendly properties, cleanup, offline bundling rules |
| [Design DNA](https://github.com/zanwei/design-dna) | `SKILL.md`, `references/schema.md` | three-part authoring profile: measurable system, perceptual style, advanced effects; distinguishes reference measurements from aesthetic inference |
| [LottieFiles Motion Design](https://github.com/lottiefiles/motion-design-skill) | `SKILL.md`, `director/decision-framework.md` | emotion/purpose-first motion choices; staging, timing/easing, personality and complexity limits |
| [Genjutsu](https://github.com/AThevon/genjutsu) | `README.md`, `skills/cast/SKILL.md`, `skills/paint/SKILL.md` | visual thesis, interaction thesis, single-effect versus full-identity routes, browser critique and audit |
| [Playwright Skill](https://github.com/lackeyjb/playwright-skill) | `skills/playwright-skill/SKILL.md` | preserved Python Playwright QA, stronger final binary PDF/HTML parity validation; duplicate user listing does not add a second runner |

These projects supply processes and conceptual guidance only. The `export_deck.py` packager is original code in this skill, not upstream GSAP/Playwright/Lottie code. Upstream library licensing must still be checked before vendoring its runtime code.
