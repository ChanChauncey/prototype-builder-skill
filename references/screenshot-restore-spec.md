# Screenshot Restore Spec (1:1)

## Goal

Rebuild prototype pages from screenshots with near pixel-level visual parity.

## Inputs

1. One or more screenshots.
2. Target viewport size for each screenshot.
3. Optional: preferred font family and acceptable fallback.

## Output Contract

1. One HTML page per screenshot by default.
2. Shared CSS tokens, but page-level pixel geometry must stay explicit.
3. No framework dependency.
4. Provide a short parity report with known gaps.

## Geometry Rules

1. Lock design baseline to screenshot width/height.
2. Use px for major block geometry (x/y/width/height/padding/radius).
3. Avoid responsive reflow before baseline parity is reached.
4. After baseline parity, add adaptive behavior for smaller screens only.

## Visual Rules

1. Match background, border, radius, and shadow intensity first.
2. Match typography hierarchy: size, weight, color, line-height.
3. Match icon and avatar containers with exact box size.
4. Keep spacing rhythm identical to screenshot.

## Interaction Rules

1. Keep page tabs and major CTA clickable.
2. Preserve visible hover/active states where identifiable.
3. If interaction details are unknown from screenshot, use neutral defaults and mark assumptions.

## QA Procedure

1. Render page at baseline viewport.
2. Capture screenshot from browser.
3. Compare against target screenshot.
4. Iterate geometry and style until major blocks pass tolerance.
5. Record unresolved diffs and reasons.
