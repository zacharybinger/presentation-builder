# Browser and visual QA

Use Python 3.10+, the packages in `scripts/requirements.txt`, and Playwright Chromium. Run from the skill root or invoke scripts by absolute installed path.

```bash
python scripts/check_deck.py ./my-deck --out ./deck-qa
```

The checker serves the folder on loopback and validates the export interface. It visits every scene/reveal, checks stage and text/control bounds, records script/console errors, and captures completed scenes. It checks 1440×810, 1280×720, 1920×1080, and 390×844 viewports. Starter controllers receive keyboard, URL, and browser history checks. A one-scene deck is valid.

`report.json` lists checks, failures, and anything not tested. Screenshot names use scene numbers, not user-provided titles. The contact sheet supports review; inspect individual frames at full size where detail matters. Bounds checks detect common clipping but cannot prove that overlapping text is readable.

## Actual widget assertions

The default checker does not assume that the deck contains the demo slider or inspector. Supply a trusted local Python module with this interface:

```python
def exercise(page, check):
    # Navigate to the scene first using its real controller.
    page.get_by_role('slider', name='Allocation percentage').fill('70')
    check('Allocation updates result', page.locator('#result').inner_text() == '70%')
```

```bash
python scripts/check_deck.py ./my-deck --out ./deck-qa --interaction-test ./deck_interactions.py
# Only for the unmodified starter:
python scripts/check_deck.py ./my-deck --out ./deck-qa --interaction-test scripts/starter_interactions.py
```

Test observable outcomes, reset behavior, keyboard focus, and input handling. Add custom keyboard/deep-link tests for a nonstarter controller. Avoid asserting only that a click succeeded. The [local Playwright patterns](upstream/playwright-skill/browser-patterns.md) show locator and wait approaches; those examples use JavaScript, while these helpers use Python.

## Visual and accessibility review

Inspect every completed scene and intermediate states where reveals overlap. Check typography, line breaks, content coverage, source citations, numerical units, chart labels, focus rings, contrast, and media loading. Confirm motion changes meaning and reduced motion retains the information. Check a normal-motion run when adding animations; a reduced-motion screenshot alone does not validate choreography.

A fixed 16:9 deck letterboxes on portrait screens. Do not call it a readable phone layout just because the stage fits. Keep alternative text for diagrams, visible labels for controls, and live announcements for changing results. Fullscreen should work or fail gracefully. Hidden reveals should be inert, and keyboard use in widgets should not advance the deck.

Intentional decoration can overflow; put `data-allow-overflow` on that decoration only. Do not use it to silence clipped evidence or labels. Use `data-check-bounds` on custom evidence containers that need explicit checking.

## Export review

```bash
python scripts/export_deck.py ./my-deck --out ./deliverable
python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf
python scripts/render_pdf.py ./deliverable/presentation.pdf --out ./pdf-review
```

The standalone verifier blocks network access and checks all reveals. PDF checks cover geometry, count (including `--include-reveals` exports), and selectable text. Open every rendered PDF page and compare its conclusion to the matching HTML state. A good interactive state may still need a different static explanation.

If URL navigation is blocked, `preview_deck.py ./my-deck --out ./deck-preview` can render in memory. It does not test widgets, keyboard navigation, native opening, or browser history. The verifier also has an explicit `--in-memory` fallback. Disclose those gaps and never invent successful checks.
