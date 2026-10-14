> Curated from [genjutsu](https://github.com/AThevon/genjutsu/blob/1f518a71378b15d423389e546e767cffc86e14c3/skills/_jutsu/threejs-r3f/references/scene-setup.md), revision `1f518a71378b`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Optional React/Three.js route. Keep the canvas inside the slide, add accessible static content, and supply a PDF still.

## Minimal Canvas Setup

```tsx
import { Canvas } from '@react-three/fiber'
import { Suspense } from 'react'

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Canvas
        camera={{ position: [0, 2, 5], fov: 45, near: 0.1, far: 100 }}
        dpr={[1, 2]}
        gl={{ antialias: true, alpha: false, powerPreference: 'high-performance' }}
      >
        <Suspense fallback={null}>
          <Scene />
        </Suspense>
      </Canvas>
    </div>
  )
}
```

**Props breakdown:**
- `dpr={[1, 2]}` -- clamp device pixel ratio (retina without burning GPUs)
- `alpha: false` -- opaque background = faster compositing
- `powerPreference: 'high-performance'` -- request discrete GPU on laptops
- `frameloop="demand"` -- add for static scenes (render only on invalidate)

---

## Camera Configurations

### Perspective (default, most scenes)

```tsx
<Canvas camera={{ position: [0, 2, 5], fov: 45 }}>
```

- **fov 35-45:** Natural, cinematic feel
- **fov 60-75:** Wider, more immersive
- **fov 20-30:** Telephoto, compressed depth

### Orthographic (isometric, UI, 2D-in-3D)

```tsx
<Canvas orthographic camera={{ position: [0, 5, 10], zoom: 50 }}>
```

### Animated Camera (smooth transitions)

```tsx
import { useFrame, useThree } from '@react-three/fiber'
import { useMemo } from 'react'
import * as THREE from 'three'

function CameraRig({ target }: { target: [number, number, number] }) {
  const _target = useMemo(() => new THREE.Vector3(), [])
  const _position = useMemo(() => new THREE.Vector3(), [])

  useFrame((state, delta) => {
    // Smooth lerp to target
    _target.set(...target)
    state.camera.position.lerp(_position.set(target[0], target[1] + 2, target[2] + 5), delta * 2)
    state.camera.lookAt(_target)
  })

  return null
}
```

---

## Controls

### OrbitControls (inspect / product viewer)

```tsx
import { OrbitControls } from '@react-three/drei'

<OrbitControls
  makeDefault
  enableDamping
  dampingFactor={0.05}
  minDistance={2}
  maxDistance={20}
  minPolarAngle={0}
  maxPolarAngle={Math.PI / 2}    // prevent going below ground
  autoRotate={false}
  autoRotateSpeed={0.5}
/>
```

### PresentationControls (drag-to-rotate, bounded)

```tsx
import { PresentationControls } from '@react-three/drei'

<PresentationControls
  global                         // listen on entire canvas
  snap                           // snap back to rest
  speed={1.5}
  zoom={0.8}
  rotation={[0, -Math.PI / 4, 0]}  // initial angle
  polar={[-Math.PI / 4, Math.PI / 4]}
  azimuth={[-Math.PI / 4, Math.PI / 4]}
>
  <Model />
</PresentationControls>
```

### MapControls (top-down, pan-based)

```tsx
import { MapControls } from '@react-three/drei'

<MapControls
  makeDefault
  enableRotate={false}
  minDistance={5}
  maxDistance={50}
/>
```

### Pointer-based camera (follow cursor)

```tsx
function PointerCamera() {
  useFrame((state) => {
    const { x, y } = state.pointer // normalized -1 to 1
    state.camera.position.x = THREE.MathUtils.lerp(state.camera.position.x, x * 2, 0.05)
    state.camera.position.y = THREE.MathUtils.lerp(state.camera.position.y, y * 1.5 + 1, 0.05)
    state.camera.lookAt(0, 0, 0)
  })
  return null
}
```

---

## Responsive Canvas

### Fill parent container

```tsx
// Parent must have explicit dimensions
<div style={{ width: '100%', height: '100vh' }}>
  <Canvas>
    <Scene />
  </Canvas>
</div>
```

### Respond to viewport size inside scene

```tsx
function ResponsiveObject() {
  const { viewport } = useThree()
  // viewport.width/height = world units visible at z=0

  return (
    <mesh scale={viewport.width > 6 ? 1 : 0.6}>
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  )
}
```

### Adaptive performance

```tsx
import { PerformanceMonitor } from '@react-three/drei'

<Canvas>
  <PerformanceMonitor
    onIncline={() => setDpr(2)}
    onDecline={() => setDpr(1)}
  >
    <Scene />
  </PerformanceMonitor>
</Canvas>
```

---
