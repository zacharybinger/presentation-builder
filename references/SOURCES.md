# Sources and curation decisions

The supplied research checkouts were reviewed for this 2.0.0 release. The [local library](RESOURCE_LIBRARY.md) contains 23 guides from nine repositories; [manifest.json](upstream/manifest.json) pins every source to the reviewed commit. The 2 GB `resources/` checkout folder is local research only and is not required after installation.

| Project | Included contribution | Curation boundary |
| --- | --- | --- |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | Style presets and CSS motion patterns | Omitted deployment scripts, remote font setup, and universal style bans. |
| [design-dna](https://github.com/zanwei/design-dna) | Full design profile schema and selected code-mapping guidance | Omitted CDN-loading instructions and measurement tools; small deck profiles remain supported. |
| [diagram-design](https://github.com/cathrynlavery/diagram-design) | Diagram geometry, connectors, density budgets, and annotation snippets | Omitted the renderer, large icon collections, and unrelated diagram catalogs. Tokens are adapted to the deck. |
| [gsap-skills](https://github.com/greensock/gsap-skills) | Core API, timelines, and performance guidance | Renamed guides avoid registering additional skills. GSAP runtime is optional and separately installed. |
| [motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | Purpose, personality, choreography, timing, and property choice | Heuristics inform judgment; no mandatory ambient animation or fixed effect count. |
| [genjutsu](https://github.com/AThevon/genjutsu) | Easing and R3F camera/scene/control patterns | Omitted multi-agent workflows, installation scripts, remote HDRI/model-loading examples. |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | Typography, color, and critique extracts | Omitted website-specific scoring caps, mandatory photos, universal font/color bans, and proprietary research claims. |
| [playwright-skill](https://github.com/lackeyjb/playwright-skill) | Locators, actions, waits, and screenshot patterns | Bundled Python QA is maintained here; no dependency on the upstream Node runner. |
| [hyperframes](https://github.com/heygen-com/hyperframes) | Motion vocabulary for a requested video companion | No CLI, renderer, registry, media, or publishing workflow is bundled. |

## Link-only resources

- [threejs-skills](https://github.com/CloudAI-X/threejs-skills): no license file in the supplied snapshot; no files copied. Use the licensed local Genjutsu reference or official Three.js docs.
- [shadcn/ui](https://ui.shadcn.com/), [21st.dev](https://21st.dev/), and [thinking-orbs](https://github.com/Jakubantalik/thinking-orbs): optional integrations, not default dependencies. Inspect the selected component and current license before copying.

## Project-owned resources

The starter, Python helpers, presentation-specific guides, and integration recipes are maintained in this repository. `examples/explainer-original/` retains the supplied four-chapter prototype unchanged. Its scientific examples demonstrate an interaction pattern and should be checked before reuse as factual teaching material.

See [third-party notices](../THIRD_PARTY_NOTICES.md) for copyright and redistribution details.
