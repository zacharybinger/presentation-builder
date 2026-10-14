# Implementation recipes (optional React/3D/video upgrade path)

The included Vite-free starter is the default. Only choose the React route when interaction complexity or the requested component requires it. Never copy these snippets without wiring them to a particular story and reviewing current upstream package APIs.

## A. React + shadcn slider controlling an explanatory SVG

After creating a Vite/React/TypeScript app, initialize shadcn/ui using its current Vite instructions and add `slider`.

```tsx
import { useState } from 'react';
import { Slider } from '@/components/ui/slider';

const links = [{id:'A',weight:.91},{id:'B',weight:.63},{id:'C',weight:.37}];
export function ThresholdExplain() {
  const [threshold,setThreshold] = useState(50);
  const active = links.filter(link => link.weight*100 >= threshold);
  return (
    <section aria-label="Threshold demonstration">
      <label id="threshold-label">Minimum connection weight: {threshold}%</label>
      <Slider value={[threshold]} onValueChange={([value]) => setThreshold(value)} min={0} max={100} step={1} aria-labelledby="threshold-label" />
      <svg viewBox="0 0 560 160" role="img" aria-label={`${active.length} of three connections meet the threshold`}>
        {links.map((link,i) => <g key={link.id} opacity={active.some(x=>x.id===link.id)?1:.14}>
          <path d={`M 20 75 L 480 ${35+i*42}`} fill="none" stroke="currentColor" strokeWidth={5*link.weight} />
          <text x="490" y={35+i*42}>{link.id}</text>
        </g>)}
      </svg>
      <p aria-live="polite">{active.length} / 3 paths remain.</p>
      <button onClick={() => setThreshold(50)}>Reset example</button>
    </section>
  );
}
```

For a production scene, include axes, marker legends, semantic colors, and a sentence explaining what the output means. Do not encode accessible semantics only in SVG opacity.

## B. 21st.dev editorial component gate

1. Decide on one layout need (animated hero, immersive gallery, shader backdrop, transition mask).
2. Browse the relevant 21st.dev category; inspect previews and author-specific license.
3. Choose one candidate, copy its source or use its documented registry command.
4. Delete generic copy/background color; map CSS to `--ground`, `--ink`, `--primary`, `--secondary`.
5. Keep its animation scoped to a single scene and avoid continuous motion when speaker is talking.
6. Check bundled asset and dependency weight; ensure offline operation after build.
7. Inspect screenshot and interaction in Chromium. Reject if it distracts from narrative, makes labels hard to read, or fails reduced motion.

## C. Agent process illustration with thinking-orbs

```tsx
import { ThinkingOrb } from 'thinking-orbs';

export function AgentStatus({phase}:{phase:'searching'|'solving'|'composing'|'idle'}) {
  const state = phase==='idle' ? 'breathing' : phase;
  return <figure>
    <ThinkingOrb state={state} size={64} theme="dark" paused={phase==='idle'} />
    <figcaption>{phase==='idle' ? 'Agent is ready' : `Agent is ${phase}`}</figcaption>
  </figure>;
}
```

In a real presentation, `phase` should derive from a real agent trace or a clearly labeled simulated sequence. Do not pretend an AI tool is working solely because an orb is animating.

## D. Three.js only for spatial reasoning

```ts
import * as THREE from 'three';
const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(width,height);
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(45,width/height,.1,100);
camera.position.set(0,0,5);
const geometry=new THREE.SphereGeometry(1,32,24);
const material=new THREE.MeshStandardMaterial({color:0x72e6c5});
const mesh=new THREE.Mesh(geometry,material); scene.add(mesh);
scene.add(new THREE.AmbientLight(0xffffff, 0.6));
const key=new THREE.DirectionalLight(0xffffff, 2);
key.position.set(3,4,5); scene.add(key);
// Orbiting / animation must serve the scene's explanation; this is only a scaffold.
renderer.render(scene,camera);
function dispose(){ geometry.dispose(); material.dispose(); renderer.dispose(); }
```

For a React/R3F scene use component lifecycle to dispose resources automatically where supported, control frames via `frameloop='demand'` when static, pause updates offscreen, constrain orbit controls, and offer SVG/still alternative.

## E. Film version via HyperFrames

If the user requests a video **in addition to** the interactive deck:

- Extract slide/reveal matrix into timestamped beats (every transition has an explicit duration and purpose).
- Identify "carrier" objects reused across scene seams.
- Author a HyperFrames scene with seekable HTML/CSS animations according to its current router and quickstart.
- Render key frames around each boundary, catch flashes/gaps and text overflows, then generate MP4.
- Keep the original interactive HTML deliverable separate. A video cannot retain pointer/keyboard-driven scenes.

The HyperFrames repository version and CLI may change; consult its current docs for exact commands rather than fabricating invocation flags.
