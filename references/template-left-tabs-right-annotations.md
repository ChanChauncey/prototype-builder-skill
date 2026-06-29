# Reusable Template: Left Tabs + Right Annotations

## Purpose

Provide a reusable baseline layout for product prototype pages:

1. Left panel: page tab list for quick page switching.
2. Center panel: canvas area for current page content.
3. Right panel: annotation tools and annotation list.

## Required UI blocks

1. `layout`: three-column grid with left tabs, center canvas, right annotation panel.
2. `tabs`: static links to all pages, with active state on current page.
3. `annotation-layer`: overlay layer in canvas for note markers.
4. `annotation-list`: right panel list showing note index and content.
5. `add-note-btn`, `clear-note-btn`, `save-note-btn`, `save-status`.

## Required behaviors

1. Add note: create a new note row in inline edit mode with default marker position.
2. Select note: sync active style between marker and list item.
3. Drag marker: update note coordinates while dragging.
4. Save to HTML: write notes back to current page HTML data block.
5. Refresh semantics: unsaved edits disappear after refresh; only saved notes remain.
6. Inline edit: each note supports inline edit with Save/Cancel.
7. Delete note: each note supports delete action.
8. Marker-to-content sync: canvas and content must share one scale system (recommended fixed aspect-ratio canvas) so marker position stays stable during horizontal and vertical resize.
9. Keep `Add Note`, `Clear Notes`, and `Save HTML` on the same top action row.
10. Do not use prompt/modal for adding note text; enter text directly in inline edit row.
11. Support multiline note content with textarea editing and wrapped display (`white-space: pre-wrap`).
12. When page/tab/note lists are long, `Pages` and `Annotations` areas must scroll independently while the whole page remains fixed.
13. Apply file safety workflow on every change: backup to `_backups` before edit, run encoding check after edit, and rollback to latest backup if mojibake appears.
14. If final delivery is requested, prefer single-file output (`prototype.html`) unless user explicitly asks for multi-file structure.
15. In inline JS, avoid raw `</script>` literals; use escaped `<\\/script>` when generating HTML strings.
16. Keep inline edit stable: no immediate collapse after one click; only `Save`/`Cancel`/`Delete` should close edit mode.
17. Top action row labels must be fully visible in default desktop layout; do not truncate `Save HTML`.
18. Center canvas content area is the full prototype viewport and must not show horizontal or vertical scrollbars.
19. If prototype content is visually clipped, expand center work area first (increase center column space and/or reduce side columns within usable limits) instead of changing restored page geometry.
20. In Figma restore mode, visual art resources must use Figma assets (MCP URLs or exported files) only; do not create substitute icons/illustrations/photos manually.
21. Save defaults must use the currently opened source HTML filename and should not hardcode `prototype.html`.
22. Save path behavior should prefer the source file directory by reusing `FileSystemFileHandle`; configure a stable `showSaveFilePicker` `id` so the browser can persist last-used directory.

## Source-of-truth contract

Do not use localStorage as source of truth.

Use page-embedded JSON block in each HTML file:

```html
<!-- ANNOTATIONS_DATA_START -->
<script id="page-annotations" type="application/json">[]</script>
<!-- ANNOTATIONS_DATA_END -->
```

On load, read notes from `#page-annotations`.

## Save strategy contract

1. Preferred: use File System Access API (`showSaveFilePicker` + `createWritable`) to write updated HTML.
2. Fallback: if write API is unavailable, export updated HTML as a downloadable file.
3. Save operation updates only the annotations data block; page structure remains unchanged.
4. `suggestedName` should derive from the current file path (`location.pathname`), with safe decoding fallback.
5. Use a stable picker `id` and cached file handle to keep subsequent saves on the same file/path by default.

## Scaffold output contract

`scaffold_prototype.py` should generate:

1. `styles.css` with three-panel layout and annotation styles.
2. `annotations.js` with note behaviors and file-save logic.
3. Page html files containing tabs, annotation panel, and embedded annotations data block.
4. Optional single-file mode: `prototype.html` with inlined CSS/JS and embedded annotations map.
5. In single-file delivery, clean non-required generated files from output root (archive them under `_backups` if needed).

## Extension guidance

1. Keep ids stable (`canvas-root`, `annotation-layer`, `annotation-list`, `add-note-btn`, `clear-note-btn`, `save-note-btn`).
2. Keep per-page key injection via global variables in each page.
3. Extend note schema by adding optional fields instead of breaking existing fields.
