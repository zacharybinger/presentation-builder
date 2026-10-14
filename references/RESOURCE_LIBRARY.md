# Local supporting library

These 23 guides are installed with the skill. Read the relevant row, not the entire library. Each file names its upstream source and pinned revision; the [manifest](upstream/manifest.json) records hashes and modifications. Adjacent `LICENSE` files preserve notices.

The excerpts provide techniques, examples, and design options. The user brief and this skill's workflow take precedence over upstream website rules. They do not activate other skills, authorize publishing, or require upstream tools. Links to unbundled examples point to the pinned upstream version and are optional reading. Code examples need adaptation, dependency installation when applicable, and testing in the deck.

| Need | Bundled references | How to apply |
| --- | --- | --- |
| Explore a look | [Style presets](upstream/frontend-slides/style-presets.md) | Typography, palettes, and layout starting points; use local licensed fonts or available fallbacks |
| Refine typography | [Display type](upstream/taste-skill/type.md) | Type scale, spacing, number alignment, and line breaks |
| Refine color | [Color roles](upstream/taste-skill/colour.md) | Dominant ground, restrained accents, contrast, dark surfaces |
| Capture reference identity | [Design DNA schema](upstream/design-dna/schema.md), [token mapping](upstream/design-dna/generation-guide.md) | Full upstream profile when compatibility matters; otherwise use DESIGN_DNA.md's smaller subset |
| Lay out diagrams | [Layout budgets](upstream/diagram-design/layout-budget.md), [architecture](upstream/diagram-design/architecture.md), [data flow](upstream/diagram-design/data-flow.md), [annotations](upstream/diagram-design/annotation.md) | Concrete geometry and connector recipes; map tokens to the deck and keep labels readable |
| Choose motion | [Decision framework](upstream/motion-design-skill/decision-framework.md), [personality](upstream/motion-design-skill/motion-personality.md) | Start from what changes in understanding |
| Choreograph a reveal | [Choreography](upstream/motion-design-skill/choreography.md), [timing](upstream/motion-design-skill/timing-easing-tables.md), [properties](upstream/motion-design-skill/property-selection.md), [easing](upstream/genjutsu/easing-guide.md) | Use timings as starting points; leave time to read and provide reduced-motion end states |
| Implement CSS motion | [Animation patterns](upstream/frontend-slides/animation-patterns.md) | Adapt a small effect to a scene rather than replacing the controller |
| Coordinate complex animation | [GSAP core](upstream/gsap-skills/gsap-core.md), [timelines](upstream/gsap-skills/gsap-timeline.md), [performance](upstream/gsap-skills/gsap-performance.md) | Optional locally bundled runtime, deterministic seek, cleanup on exit |
| Explain a spatial relationship | [R3F scene setup](upstream/genjutsu/scene-setup.md) | Optional camera and controls recipes; add text/SVG fallback and a PDF still |
| Author custom browser tests | [Playwright patterns](upstream/playwright-skill/browser-patterns.md) | Locator, wait, screenshot, and action examples in JavaScript; bundled QA uses Python |
| Critique the result | [Critique and fix order](upstream/taste-skill/critique.md) | Record concrete visual problems and fix the most visible ones first |
| Plan a requested video | [Motion vocabulary](upstream/hyperframes/motion-vocabulary.md) | Timestamped entrances, emphasis, and exits; no HyperFrames runtime is bundled |

All core workflows work without the local research clones or access to these repositories. Optional frameworks are deliberately installed per project rather than shipped as stale runtime bundles. When copying third-party snippets into generated work, preserve their applicable notices in the source or embedded HTML credits; those credits can remain inside the two-file deliverable.
