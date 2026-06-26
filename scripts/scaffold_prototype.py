#!/usr/bin/env python3
"""Generate a pure HTML multi-page prototype scaffold with full-page tabs and file-based annotations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BASE_CSS = """* { box-sizing: border-box; }
html, body { min-height: 100dvh; }
body { margin: 0; min-height: 100dvh; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f3f6fb; color: #1f2937; overflow: hidden; display: flex; flex-direction: column; }
.header { height: 56px; display: flex; align-items: center; padding: 0 18px; background: #ffffff; border-bottom: 1px solid #e5e7eb; font-weight: 700; }
.main { flex: 1; min-height: 0; width: 100%; max-width: 1680px; margin: 0 auto; padding: 12px; display: flex; flex-direction: column; }
.layout { flex: 1; min-height: 0; display: grid; grid-template-columns: 220px minmax(0, 1fr) 360px; gap: 12px; }
.panel { background: #ffffff; border-right: 1px solid #e5e7eb; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }
.panel:last-child { border-right: 1px solid #e5e7eb; }
.panel-title { margin: 0; padding: 12px 14px; border-bottom: 1px solid #eef2f7; font-size: 14px; }
.tabs { padding: 10px; display: flex; flex-direction: column; gap: 8px; overflow: auto; }
.tab { display: block; text-decoration: none; color: #111827; border: 1px solid #e5e7eb; border-radius: 10px; padding: 9px 10px; background: #fff; }
.tab.active { background: #eff6ff; border-color: #93c5fd; color: #1d4ed8; font-weight: 600; }
.canvas-wrap { flex: 1; min-height: 0; padding: 12px; display: flex; align-items: flex-start; justify-content: center; }
.canvas { position: relative; width: 100%; aspect-ratio: 16 / 9; border: 1px solid #dbe2f0; border-radius: 12px; background: #fff; overflow: hidden; }
.screen { position: absolute; inset: 0; padding: 18px; overflow: hidden; }
.screen-page { display: none; }
.screen-page.active { display: block; }
.card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin-bottom: 14px; }
.btn { display: inline-block; border: 0; border-radius: 10px; padding: 10px 14px; background: #2563eb; color: #fff; text-decoration: none; cursor: pointer; }
.btn.secondary { background: #e5e7eb; color: #111827; }
.btn.link { background: #f8fafc; color: #0f172a; border: 1px solid #e2e8f0; }
.note { color: #6b7280; font-size: 14px; }
.annotation-layer { position: absolute; inset: 0; pointer-events: none; }
.annotation-dot { width: 24px; height: 24px; border-radius: 999px; border: 1px solid #ef4444; background: #fee2e2; color: #dc2626; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; position: absolute; transform: translate(-50%, -50%); cursor: grab; pointer-events: auto; user-select: none; touch-action: none; }
.annotation-dot.active { background: #ef4444; color: #fff; border-color: #ef4444; }
.annotation-body { flex: 1; min-height: 0; padding: 10px; display: flex; flex-direction: column; gap: 8px; }
.annotation-list { display: flex; flex-direction: column; gap: 8px; overflow: auto; min-height: 0; }
.annotation-item { border: 1px solid #e5e7eb; border-radius: 10px; padding: 8px; font-size: 13px; }
.annotation-item.active { border-color: #fca5a5; background: #fef2f2; }
.annotation-index { font-weight: 700; color: #b91c1c; margin-right: 6px; }
.annotation-text { display: block; margin-top: 6px; white-space: pre-wrap; word-break: break-word; }
.annotation-edit-input { width: 100%; margin-top: 8px; border: 1px solid #d1d5db; border-radius: 8px; padding: 6px 8px; font-size: 13px; resize: vertical; min-height: 68px; font-family: inherit; }
.annotation-actions { margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap; }
.mini-btn { border: 1px solid #d1d5db; background: #fff; border-radius: 8px; padding: 4px 8px; font-size: 12px; cursor: pointer; }
.mini-btn.primary { background: #2563eb; color: #fff; border-color: #2563eb; }
.mini-btn.danger { color: #b91c1c; border-color: #fecaca; background: #fff5f5; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
.top-actions { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; align-items: center; }
.top-actions > .btn { min-width: 0; white-space: normal; line-height: 1.2; text-align: center; padding: 8px 10px; }
.sub-actions { display: flex; justify-content: flex-start; align-items: center; gap: 8px; flex-wrap: wrap; }
.save-status { font-size: 12px; color: #475569; }
@media (max-width: 1100px) { .layout { grid-template-columns: 200px 1fr; } .panel.annotation-panel { grid-column: 1 / -1; min-height: 360px; border-top: 1px solid #e5e7eb; } }
@media (max-width: 860px) { .layout { grid-template-columns: 1fr; } .panel { border-right: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb; } .tabs { display: grid; grid-template-columns: 1fr 1fr; } .panel.annotation-panel { min-height: 380px; } }
"""

PAGE_TEMPLATE = """<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <header class=\"header\">{title}</header>
  <main class=\"main\">
    <div class=\"layout\">
      <aside class=\"panel\">
        <h2 class=\"panel-title\">Pages</h2>
        <nav class=\"tabs\">
          {tab_links}
        </nav>
      </aside>

      <section class=\"panel\">
        <h2 class=\"panel-title\">Canvas</h2>
        <div class=\"canvas-wrap\">
          <div class=\"canvas\" id=\"canvas-root\">
            <!-- PROTOTYPE_CANVAS_CONTENT_START -->
            <div class=\"screen\" id=\"prototype-content-root\"></div>
            <!-- PROTOTYPE_CANVAS_CONTENT_END -->
            <div class=\"annotation-layer\" id=\"annotation-layer\"></div>
          </div>
        </div>
      </section>

      <aside class=\"panel annotation-panel\">
        <h2 class=\"panel-title\">Annotations</h2>
        <div class=\"annotation-body\">
          <div class=\"top-actions\">
            <button class=\"btn\" type=\"button\" id=\"add-note-btn\">Add Note</button>
            <button class=\"btn link\" type=\"button\" id=\"clear-note-btn\">Clear Notes</button>
            <button class=\"btn\" type=\"button\" id=\"save-note-btn\">Save HTML</button>
          </div>
          <div class=\"sub-actions\"><span class=\"save-status\" id=\"save-status\">Unsaved changes</span></div>
          <div class=\"annotation-list\" id=\"annotation-list\"></div>
        </div>
      </aside>
    </div>
  </main>

  <!-- ANNOTATIONS_DATA_START -->
  <script id=\"page-annotations\" type=\"application/json\">{annotations_json}</script>
  <!-- ANNOTATIONS_DATA_END -->

  <script>
    window.PROTOTYPE_PAGE_KEY = \"{page_key}\";
    window.PROTOTYPE_PAGE_NAME = \"{page_name}\";
  </script>
  <script src=\"annotations.js\"></script>
</body>
</html>
"""

ANNOTATIONS_JS = """(function () {
  const pageKey = window.PROTOTYPE_PAGE_KEY || "default-page";
  const pageName = window.PROTOTYPE_PAGE_NAME || pageKey;
  const canvas = document.getElementById("canvas-root");
  const layer = document.getElementById("annotation-layer");
  const list = document.getElementById("annotation-list");
  const addBtn = document.getElementById("add-note-btn");
  const clearBtn = document.getElementById("clear-note-btn");
  const saveBtn = document.getElementById("save-note-btn");
  const saveStatus = document.getElementById("save-status");
  const dataNode = document.getElementById("page-annotations");
  if (!canvas || !layer || !list || !addBtn || !clearBtn || !saveBtn || !saveStatus || !dataNode) return;

  let fileHandle = null;
  let dirty = false;
  let pendingEditIndex = null;
  const initialRaw = dataNode.textContent || "[]";
  let notes = parseNotes(initialRaw);

  function parseNotes(raw) {
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }

  function setDirty(flag) {
    dirty = flag;
    if (dirty) {
      saveStatus.textContent = "Unsaved changes";
      saveStatus.style.color = "#b45309";
    } else {
      saveStatus.textContent = "Saved to HTML";
      saveStatus.style.color = "#047857";
    }
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function getAnnotationsJson() {
    return JSON.stringify(notes, null, 2);
  }

  function buildUpdatedHtml() {
    const html = "<!doctype html>\\n" + document.documentElement.outerHTML;
    const block = '<!-- ANNOTATIONS_DATA_START -->\\n  <script id=\"page-annotations\" type=\"application/json\">' + getAnnotationsJson() + '</script>\\n  <!-- ANNOTATIONS_DATA_END -->';
    return html.replace(/<!-- ANNOTATIONS_DATA_START -->[\\s\\S]*?<!-- ANNOTATIONS_DATA_END -->/, block);
  }

  function downloadUpdatedHtml() {
    const blob = new Blob([buildUpdatedHtml()], { type: "text/html;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    const currentName = location.pathname.split("/").pop() || (pageKey + ".html");
    a.download = currentName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  }

  async function ensureFileHandle() {
    if (fileHandle) return fileHandle;
    if (!window.showSaveFilePicker) return null;
    const currentName = location.pathname.split("/").pop() || (pageKey + ".html");
    fileHandle = await window.showSaveFilePicker({
      suggestedName: currentName,
      types: [{ description: "HTML", accept: { "text/html": [".html"] } }]
    });
    return fileHandle;
  }

  async function saveToFile() {
    try {
      const handle = await ensureFileHandle();
      if (!handle) {
        downloadUpdatedHtml();
        setDirty(false);
        return;
      }
      const writable = await handle.createWritable();
      await writable.write(buildUpdatedHtml());
      await writable.close();
      setDirty(false);
    } catch (err) {
      console.warn("Save failed:", err);
      saveStatus.textContent = "Save failed, retry";
      saveStatus.style.color = "#b91c1c";
    }
  }

  function render() {
    layer.innerHTML = "";
    list.innerHTML = "";
    if (!notes.length) {
      const empty = document.createElement("div");
      empty.className = "annotation-item";
      empty.textContent = "No notes on " + pageName + ".";
      list.appendChild(empty);
      return;
    }

    notes.forEach((note, idx) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "annotation-dot";
      dot.style.left = note.x + "%";
      dot.style.top = note.y + "%";
      dot.textContent = String(idx + 1);
      dot.title = note.text;
      layer.appendChild(dot);

      const row = document.createElement("div");
      row.className = "annotation-item";
      row.innerHTML =
        "<span class=\\"annotation-index\\">#" + (idx + 1) + "</span>" +
        "<span class=\\"annotation-text\\"></span>" +
        "<textarea class=\\"annotation-edit-input\\" style=\\"display:none;\\"></textarea>" +
        "<div class=\\"annotation-actions\\">" +
        "<button type=\\"button\\" class=\\"mini-btn\\" data-role=\\"edit\\">Edit</button>" +
        "<button type=\\"button\\" class=\\"mini-btn primary\\" data-role=\\"save\\" style=\\"display:none;\\">Save</button>" +
        "<button type=\\"button\\" class=\\"mini-btn\\" data-role=\\"cancel\\" style=\\"display:none;\\">Cancel</button>" +
        "<button type=\\"button\\" class=\\"mini-btn danger\\" data-role=\\"delete\\">Delete</button>" +
        "</div>";
      const textNode = row.querySelector(".annotation-text");
      const inputNode = row.querySelector(".annotation-edit-input");
      const editBtn = row.querySelector('[data-role="edit"]');
      const saveInlineBtn = row.querySelector('[data-role="save"]');
      const cancelBtn = row.querySelector('[data-role="cancel"]');
      const deleteBtn = row.querySelector('[data-role="delete"]');
      textNode.textContent = note.text;
      list.appendChild(row);

      dot.addEventListener("click", function () {
        document.querySelectorAll(".annotation-dot.active").forEach((n) => n.classList.remove("active"));
        document.querySelectorAll(".annotation-item.active").forEach((n) => n.classList.remove("active"));
        dot.classList.add("active");
        row.classList.add("active");
      });

      function enterEdit() {
        inputNode.value = note.text;
        textNode.style.display = "none";
        inputNode.style.display = "block";
        editBtn.style.display = "none";
        saveInlineBtn.style.display = "inline-block";
        cancelBtn.style.display = "inline-block";
        inputNode.focus();
        inputNode.select();
      }

      function exitEdit() {
        textNode.style.display = "block";
        inputNode.style.display = "none";
        editBtn.style.display = "inline-block";
        saveInlineBtn.style.display = "none";
        cancelBtn.style.display = "none";
      }

      editBtn.addEventListener("click", function () {
        enterEdit();
      });

      saveInlineBtn.addEventListener("click", function () {
        const rawText = String(inputNode.value || "").replace(/\\r\\n/g, "\\n");
        if (!rawText.trim()) return;
        const nextText = rawText;
        notes[idx].text = nextText;
        setDirty(true);
        render();
      });

      cancelBtn.addEventListener("click", function () {
        exitEdit();
      });

      inputNode.addEventListener("keydown", function (evt) {
        if (evt.key === "Enter" && evt.ctrlKey) {
          evt.preventDefault();
          saveInlineBtn.click();
        }
        if (evt.key === "Escape") {
          evt.preventDefault();
          cancelBtn.click();
        }
      });

      deleteBtn.addEventListener("click", function () {
        notes.splice(idx, 1);
        setDirty(true);
        render();
      });

      let dragging = false;
      dot.addEventListener("pointerdown", function (evt) {
        dragging = true;
        dot.setPointerCapture(evt.pointerId);
      });
      dot.addEventListener("pointermove", function (evt) {
        if (!dragging) return;
        const rect = canvas.getBoundingClientRect();
        const x = clamp(((evt.clientX - rect.left) / rect.width) * 100, 0, 100);
        const y = clamp(((evt.clientY - rect.top) / rect.height) * 100, 0, 100);
        dot.style.left = x + "%";
        dot.style.top = y + "%";
        notes[idx].x = Number(x.toFixed(2));
        notes[idx].y = Number(y.toFixed(2));
        setDirty(true);
      });
      dot.addEventListener("pointerup", function (evt) {
        dragging = false;
        dot.releasePointerCapture(evt.pointerId);
      });

      if (pendingEditIndex === idx) {
        pendingEditIndex = null;
        enterEdit();
      }
    });
  }

  function addNoteInline() {
    pendingEditIndex = notes.length;
    notes.push({ text: "", x: 50, y: 50 });
    setDirty(true);
    render();
  }

  addBtn.addEventListener("click", function () {
    addNoteInline();
  });

  clearBtn.addEventListener("click", function () {
    if (!window.confirm("Clear all notes on current page?")) return;
    notes = [];
    setDirty(true);
    render();
  });

  saveBtn.addEventListener("click", function () {
    saveToFile();
  });

  window.addEventListener("beforeunload", function (evt) {
    if (!dirty) return;
    evt.preventDefault();
    evt.returnValue = "";
  });

  setDirty(false);
  render();
})();
"""

SINGLE_FILE_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
{inline_css}
  </style>
</head>
<body>
  <header class="header">{title}</header>
  <main class="main">
    <div class="layout">
      <aside class="panel">
        <h2 class="panel-title">Pages</h2>
        <nav class="tabs">
{tab_buttons}
        </nav>
      </aside>

      <section class="panel">
        <h2 class="panel-title">Canvas</h2>
        <div class="canvas-wrap">
          <div class="canvas" id="canvas-root">
            <div class="screen">
{page_sections}
            </div>
            <div class="annotation-layer" id="annotation-layer"></div>
          </div>
        </div>
      </section>

      <aside class="panel annotation-panel">
        <h2 class="panel-title">Annotations</h2>
        <div class="annotation-body">
          <div class="top-actions">
            <button class="btn" type="button" id="add-note-btn">Add Note</button>
            <button class="btn link" type="button" id="clear-note-btn">Clear Notes</button>
            <button class="btn" type="button" id="save-note-btn">Save HTML</button>
          </div>
          <div class="sub-actions"><span class="save-status" id="save-status">Unsaved changes</span></div>
          <div class="annotation-list" id="annotation-list"></div>
        </div>
      </aside>
    </div>
  </main>

  <!-- ANNOTATIONS_DATA_START -->
  <script id="page-annotations-map" type="application/json">{annotations_map_json}</script>
  <!-- ANNOTATIONS_DATA_END -->

  <script>
    window.PROTOTYPE_PAGES = {pages_json};
{inline_js}
  </script>
</body>
</html>
"""

SINGLE_FILE_JS = """(function () {
  const pages = Array.isArray(window.PROTOTYPE_PAGES) ? window.PROTOTYPE_PAGES : [];
  if (!pages.length) return;
  let currentPage = pages[0].key;

  const canvas = document.getElementById("canvas-root");
  const layer = document.getElementById("annotation-layer");
  const list = document.getElementById("annotation-list");
  const addBtn = document.getElementById("add-note-btn");
  const clearBtn = document.getElementById("clear-note-btn");
  const saveBtn = document.getElementById("save-note-btn");
  const saveStatus = document.getElementById("save-status");
  const dataNode = document.getElementById("page-annotations-map");
  if (!canvas || !layer || !list || !addBtn || !clearBtn || !saveBtn || !saveStatus || !dataNode) return;

  let fileHandle = null;
  let dirty = false;
  let pendingEditIndex = null;
  let notesMap = parseMap(dataNode.textContent || "{}");

  function parseMap(raw) {
    try {
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch {
      return {};
    }
  }
  function getNotes() {
    return Array.isArray(notesMap[currentPage]) ? notesMap[currentPage] : [];
  }
  function setNotes(notes) {
    notesMap[currentPage] = notes;
  }
  function setDirty(flag) {
    dirty = flag;
    if (dirty) { saveStatus.textContent = "Unsaved changes"; saveStatus.style.color = "#b45309"; }
    else { saveStatus.textContent = "Saved to HTML"; saveStatus.style.color = "#047857"; }
  }
  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }
  function buildUpdatedHtml() {
    const html = "<!doctype html>\\n" + document.documentElement.outerHTML;
    const block = '<!-- ANNOTATIONS_DATA_START -->\\n  <script id="page-annotations-map" type="application/json">' + JSON.stringify(notesMap, null, 2) + '<\\/script>\\n  <!-- ANNOTATIONS_DATA_END -->';
    return html.replace(/<!-- ANNOTATIONS_DATA_START -->[\\s\\S]*?<!-- ANNOTATIONS_DATA_END -->/, block);
  }
  function downloadUpdatedHtml() {
    const blob = new Blob([buildUpdatedHtml()], { type: "text/html;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "prototype.html";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  }
  async function ensureFileHandle() {
    if (fileHandle) return fileHandle;
    if (!window.showSaveFilePicker) return null;
    fileHandle = await window.showSaveFilePicker({
      suggestedName: "prototype.html",
      types: [{ description: "HTML", accept: { "text/html": [".html"] } }]
    });
    return fileHandle;
  }
  async function saveToFile() {
    try {
      const handle = await ensureFileHandle();
      if (!handle) { downloadUpdatedHtml(); setDirty(false); return; }
      const writable = await handle.createWritable();
      await writable.write(buildUpdatedHtml());
      await writable.close();
      setDirty(false);
    } catch (err) {
      console.warn("Save failed:", err);
      saveStatus.textContent = "Save failed, retry";
      saveStatus.style.color = "#b91c1c";
    }
  }
  function renderTabs() {
    document.querySelectorAll("[data-page-key]").forEach((node) => {
      node.classList.toggle("active", node.getAttribute("data-page-key") === currentPage);
    });
    document.querySelectorAll(".screen-page").forEach((node) => {
      node.classList.toggle("active", node.getAttribute("data-page-key") === currentPage);
    });
  }
  function renderNotes() {
    const notes = getNotes();
    layer.innerHTML = "";
    list.innerHTML = "";
    if (!notes.length) {
      const empty = document.createElement("div");
      empty.className = "annotation-item";
      empty.textContent = "No notes on " + currentPage + ".";
      list.appendChild(empty);
      return;
    }
    notes.forEach((note, idx) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "annotation-dot";
      dot.style.left = note.x + "%";
      dot.style.top = note.y + "%";
      dot.textContent = String(idx + 1);
      dot.title = note.text;
      layer.appendChild(dot);

      const row = document.createElement("div");
      row.className = "annotation-item";
      row.innerHTML =
        "<span class=\\"annotation-index\\">#" + (idx + 1) + "</span>" +
        "<span class=\\"annotation-text\\"></span>" +
        "<textarea class=\\"annotation-edit-input\\" style=\\"display:none;\\"></textarea>" +
        "<div class=\\"annotation-actions\\">" +
        "<button type=\\"button\\" class=\\"mini-btn\\" data-role=\\"edit\\">Edit</button>" +
        "<button type=\\"button\\" class=\\"mini-btn primary\\" data-role=\\"save\\" style=\\"display:none;\\">Save</button>" +
        "<button type=\\"button\\" class=\\"mini-btn\\" data-role=\\"cancel\\" style=\\"display:none;\\">Cancel</button>" +
        "<button type=\\"button\\" class=\\"mini-btn danger\\" data-role=\\"delete\\">Delete</button>" +
        "</div>";
      const textNode = row.querySelector(".annotation-text");
      const inputNode = row.querySelector(".annotation-edit-input");
      const editBtn = row.querySelector('[data-role="edit"]');
      const saveInlineBtn = row.querySelector('[data-role="save"]');
      const cancelBtn = row.querySelector('[data-role="cancel"]');
      const deleteBtn = row.querySelector('[data-role="delete"]');
      textNode.textContent = note.text;
      list.appendChild(row);

      function enterEdit() {
        inputNode.value = note.text;
        textNode.style.display = "none";
        inputNode.style.display = "block";
        editBtn.style.display = "none";
        saveInlineBtn.style.display = "inline-block";
        cancelBtn.style.display = "inline-block";
        inputNode.focus();
      }
      function exitEdit() {
        textNode.style.display = "block";
        inputNode.style.display = "none";
        editBtn.style.display = "inline-block";
        saveInlineBtn.style.display = "none";
        cancelBtn.style.display = "none";
      }
      editBtn.addEventListener("click", enterEdit);
      saveInlineBtn.addEventListener("click", function () {
        const rawText = String(inputNode.value || "").replace(/\\r\\n/g, "\\n");
        if (!rawText.trim()) return;
        notes[idx].text = rawText;
        setNotes(notes);
        setDirty(true);
        renderNotes();
      });
      cancelBtn.addEventListener("click", exitEdit);
      deleteBtn.addEventListener("click", function () {
        notes.splice(idx, 1);
        setNotes(notes);
        setDirty(true);
        renderNotes();
      });
      inputNode.addEventListener("keydown", function (evt) {
        if (evt.key === "Enter" && evt.ctrlKey) { evt.preventDefault(); saveInlineBtn.click(); }
        if (evt.key === "Escape") { evt.preventDefault(); cancelBtn.click(); }
      });
      let dragging = false;
      dot.addEventListener("pointerdown", function (evt) { dragging = true; dot.setPointerCapture(evt.pointerId); });
      dot.addEventListener("pointermove", function (evt) {
        if (!dragging) return;
        const rect = canvas.getBoundingClientRect();
        notes[idx].x = Number(clamp(((evt.clientX - rect.left) / rect.width) * 100, 0, 100).toFixed(2));
        notes[idx].y = Number(clamp(((evt.clientY - rect.top) / rect.height) * 100, 0, 100).toFixed(2));
        dot.style.left = notes[idx].x + "%";
        dot.style.top = notes[idx].y + "%";
        setNotes(notes);
        setDirty(true);
      });
      dot.addEventListener("pointerup", function (evt) { dragging = false; dot.releasePointerCapture(evt.pointerId); });
      if (pendingEditIndex === idx) { pendingEditIndex = null; enterEdit(); }
    });
  }

  document.querySelectorAll("[data-page-key]").forEach((btn) => {
    btn.addEventListener("click", function () {
      currentPage = btn.getAttribute("data-page-key");
      pendingEditIndex = null;
      renderTabs();
      renderNotes();
    });
  });
  addBtn.addEventListener("click", function () {
    const notes = getNotes();
    pendingEditIndex = notes.length;
    notes.push({ text: "", x: 50, y: 50 });
    setNotes(notes);
    setDirty(true);
    renderNotes();
  });
  clearBtn.addEventListener("click", function () {
    if (!window.confirm("Clear all notes on current page?")) return;
    setNotes([]);
    setDirty(true);
    renderNotes();
  });
  saveBtn.addEventListener("click", saveToFile);
  window.addEventListener("beforeunload", function (evt) { if (!dirty) return; evt.preventDefault(); evt.returnValue = ""; });

  setDirty(false);
  renderTabs();
  renderNotes();
})();"""


def to_filename(name: str) -> str:
  cleaned = ''.join(ch.lower() if ch.isalnum() else '-' for ch in name).strip('-')
  while '--' in cleaned:
    cleaned = cleaned.replace('--', '-')
  return cleaned or 'page'


def create_project(output_dir: Path, pages: list[str], title: str) -> None:
  output_dir.mkdir(parents=True, exist_ok=True)
  (output_dir / 'styles.css').write_text(BASE_CSS, encoding='utf-8')
  (output_dir / 'annotations.js').write_text(ANNOTATIONS_JS, encoding='utf-8')

  page_files = [f"{to_filename(page)}.html" for page in pages]
  for index, page in enumerate(pages):
    links = []
    for i, page_name in enumerate(pages):
      file_name = page_files[i]
      if i == index:
        links.append(f'<a class="tab active" href="{file_name}">{page_name}</a>')
      else:
        links.append(f'<a class="tab" href="{file_name}">{page_name}</a>')
    html = PAGE_TEMPLATE.format(
      title=f"{title} - {page}",
      tab_links='\n          '.join(links),
      page_name=page,
      page_key=to_filename(page),
      annotations_json=json.dumps([], ensure_ascii=False, indent=2),
    )
    (output_dir / page_files[index]).write_text(html, encoding='utf-8')


def create_single_file_project(output_dir: Path, pages: list[str], title: str) -> None:
  output_dir.mkdir(parents=True, exist_ok=True)
  page_defs = [{"name": p, "key": to_filename(p)} for p in pages]
  tab_buttons = '\n'.join(
    f'          <button type="button" class="tab{" active" if i == 0 else ""}" data-page-key="{p["key"]}">{p["name"]}</button>'
    for i, p in enumerate(page_defs)
  )
  page_sections = '\n'.join(
    f'''              <section class="screen-page{" active" if i == 0 else ""}" data-page-key="{p["key"]}">
                <!-- PROTOTYPE_CANVAS_CONTENT_START -->
                <div id="prototype-content-root-{p["key"]}"></div>
                <!-- PROTOTYPE_CANVAS_CONTENT_END -->
              </section>'''
    for i, p in enumerate(page_defs)
  )
  notes_map = {p["key"]: [] for p in page_defs}
  html = SINGLE_FILE_TEMPLATE.format(
    title=title,
    inline_css=BASE_CSS,
    tab_buttons=tab_buttons,
    page_sections=page_sections,
    pages_json=json.dumps(page_defs, ensure_ascii=False),
    annotations_map_json=json.dumps(notes_map, ensure_ascii=False, indent=2),
    inline_js=SINGLE_FILE_JS,
  )
  (output_dir / 'prototype.html').write_text(html, encoding='utf-8')


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description='Generate a pure HTML multi-page prototype scaffold.')
  parser.add_argument('--title', required=True, help='Project title')
  parser.add_argument('--pages', required=True, nargs='+', help='Page names')
  parser.add_argument('--out', default='prototype-output', help='Output directory')
  parser.add_argument('--single-file', action='store_true', help='Generate a single self-contained HTML file.')
  return parser.parse_args()


def main() -> None:
  args = parse_args()
  if args.single_file:
    create_single_file_project(Path(args.out), args.pages, args.title)
  else:
    create_project(Path(args.out), args.pages, args.title)
  print(f'Generated prototype scaffold at: {Path(args.out).resolve()}')


if __name__ == '__main__':
  main()
