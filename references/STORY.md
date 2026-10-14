# Narrative and learning design

## Content pass

1. Identify one desired audience belief, skill, or decision; everything else supports it.
2. Record what the user actually supplied: facts, figures, formulas, code, screenshots, constraints, citations. Preserve uncertainty and wording when important. Do not silently invent a business metric.
3. Split ideas into **claims + evidence**. For a technical tutorial, split a mechanism into input → transformation → output → failure mode → practice.
4. Choose storyline: explanation (`why → parts → mechanism → worked example → consequence`), pitch (`tension → insight → solution → proof → ask`), update (`headline → evidence → diagnosis → options → decision`), demo (`problem → interaction → feedback → implication`).
5. Write a 1–3 sentence **speaker note** for each scene; put detail there rather than cramming it onto the stage.
6. Create the slide/reveal matrix and design the densest final reveal first.

## Narrative rules

- Give each slide a clear purpose. Setup and definitions can use direct topic titles; use a factual takeaway when the evidence supports one.
- One reveal = one added causal link, comparison, highlight, demonstration, or result. A reveal that only animates arbitrary decoration does not count.
- Prefer a persistent scene that becomes more sophisticated over time to five disconnected diagrams.
- A concrete example should remain visible while abstract terms are introduced.
- Distinguish measured data, hypothetical sample data, simplification, and illustrative layout in labels/notes.
- Use adjacent slides for contrast and callback: the new slide borrows a color/shape/word from the preceding visual.
- Include a meaningful ending: answer the opening tension, show a synthesized model, and explain a useful action.

## Default content limits (adapt to format)

- Speaker-led: title ≤2 lines; 1–3 short statements; one strong hero visual; normal body copy ≥24px on a 1600×900 canvas; annotations ≥17px whenever possible.
- Reading-first: multiple panels and supporting labels are allowed; split instead of shrinking below legibility.
- Deep technical schematics: diagrams have zoom/expand affordance or their own slide if labels would become tiny.
- Diagram complexity: a figure with ~9+ meaningful nodes often deserves a build-up or decomposition.

## Example reveal matrix

| Slide | Claim | Evidence | Visual | Reveals |
|---|---|---|---|---|
| 1 | A bottleneck drives the result | data point | large statement + chart | 1 |
| 2 | Three mechanisms create it | simplified process | connected SVG graph | 4: nodes → edges → bottleneck → consequence |
| 3 | Tuning one parameter shifts output | labeled simulation | slider with outputs | 2: baseline → adjustable tradeoff |
| 4 | A specific change resolves it | comparison metric | shared before/after diagram | 3: current → intervention → result |

## Input-to-deck prompt contract

When a user hands you raw notes, infer and write an internal brief:

```yaml
purpose: explain | persuade | demo | review
audience: who, domain background
outcome: single takeaway
primary_sources: user files or verified links
facts_to_preserve: list with source provenance
length: slide target or inferred reasonable count
density: speaker-led | reading-first
art_direction: a subject-specific visual thesis
interactive_moments: list of audience actions and what changes
exports: [offline-html, static-pdf]
```

The core deliverable is still the runnable deck; a brief is a planning tool, not an excuse to stop before implementation.
