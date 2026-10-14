> Curated from [motion-design-skill](https://github.com/LottieFiles/motion-design-skill/blob/f9a8a041b85185ee4881b3471d3415e939aac772/skills/motion-design/director/decision-framework.md), revision `f9a8a041b851`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Timing and density numbers are design heuristics. Reduced motion must retain the information; ambient motion is optional.

# Decision Framework

## The First Questions

### 1. Purpose?

| Purpose | Approach | Priority |
|---------|----------|----------|
| Draw attention | Scale, color, pulse | Responsiveness |
| Guide sequence | Stagger, directional flow | Clarity |
| Provide feedback | Immediate response | Speed |
| Create atmosphere | Subtle, continuous | Subtlety |
| Explain relationship | Position, connection | Legibility |
| Celebrate/reward | Overshoot, particles | Delight |

### 2. Audience?
- Stressed → calm motion; Browsing → richer motion
- Task-focused → fast, minimal; Exploring → can be dramatic
- Seen 100x/day → fast, subtle; Seen once → can be dramatic

### 3. Context?
- Busy layout → simpler motion; Empty → can be dramatic
- Other animations active → coordinate or stagger
- Small container → small motion

## 4-Level Decision Hierarchy

### Level 1: Motion Category

| Category | When |
|----------|------|
| Revealing | Content appearing |
| Concealing | Content disappearing |
| Transitioning | Between states/views |
| Emphasizing | Drawing attention |
| Responding | Reacting to interaction |
| Ambient | Background atmosphere |

### Level 2: Motion Personality
Match to brand. See [motion-personality.md](https://github.com/LottieFiles/motion-design-skill/blob/f9a8a041b85185ee4881b3471d3415e939aac772/skills/motion-design/director/motion-personality.md).

### Level 3: Motion Direction

| Direction | Communicates |
|-----------|-------------|
| Upward | Growth, aspiration |
| Downward | Settling, completion |
| Leftward | Regression, departure |
| Rightward | Progression, arrival |
| Outward (scale up) | Importance, emergence |
| Inward (scale down) | Dismissal, removal |
| Center-seeking | Focus, convergence |
| Center-fleeing | Distribution, release |

### Level 4: Implementation Properties
Choose animated properties. See [property-selection.md](https://github.com/LottieFiles/motion-design-skill/blob/f9a8a041b85185ee4881b3471d3415e939aac772/skills/motion-design/reference/property-selection.md).

## Decision Quick-Path

```
1. PURPOSE → What does this motion DO?
   ├── Feedback → short, ease-out, minimal
   ├── Entrance → ease-out, personality-matched
   ├── Exit → ease-in, 70% of entrance
   ├── Emphasis → scale or color pulse
   └── Ambient → slow, continuous, sine

2. PERSONALITY → Match keywords
   ├── Fun/bouncy → Playful
   ├── Elegant/luxury → Premium
   ├── Clean/professional → Corporate
   └── Bold/dynamic → Energetic

3. PROPERTIES → Minimum needed (two = sweet spot)

4. TIMING → Check duration table, adjust for distance/weight

5. EASING → Entering=ease-out, Leaving=ease-in, On-screen=ease-in-out, Looping=sine
```

## Evaluation Before Delivery

| Check | Question |
|-------|----------|
| Purpose | Clear function? |
| Personality | Matches brand/context? |
| Repetition | Fine on 100th viewing? |
| Attention | Respects viewer's focus? |
| Hierarchy | Reinforces importance? |
| Layers | Primary + secondary + ambient? |
| Timing | Duration appropriate? |
