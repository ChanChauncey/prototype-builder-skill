---
name: prototype-builder
description: Build and iterate interactive web prototypes for product managers. Use this skill to turn product ideas into runnable pure HTML/CSS/JS multi-page main-flow prototypes with reusable left-side page tabs and right-side annotation capabilities, plus page navigation, form validation, state feedback, and testable task flows. Also use this skill when the user pastes a Figma link and asks for 1:1 restoration in the center canvas via figma-bridge. When information is missing, run a minimum question set first and ask follow-up questions only as needed.
---

# Prototype Builder

## Goal

Turn requirements into runnable pure HTML multi-page prototypes with usability first, visual consistency, and testable task flows.

## Rules

1. Run a minimum question set first, then ask only necessary follow-up questions.
2. Do not start coding before key requirements are clear.
3. Output in Simplified Chinese.
4. Interaction depth must include page navigation, form validation, and state feedback.
5. Default delivery is a complete multi-page main flow, not a single page mock.
6. Keep a reusable layout template with left page tabs and right annotation panel by default.

## Minimum Question Set

Collect at least:

1. Product goal and target users.
2. Core task and success criteria for this version.
3. Main flow start, end, and key steps.
4. Inputs, validation rules, and success or error feedback for each step.
5. Required states: empty, loading, error, no-permission, success.
6. Device scope: desktop, mobile, or both.
7. Visual preference and prohibited style choices.
8. Scope and priority boundary for MVP.
9. If user provides a Figma link, confirm target node/page and required restoration scope (full page or center canvas only).

Ask follow-up questions only for missing details that block implementation.

Use [references/discovery-question-bank.md](references/discovery-question-bank.md) for question templates.

## Workflow

1. Clarify: run minimum questions and follow-ups, then output a confirmed summary.
2. Model: produce page list, task flow, state matrix, and validation matrix.
3. Scaffold: create pure HTML page skeletons and shared styles.
4. Wire: implement navigation, validation, and state feedback.
5. Self-test: execute main-flow checks and fix blockers.
6. Deliver: provide run steps, page map, test cases, and known limits.

### MCP Config Workflow

When task requires Figma link restoration:

1. Do not auto-install Codex CLI or Figma MCP for the user.
2. Ask user to add the following MCP config entry:
3. Ensure MCP has an entry named `figma-bridge`:
   ```json
   {
     "figma-bridge": {
       "command": "npx",
       "args": ["-y", "@gethopp/figma-mcp-bridge"]
     }
   }
   ```
4. If `figma-bridge` is unavailable, report exact blocking reason and stop MCP-dependent restoration.

### Screenshot 1:1 Mode Workflow

When user asks to restore prototype from screenshots, use this mode:

1. Lock canvas size to screenshot pixel size (for example 1920x1080) before building.
2. Build a layout skeleton first (major blocks and coordinates), then fill typography and controls.
3. Use pixel values from screenshot geometry, avoid `%` for key spacing and key component sizes.
4. Keep one page per screenshot and name pages by screenshot sequence.
5. Run visual diff self-check and adjust until major blocks align.

### Figma Link 1:1 Restore Workflow

When user pastes a Figma URL and asks for 1:1 restoration, run this workflow:

1. Parse URL and extract `fileKey` and `nodeId` when available.
2. Use `figma-bridge` as the source of truth for structure, spacing, and styles.
3. Call `get_design_context` on selected node/page first, then map structure into prototype center canvas only.
4. Keep default left-page-tab and right-annotation framework unchanged unless user disables it.
5. Enforce canvas viewport parity with Figma frame size using explicit px values.
6. Reproduce major blocks and key controls in center canvas with target tolerance <= 2 px.
7. If exact local font is missing, use nearest fallback and record deviation in delivery notes.
8. Validate center canvas has no horizontal or vertical scrollbar in default desktop layout.
9. If multiple Figma pages/nodes are provided, generate one prototype page per node by default.
10. If center canvas cannot fully present the restored node, expand center panel width first (before shrinking/restyling target UI), while keeping left tabs and right annotations usable.
11. For visual assets in restored area (icons, illustrations, photos, masks, logos), use Figma-provided assets/URLs only; do not invent replacement art.

## Implementation Standard

