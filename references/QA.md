# Browser QA, accessibility, and delivery gates

## Automated checks

Run on an unrestricted workstation:

```bash
python scripts/check_deck.py ./my-deck --out ./deck-qa
```

If Chromium is administratively blocked from all URL navigation, use the in-memory fallback:

```bash
python scripts/preview_deck.py ./my-deck --out ./deck-preview
```

This fallback actually renders and tests controls, but **does not** validate real URL or history behavior. It is not a substitute for the full HTTP test.

Requires `playwright` for Python and Chromium. In a clean environment:

```bash
python -m pip install playwright pillow
python -m playwright install chromium
```

The runner can use system Chromium when available. It serves the folder on loopback, captures every slide's final reveal and a first-slide screenshot, checks URL state, Arrow navigation, slide selection, the working slider and reset, browser JS errors, and bounded stage layout at 1440×810 and 390×844. It writes `report.json`, screenshots, and optional `contact-sheet.png` (Pillow). When using a custom React deck instead of the starter, rewrite/add assertions specific to real widgets and roles; generic screenshots alone do not prove interactions.

## Manual visual review (mandatory)

Review screenshots at 1600×900, 1280×720, 1440×810, and one phone viewport. Fixed 16:9 decks should **letterbox**, not reflow to 9:16; inspect legibility rather than pretending a projector deck is a mobile app. Specifically check every final reveal: annotation collision, skinny SVG lines, number formatting, title wraps, cutoff logos, focus rings, dead controls, color contrast, clipped chart labels. View on a real browser, not just HTML source.

## Functional tests

- ArrowRight/Space advance; ArrowLeft reverses; first/last bounds do not throw.
- Keyboard events inside inputs, selects, sliders, textarea, buttons do not advance accidentally.
- Prev/Next buttons, direct slide navigation, URL query parameters (`slide`, `step`, `theme`) and browser back/forward resolve to the same state.
- Fullscreen works or fails gracefully; Escape is left to browser fullscreen behavior.
- Widgets update the chart and explanatory text, and have a reliable reset.
- Reduced-motion preference yields meaningful still states; transitions never hide critical content forever.
- Keyboard focus visible and target sizes practical; SVG images have text equivalents; dynamic results have aria-live regions where appropriate.
- No app script error, unloaded media, stray browser scrolling or off-stage overflow.

## Source, accuracy, and safety

- Keep all user-provided facts traceable; note assumptions and oversimplifications. Technical claims, charts, performance comparisons and algorithm demos must be truthful or explicitly labeled illustrative.
- External images and components must have licenses/attribution reviewed. Don't add unnecessary remote dependencies or encode user documents in external requests.
- Fonts should be bundled only when properly licensed; fallback stack must work offline.
- When showing code snippets, keep them small, syntax readable and use `textContent` rather than dangerous HTML insertion for dynamic untrusted input.

## Required publishing gate

`python scripts/export_deck.py ./my-deck --out ./deliverable` must create **one** `presentation.html` and **one** `presentation.pdf`, not a ZIP or multi-file site. Open/review the HTML in an offline browser and render/review **all** PDF pages. Assert PDF page count, 16:9 format and extractable text; verify complex widgets have a meaningful static result, not an empty first frame. See `references/EXPORT.md`.

## Export limitations

- Browser share: exactly **one standalone HTML** with all resources embedded, no server or online assets required.
- PDF: **mandatory**, use `export_deck.py` (Playwright browser printing and PDF assembly) per slide/state; freezes animations and widgets. Check page size and full render.
- PPTX: create image-backed slides or native approximations; interactivity does not transfer.
- Video: need a separately authored seekable timeline (HyperFrames), not static PDF or a capture of random interactions.

Never claim the HTML deck has a verified PDF, PowerPoint, or MP4 export unless you actually generated and checked those artifacts.

After exporting: `python scripts/verify_exports.py ./deliverable/presentation.html ./deliverable/presentation.pdf`. This checks HTML resource integrity, browser interactions, mobile scaling, PDF 16:9 pages, PDF selectable text, and page counts (the default final-reveal export; for `--include-reveals`, adjust or skip the page-count assertion).
