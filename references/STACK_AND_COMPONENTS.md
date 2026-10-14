# Integration guide: stack, component libraries, rendering

## Decision tree

**Vanilla HTML + CSS + SVG + small JS controller** (default): decks where text, shapes, progressive diagrams and a few interactive controls carry the talk. Portable, fast, offline, easy to screenshot. Use `templates/interactive-deck/`.

**React + Vite + TypeScript**: when one or more scenes have substantial shared state, dynamic lists, libraries requiring React, multiple synchronized visualizations, or intricate accessibility. Start with Vite (`npm create vite@latest deck -- --template react-ts`); add libraries only after mapping the scene requirements; pin versions with a lockfile; verify static production build (`npm run build`), use relative asset paths for static hosting.

**Optional packages** (as required, not obligatory): Motion for transition/state orchestration; D3 for data-driven SVG; `@react-three/fiber` and `@react-three/drei` for 3D React scenes; `three` for vanilla WebGL; `thinking-orbs` for agent activity widgets; `recharts` for conventional charts. Do not depend on a package solely for an entrance fade.

## shadcn/ui — https://ui.shadcn.com/

Use it for well-tested interaction semantics: Dialog, Slider, Tooltip, Popover, Tabs, Toggle Group, Command, or Switch. shadcn is **component source brought into your project**, not one all-inclusive UI runtime. To bootstrap in Vite use the current setup flow in https://ui.shadcn.com/docs/installation/vite (`npx shadcn@latest init -t vite`) and add relevant controls (`npx shadcn@latest add slider tabs tooltip`). Keep keyboard focus and label behavior. Remove default dashboard-like chrome and restyle variables to your presentation direction. A control belongs only if the audience can actually change something.

## 21st.dev — https://21st.dev/

A discovery/registry layer for expressive React components, animated hero blocks, shaders, gradients, galleries, and visual motifs, many in shadcn-compatible form. Browse and **select by a particular scene's need**; inspect live preview + code + dependencies + license + performance + fallback before incorporation. Add via the provider's documented instructions/registry command or adapt a copy prompt; do NOT assume all assets come from a unified `21st.dev` npm package. Favor source-specific hero/diagram assets; do not stack five competing effects.

Selection checklist:
- Does it communicate something about *this subject*?
- Will it remain readable at 1280×720 projector scaling?
- Do the props actually respond to a presentation-specific interaction?
- Does it run offline after installation/build?
- Are the dependencies/licenses compatible with redistribution?
- Does `prefers-reduced-motion` yield a meaningful still frame?

## thinking-orbs — https://github.com/Jakubantalik/thinking-orbs

Use a `ThinkingOrb` for a real process/state (agent solving, searching, listening, etc). Library is canvas 2D, not Three.js; published as `thinking-orbs` with React peer dependency. Current upstream examples:

```tsx
import { ThinkingOrb } from 'thinking-orbs';

export function LiveReasoningState({ running }: { running: boolean }) {
  return <div aria-live="polite">
    <ThinkingOrb state={running ? 'solving' : 'breathing'} size={64} paused={!running} theme="dark" />
    <span>{running ? 'Evaluating tool results…' : 'Idle / ready'}</span>
  </div>;
}
```

Only show a claimed agent state when real application state supports it. Prefer static annotation for purely conceptual slides. The upstream package supports reduced motion and off-screen pausing.

## Three.js and R3F

Appropriate when topology/depth/physical spatial constraints are the explanation: point clouds, embedding manifolds, orbit cameras, 3D network surfaces, volumetric domains. Keep labels outside 3D wherever possible; use raycast hit testing, simple camera control, capped pixel ratio, controlled frame rate, cleanup (dispose renderer/geometries/materials). Freeze or render stills for non-3D clients. See `references/VISUALS_AND_MOTION.md`.

## HyperFrames — https://github.com/heygen-com/hyperframes

Use only for a **separate timed render** when the requested artifact includes a video or narrated MP4. HyperFrames renders HTML/CSS and seekable animation deterministically. It does not make a video file interactive. Consult upstream `/hyperframes` router and video rendering instructions on demand; do not claim generic CSS transitions inside a live deck can be exported frame-perfect without converting them into a seekable timeline. Label the rendered video as a companion export.

## Source constraints and security

Pin versions, review license, avoid remote CDN fonts/scripts/media for on-prem and live talks, provide attributions for image/illustration/code assets, sanitize imported Markdown/HTML, do not execute arbitrary JS from user documents, and never paste credentials into deck assets. Exportable HTML must use local assets or explicit approved external URLs with an offline fallback.