1. Use semantic HTML and avoid framework dependency.
2. Use consistent design tokens: color, type scale, spacing, radius, shadow.
3. Keep navigation and button hierarchy consistent.
4. Add frontend validation and clear error copy for each key field.
5. Provide visible loading, success, and failure feedback for key actions.
6. Include empty and exception states on key pages.
7. Keep code modular; avoid a single massive file.
8. Always include reusable left-page-tab navigation and right-side annotation panel unless explicitly disabled by the user.
9. Annotation support must include add note, list notes, active note highlight, and drag note marker.
10. Keep annotation marker coordinates in the same scaling coordinate system as page content; prevent vertical-resize drift.
11. Annotation source of truth must be the current HTML file content, not browser cache.
12. Include a manual save action that writes annotations back into the current HTML file.
13. Each annotation row must include inline Edit and Delete actions.
14. Edit must happen directly in the page panel (inline input), not in modal/prompt dialogs.
15. Place `Add Note`, `Clear Notes`, and `Save HTML` on the same top action row.
16. Add-note interaction must be inline in the panel by creating an editable row directly; do not use prompt/modal dialogs.
17. Annotation text must support multiple lines for both editing and display.
18. Keep `Pages` and `Annotations` panels independently scrollable when content is long; avoid whole-page scrolling.
19. Support single-file delivery when requested: output one self-contained HTML without external CSS/JS files.
20. Before every file modification, create a versioned backup in `_backups`.
21. After every file modification, run a mojibake/encoding check.
22. If encoding issues are detected, immediately roll back to the latest backup and redo the change from that backup.
23. If user asks for final delivery artifact, default to a single-file `prototype.html` unless user explicitly asks for multi-file output.
24. In single-file mode, inline CSS/JS and remove external `link`/`script src` dependencies.
25. Avoid inline-script termination bugs: never place raw `</script>` string literals inside inline JS; use escaped form like `<\\/script>`.
26. Add/Edit interaction must be stable: entering edit mode must not collapse immediately from container re-render or bubbling side effects.
27. Keep annotation edit in-place until explicit `Save`/`Cancel`/`Delete`; no implicit close on generic click.
28. For delivered output directories, keep only required artifact(s) and move legacy generated files to `_backups`.
29. Enforce pre-delivery hard checks on final artifact: `.canvas` must use fixed aspect ratio (for example `aspect-ratio: 16 / 9`) and must not use `height: 100%` as marker coordinate reference.
30. Enforce pre-delivery interaction check: after resize (horizontal and vertical), marker-to-content relative position must remain stable.
31. Ensure top action row buttons are fully visible in default desktop layout; no truncation of labels such as `Save HTML`.
32. Treat center canvas as full prototype viewport: disallow horizontal and vertical scrollbars in the canvas content area.
33. If screenshot 1:1 mode is requested, prioritize structural and visual parity over generic component reuse.
34. In screenshot 1:1 mode, define viewport, sidebar width, header height, card size, and key offsets with explicit pixels.
35. In screenshot 1:1 mode, preserve screenshot page information architecture exactly; do not merge pages unless user asks.
36. In screenshot 1:1 mode, allowed deviation target is <= 2 px on major block edges and <= 1 px on icon/button size when practical.
37. In screenshot 1:1 mode, if fonts are unavailable locally, choose the nearest fallback and record the gap in delivery notes.
38. In screenshot 1:1 mode, do not remove the default left-page-tab and right-annotation framework unless the user explicitly disables it.
39. If screenshot parity conflicts with framework structure, keep the framework and apply 1:1 restoration only inside the center canvas area.
40. If Figma restoration is required, never auto-install Codex CLI or Figma MCP components.
41. Require MCP configuration entry `figma-bridge` and use it as the only design-context source.
42. If user provides a Figma link, prioritize figma-bridge driven restoration over screenshot-only inference.
43. For Figma-link tasks, implement 1:1 restoration in center canvas first, then adapt peripheral framework.
44. For Figma-link tasks, treat Figma frame dimensions as baseline viewport and keep major geometry in px.
45. For Figma-link tasks, avoid introducing extra sections/components not present in the selected Figma node.
46. For Figma-link tasks, complete an end check at 100% zoom comparing center canvas against Figma screenshot/context.
47. When center canvas is clipped in default desktop layout, prioritize expanding center column and canvas max-width (or reducing side-panel widths within readable limits) over altering Figma node geometry.
48. In Figma-link or screenshot restore tasks, all art assets must come from Figma exports/MCP URLs; prohibit agent-invented icons, avatars, illustrations, and decorative graphics.
49. If a Figma asset is temporarily unavailable, use neutral placeholder blocks only for blocked positions and mark each placeholder explicitly in delivery notes.

## Resource Usage

1. Read `references/discovery-question-bank.md` for discovery questions.
2. Read `references/prototype-qa-checklist.md` for QA and acceptance.
3. Read `references/template-left-tabs-right-annotations.md` for the reusable template contract.
4. Read `references/screenshot-restore-spec.md` when screenshot 1:1 restoration is requested.
5. Read `references/codex-cli-figma-mcp-bootstrap.md` when user asks how to configure `figma-bridge`.
6. Run `scripts/scaffold_prototype.py` to bootstrap the default reusable template structure.
7. For Figma-link restoration, use `figma-bridge` and prioritize `get_design_context` from selected node/page over manual guessing.

## Delivery Checklist

1. Runnable prototype files.
2. Page map and main-flow description.
3. Validation and state feedback notes.
4. Test steps for the main flow.
5. Known limitations and next iteration suggestions.
6. Verify critical runtime interactions in final artifact: page switching, add/edit/delete notes, drag marker, save action.
