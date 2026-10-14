# Motion direction, choreography, and runtime engine

**Source ideas:** [GreenSock gsap-skills](https://github.com/greensock/gsap-skills) (`gsap-core`, `gsap-timeline`, `gsap-performance`, optional `gsap-scrolltrigger` / `gsap-plugins`), [LottieFiles motion-design-skill](https://github.com/lottiefiles/motion-design-skill) (director / choreography / timing & easing), [Genjutsu cast](https://github.com/AThevon/genjutsu/tree/main/skills/cast) (interaction thesis), and existing HyperFrames guidance.

## Motion direction order (before code)

For each beat fill `who moves → why → from state → to state → causal trigger → emotional intent → freeze state for PDF`. Select ONE motion personality (subtle/premium, energetic, playful, technical) and one dominant spatial current for the deck. Use the most conspicuous motion sparingly. Choreograph a primary element, optional secondary feedback, and ambient texture only if content remains legible. The **purpose** is comprehension, not a numerical count of animated elements.

Pick **native CSS** for small non-interrupted transitions and `prefers-reduced-motion`. Pick **GSAP** when coordinating multiple objects over time, when progress needs seeking or reversal, or for intricate SVG paths / FLIP; do not add GSAP simply for a fade. Pick **Lottie** for prepared vector character/brand animations, not as the default for interactive system diagrams (LottieFiles' motion-design-skill itself is implementation-agnostic). Pick **Three.js** for genuine 3D spatial reasoning. **HyperFrames** is reserved for optional MP4/video output, separate from HTML/PDF.

## GSAP recipe: reversible explanatory sequence

```js
// Assumes GSAP has been compiled into this presentation's JS bundle.
// GSAP must NOT be fetched from a CDN by the final standalone HTML.
const timeline = gsap.timeline({ paused: true, defaults: { duration: 0.5, ease: 'power2.out' } });
timeline.addLabel('input', 0)
  .fromTo('.signal', { opacity: 0, x: -30 }, { opacity: 1, x: 0 }, 'input')
  .addLabel('transform', '+=0.1')
  .to('.signal', { x: 200, duration: 0.65 }, 'transform')
  .fromTo('.result', { opacity: 0, scale: .9 }, { opacity: 1, scale: 1 }, 'transform+=0.3');

const milestones = ['input', 'transform'];
function goToReveal(n, instant = false) {
  const target = milestones[Math.max(0, Math.min(n, milestones.length - 1))];
  if (instant || matchMedia('(prefers-reduced-motion: reduce)').matches) timeline.seek(target, false);
  else timeline.tweenTo(target);
}
// For PDF, seek explicitly to the meaningful final end-state.
window.__presentationExport = {
  frames: () => [{index: 0, steps: 2, title: 'Signal processing'}],
  goto: (_, step) => goToReveal(step, true),
  freeze: () => { timeline.pause().progress(1); }
};
```

**Important:** The example's timeline labels are illustrative; map each reveal index to the proper actual label/end time, and test all intermediate states. For complex diagrams, preserve nodes across beats rather than rebuilding DOM and resetting every animation on each advance.

### GSAP engineering rules

- Use labeled `gsap.timeline({paused:true})`, nested timelines where useful, and position parameters (`'<', '+=0.2', 'label+=0.1'`) instead of hand-written delay chains.
- Keep reveal state **seekable** and deterministic; PDF exporter should `goto(scene, finalStep)` then `freeze()`.
- Animate transforms/opacity whenever possible, batch layout reads/writes, use stagger sparingly, scope selectors to a slide, and kill/revert timelines when scenes unmount (in React use `gsap.context` / current `useGSAP` pattern).
- Register required plugins once. Inspect plugin licensing and versions before embedding vendor code. Build GSAP into a local *single* output JS bundle (Vite/Rollup/esbuild) before calling `export_deck.py`; no CDN link survives.
- `ScrollTrigger` only if deliberately creating a scrollytelling deck; do not let scroll and arrow-based reveal controllers compete.
- `gsap.matchMedia()` or equivalent must honor reduced motion. Do not hide information from reduced-motion or print views.

### Lottie and timeline assets

If using Lottie JSON/dotLottie + player, compile or vendor the player and embed animation bytes/data into the exported HTML. Avoid lazy fetching assets from network or relative `.json` paths. Ensure exporter can freeze on a selected, content-complete frame (not frame zero), and provide static SVG/HTML fallback for PDF and reduced-motion. Bundled HTML must be fully functional offline; test in a network-blocked browser.

### Genjutsu-style microinteraction criteria

Before implementing a 'wow moment' state an interaction thesis, including what data or causal relationship changes. Validate both pointer and keyboard affordances. A speculative shimmer with no changed meaning is not a justification for a dependency. Always inspect a screenshot and confirm the effect stops or pauses when leaving its scene.

## Cross-format continuity

The live HTML is the authoritative **interactive** master. The PDF is a frozen narrative, never purported to be interactive; one PDF page per final slide is default. For complex GSAP morphs/canvas/3D/Lottie scenes, always author a legible deterministic print snapshot or `freeze` adapter and compare the PDF render against a browser screenshot. If content only exists in an interactive tooltip, convert it into a visible annotation before PDF export or add a separate PDF-friendly slide.
