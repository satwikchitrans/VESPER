/* ═══════════════════════════════════════════════════════════════════
   VESPER DEDICATED VISUAL STUDIO & PLATFORM EDITOR v3
   
   1. Live Visual Color System: Real-time native color pickers + curated Gov/Tactical palettes for text, background, border.
   2. Unhide & Visibility Manager: Instant "Unhide All Buttons & Elements" + single-click visibility toggle.
   3. Floating Quick Toolbar: Color, font-size, margin, duplicate, and delete right on the selected element.
   4. Full Platform Navigation: Freely click and switch across all 6 window tabs.
   5. Direct Drag & Reposition: Click & hold any element/card to reposition without keys.
   6. Edge & Margin Resize: Grab borders or 8 handles to resize width, height, margins.
   7. Space Preservation: Removing an element preserves layout space with a placeholder slot.
   8. In-Place Text Editing: Double-click any text to edit directly.
   9. Real-Time Disk Persistence: Saves clean HTML directly to index.html on disk.
   ═══════════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  let selectedElement = null;
  let isDragging = false;
  let isResizing = false;
  let resizeDir = null;
  let dragTarget = null;
  let dragStartPos = { mouseX: 0, mouseY: 0, elX: 0, elY: 0, width: 0, height: 0 };
  let hasMovedDuringDrag = false;
  let isMouseDown = false;
  let pendingTarget = null;
  let autoSaveTimeout = null;
  let undoStack = [];
  let redoStack = [];
  const MAX_UNDO = 30;

  // Curated Tactical & Government Color Palette Swatches
  const PALETTE_COLORS = [
    { name: 'Saffron Orange', hex: '#fb792b' },
    { name: 'Cyan Blue', hex: '#00f0ff' },
    { name: 'Govt Navy', hex: '#213d77' },
    { name: 'Terminal Green', hex: '#10b981' },
    { name: 'Pure White', hex: '#ffffff' },
    { name: 'Amber Gold', hex: '#f59e0b' },
    { name: 'Alert Red', hex: '#ef4444' },
    { name: 'Tactical Purple', hex: '#8b5cf6' },
    { name: 'Dark Slate', hex: '#0f172a' },
    { name: 'Deep Midnight', hex: '#090d16' }
  ];

  // Selectors for interactive controls that should not trigger dragging
  const INTERACTIVE_SELECTOR = [
    'button', 'a', 'input', 'select', 'textarea', 'label',
    '.nav-tab', '.layout-btn', '.hero-cta', '.wfh-btn', '.iub-btn',
    '.top-bar-action', '.stat-pill', '.global-plate-btn', '.global-plate-input',
    '.api-status-action', '.studio-btn-link',
    '.slot-btn', '.assc-btn', '#vesper-editor-topbar', '#vesper-floating-toolbar',
    '[onclick]', '[data-window]', '[data-layout]',
    '.leaflet-control', '.leaflet-container'
  ].join(', ');

  // Selectors for draggable modules & cards
  const DRAGGABLE_SELECTOR = [
    '.hero-stat-card', '.vesper-custom-card', '.vesper-custom-stat-card', '.vesper-preserved-slot',
    '.home-hero', '.card', '.modal-box', '.pane',
    '.info-card', '.stat-card', '.command-card', '.dashboard-card',
    '.sc-target-banner', '.sc-corridor-card', '.lcm-feed-card', '.hero-api-banner'
  ].join(', ');

  // ── 1. INJECT EDITOR STYLES ──
  const styleEl = document.createElement('style');
  styleEl.id = 'vesper-editor-injected-styles';
  styleEl.textContent = `
    /* Studio Topbar */
    #vesper-editor-topbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 52px;
      background: #090d16;
      border-bottom: 1.5px solid rgba(251, 121, 43, 0.4);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 100000;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8), 0 0 15px rgba(251, 121, 43, 0.15);
      font-family: 'Inter', system-ui, sans-serif;
      user-select: none;
    }
    
    body {
      padding-top: 52px !important;
    }

    .vet-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .vet-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(251, 121, 43, 0.15);
      border: 1px solid rgba(251, 121, 43, 0.4);
      padding: 4px 10px;
      border-radius: 4px;
      color: #fb792b;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
    }
    .vet-pulse {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: vet-pulse-anim 1.5s infinite alternate;
    }
    @keyframes vet-pulse-anim {
      from { opacity: 0.5; transform: scale(0.85); }
      to { opacity: 1; transform: scale(1.2); }
    }

    .vet-status-pill {
      font-size: 11px;
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
    }
    .vet-status-pill.saved { color: #00f0ff; }
    .vet-status-pill.saving { color: #fb792b; }

    .vet-center {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .vet-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #cbd5e1;
      border-radius: 4px;
      padding: 5px 10px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: 'Inter', system-ui, sans-serif;
    }
    .vet-btn:hover {
      background: rgba(255, 255, 255, 0.14);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.3);
    }
    .vet-btn.primary {
      background: linear-gradient(135deg, #fb792b, #e05a10);
      color: #ffffff;
      border: 1px solid #fb792b;
      box-shadow: 0 0 10px rgba(251, 121, 43, 0.4);
    }
    .vet-btn.primary:hover {
      background: linear-gradient(135deg, #fc8942, #fb792b);
      box-shadow: 0 0 15px rgba(251, 121, 43, 0.6);
    }
    .vet-btn.cyan {
      background: rgba(0, 240, 255, 0.12);
      color: #00f0ff;
      border-color: rgba(0, 240, 255, 0.3);
    }
    .vet-btn.cyan:hover {
      background: #00f0ff;
      color: #0b111e;
    }
    .vet-btn.unhide {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
      color: #10b981;
    }
    .vet-btn.unhide:hover {
      background: #10b981;
      color: #0b111e;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }

    .vet-color-swatch-group {
      display: flex;
      align-items: center;
      gap: 3px;
      padding: 2px 6px;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .vet-color-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      cursor: pointer;
      border: 1px solid rgba(255, 255, 255, 0.3);
      transition: transform 0.15s;
    }
    .vet-color-dot:hover {
      transform: scale(1.3);
      border-color: #ffffff;
    }

    .vet-picker-wrap {
      position: relative;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .vet-color-input {
      width: 22px;
      height: 22px;
      padding: 0;
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 4px;
      cursor: pointer;
      background: none;
    }

    .vet-divider {
      width: 1px;
      height: 22px;
      background: rgba(255, 255, 255, 0.12);
      margin: 0 4px;
    }

    .vet-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .vet-live-link {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #10b981;
      padding: 5px 12px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .vet-live-link:hover {
      background: #10b981;
      color: #0b111e;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
    }

    /* Floating Quick Formatting Toolbar (above selection) */
    #vesper-floating-toolbar {
      position: absolute;
      background: #0b111e;
      border: 1px solid rgba(0, 240, 255, 0.4);
      border-radius: 6px;
      padding: 4px 8px;
      display: none;
      align-items: center;
      gap: 6px;
      z-index: 99995;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8), 0 0 12px rgba(0, 240, 255, 0.2);
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 11px;
    }
    #vesper-floating-toolbar.active {
      display: flex;
    }
    .vft-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #e2e8f0;
      border-radius: 3px;
      padding: 3px 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
    }
    .vft-btn:hover {
      background: #fb792b;
      color: #ffffff;
      border-color: #fb792b;
    }

    /* Selection Overlay & Handles */
    #vesper-selection-overlay {
      position: absolute;
      pointer-events: none;
      border: 1.5px solid #00f0ff;
      border-radius: 6px;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.4), inset 0 0 8px rgba(0, 240, 255, 0.1);
      z-index: 99990;
      display: none;
    }
    #vesper-selection-overlay.active {
      display: block;
    }
    #vesper-selection-overlay .handle {
      position: absolute;
      width: 10px;
      height: 10px;
      background: #0b111e;
      border: 2px solid #00f0ff;
      border-radius: 3px;
      pointer-events: auto;
      box-shadow: 0 0 6px rgba(0, 240, 255, 0.8);
      z-index: 99992;
      transition: transform 0.1s, background-color 0.1s;
    }
    #vesper-selection-overlay .handle:hover {
      background: #fb792b;
      border-color: #ffffff;
      transform: scale(1.3);
    }
    #vesper-selection-overlay .handle-nw { top: -6px; left: -6px; cursor: nwse-resize; }
    #vesper-selection-overlay .handle-ne { top: -6px; right: -6px; cursor: nesw-resize; }
    #vesper-selection-overlay .handle-sw { bottom: -6px; left: -6px; cursor: nesw-resize; }
    #vesper-selection-overlay .handle-se { bottom: -6px; right: -6px; cursor: nwse-resize; }
    #vesper-selection-overlay .handle-n  { top: -6px; left: calc(50% - 5px); cursor: ns-resize; }
    #vesper-selection-overlay .handle-s  { bottom: -6px; left: calc(50% - 5px); cursor: ns-resize; }
    #vesper-selection-overlay .handle-w  { top: calc(50% - 5px); left: -6px; cursor: ew-resize; }
    #vesper-selection-overlay .handle-e  { top: calc(50% - 5px); right: -6px; cursor: ew-resize; }

    #vesper-selection-overlay .edge-zone {
      position: absolute;
      pointer-events: auto;
    }
    #vesper-selection-overlay .edge-n { top: -4px; left: 6px; right: 6px; height: 8px; cursor: ns-resize; }
    #vesper-selection-overlay .edge-s { bottom: -4px; left: 6px; right: 6px; height: 8px; cursor: ns-resize; }
    #vesper-selection-overlay .edge-w { left: -4px; top: 6px; bottom: 6px; width: 8px; cursor: ew-resize; }
    #vesper-selection-overlay .edge-e { right: -4px; top: 6px; bottom: 6px; width: 8px; cursor: ew-resize; }

    #vesper-size-tag {
      position: absolute;
      top: -26px;
      left: 0;
      background: rgba(11, 17, 30, 0.95);
      border: 1px solid rgba(0, 240, 255, 0.5);
      border-radius: 4px;
      padding: 2px 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: #00f0ff;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    .live-edit-focused {
      outline: 2px solid #fb792b !important;
      outline-offset: 2px;
      background: rgba(251, 121, 43, 0.12) !important;
      border-radius: 4px;
      caret-color: #fb792b !important;
    }
    .live-edit-selected {
      outline: 1.5px dashed #00f0ff !important;
      outline-offset: 2px;
    }
    .live-dragging {
      opacity: 0.88 !important;
      cursor: grabbing !important;
      box-shadow: 0 16px 40px rgba(0,0,0,0.8), 0 0 24px rgba(251,121,43,0.4) !important;
      z-index: 99999 !important;
      transition: none !important;
    }

    /* Unhidden Element Highlight */
    .vesper-just-unhidden {
      animation: unhide-highlight 2.5s ease-out forwards;
    }
    @keyframes unhide-highlight {
      0% { outline: 3px solid #10b981; box-shadow: 0 0 20px #10b981; }
      100% { outline: none; box-shadow: none; }
    }

    /* Preserved Layout Slot */
    .vesper-preserved-slot {
      background: rgba(13, 20, 36, 0.45) !important;
      border: 1.5px dashed rgba(0, 240, 255, 0.35) !important;
      border-radius: 8px !important;
      margin: 12px 0 !important;
      padding: 16px !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      min-height: 90px !important;
      box-sizing: border-box !important;
      position: relative !important;
      backdrop-filter: blur(8px) !important;
      cursor: pointer !important;
    }
    .vesper-preserved-slot:hover {
      border-color: #fb792b !important;
      background: rgba(251, 121, 43, 0.08) !important;
    }
    .vesper-preserved-slot .slot-title {
      font-family: 'Inter', system-ui, sans-serif !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 0.8px !important;
      color: #94a3b8 !important;
      text-transform: uppercase !important;
      margin-bottom: 4px !important;
    }
    .vesper-preserved-slot .slot-hint {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 10px !important;
      color: #64748b !important;
    }
    .vesper-preserved-slot .slot-actions {
      display: flex;
      gap: 8px;
      margin-top: 8px;
    }
    .vesper-preserved-slot .slot-btn {
      background: rgba(0, 240, 255, 0.15);
      border: 1px solid rgba(0, 240, 255, 0.3);
      color: #00f0ff;
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      font-family: 'Inter', system-ui, sans-serif;
      transition: all 0.15s;
    }
    .vesper-preserved-slot .slot-btn:hover {
      background: #00f0ff;
      color: #0b111e;
    }
    .vesper-preserved-slot .slot-btn-del {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.3);
      color: #ef4444;
    }
    .vesper-preserved-slot .slot-btn-del:hover {
      background: #ef4444;
      color: #ffffff;
    }

    /* Custom Cards */
    .vesper-custom-card {
      background: var(--card-bg, rgba(13, 20, 36, 0.92)) !important;
      border: 1px solid var(--accent-border, rgba(251, 121, 43, 0.3)) !important;
      border-radius: var(--radius, 8px) !important;
      padding: 18px 22px !important;
      margin: 16px 0 !important;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
      backdrop-filter: blur(12px) !important;
      color: var(--text-main, #e2e8f0) !important;
      position: relative !important;
      font-family: 'Inter', system-ui, sans-serif !important;
    }
    .vesper-custom-stat-card {
      background: var(--card-bg, rgba(13, 20, 36, 0.85)) !important;
      border: 1px solid rgba(0, 240, 255, 0.25) !important;
      border-radius: var(--radius, 8px) !important;
      padding: 16px 20px !important;
      margin: 12px 0 !important;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
      backdrop-filter: blur(10px) !important;
      font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* Context Menu */
    #vesper-editor-context-menu {
      position: fixed;
      z-index: 100001;
      background: #0b111e;
      border: 1px solid rgba(251, 121, 43, 0.3);
      border-radius: 8px;
      padding: 6px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.8), 0 0 20px rgba(0, 240, 255, 0.1);
      display: none;
      flex-direction: column;
      gap: 2px;
      min-width: 240px;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 12px;
      backdrop-filter: blur(16px);
    }
    .vec-header {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.8px;
      color: #fb792b;
      padding: 4px 10px;
      text-transform: uppercase;
    }
    .vec-item {
      padding: 7px 12px;
      color: #cbd5e1;
      border-radius: 5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: background 0.15s, color 0.15s;
    }
    .vec-item:hover {
      background: rgba(251, 121, 43, 0.2);
      color: #ffffff;
    }
    .vec-item span.icon {
      font-size: 14px;
      width: 16px;
      text-align: center;
    }
    .vec-divider {
      height: 1px;
      background: rgba(255,255,255,0.08);
      margin: 4px 0;
    }
  `;
  document.head.appendChild(styleEl);

  // ── 2. CREATE TOPBAR, FLOATING TOOLBAR, OVERLAY & CONTEXT MENU ──
  const topbar = document.createElement('div');
  topbar.id = 'vesper-editor-topbar';
  
  // Build palette swatches HTML
  let swatchesHtml = PALETTE_COLORS.map(c => 
    `<span class="vet-color-dot" style="background:${c.hex}" title="Apply ${c.name} (${c.hex})" data-color="${c.hex}"></span>`
  ).join('');

  topbar.innerHTML = `
    <div class="vet-left">
      <div class="vet-badge">
        <span class="vet-pulse"></span>
        <span>VESPER Visual Editor</span>
      </div>
      <div class="vet-status-pill" id="vet-save-status">Saved to disk (realtime)</div>
    </div>
    <div class="vet-center">
      <!-- Unhide All Button -->
      <button class="vet-btn unhide" id="vet-btn-unhide" title="Scan and restore any hidden buttons, controls, or sections">
        👁 Unhide All Buttons
      </button>
      <div class="vet-divider"></div>

      <!-- Color Pickers & Palette Swatches -->
      <div class="vet-picker-wrap" title="Custom Text Color">
        <span style="font-size:10px;color:#fb792b;font-weight:700;">TEXT:</span>
        <input type="color" id="vet-text-color-input" class="vet-color-input" value="#fb792b" title="Pick text color">
      </div>
      <div class="vet-picker-wrap" title="Custom Background Color">
        <span style="font-size:10px;color:#00f0ff;font-weight:700;">BG:</span>
        <input type="color" id="vet-bg-color-input" class="vet-color-input" value="#0d1424" title="Pick background color">
      </div>
      <div class="vet-color-swatch-group" title="Quick Color Palette">
        ${swatchesHtml}
      </div>

      <div class="vet-divider"></div>

      <!-- Undo / Redo -->
      <button class="vet-btn" id="vet-btn-undo" title="Undo (Ctrl+Z)">↶ Undo</button>
      <button class="vet-btn" id="vet-btn-redo" title="Redo (Ctrl+Y)">↷ Redo</button>

      <div class="vet-divider"></div>

      <!-- Module Insertion -->
      <button class="vet-btn cyan" id="vet-btn-add-card">+ Add Card</button>
      <button class="vet-btn cyan" id="vet-btn-add-stat">+ Add Stat</button>
      <button class="vet-btn" id="vet-btn-preserve-slot">[_] Preserve Slot</button>
      <button class="vet-btn" id="vet-btn-margin">| | Margin</button>

      <div class="vet-divider"></div>

      <!-- Save -->
      <button class="vet-btn primary" id="vet-btn-save">💾 Save to Disk</button>
    </div>
    <div class="vet-right">
      <a href="/" target="_blank" class="vet-live-link">
        <span>👁 Preview Live Platform</span>
        <span>↗</span>
      </a>
    </div>
  `;
  document.body.prepend(topbar);

  // Floating selection toolbar
  const floatBar = document.createElement('div');
  floatBar.id = 'vesper-floating-toolbar';
  floatBar.innerHTML = `
    <span style="font-weight:700;color:#00f0ff;font-size:10px;">FORMAT:</span>
    <button class="vft-btn" id="vft-color-text" title="Color Text (Saffron / Cyan / White)">Color Text</button>
    <button class="vft-btn" id="vft-color-bg" title="Color Background">Color BG</button>
    <button class="vft-btn" id="vft-toggle-vis" title="Toggle Visibility (Show/Hide)">👁 Toggle Vis</button>
    <button class="vft-btn" id="vft-margin" title="Toggle Margin Spacing">| | Margin</button>
    <button class="vft-btn" id="vft-dup" title="Duplicate (Ctrl+D)">++ Dup</button>
    <button class="vft-btn" id="vft-del" style="color:#ef4444;" title="Remove & Preserve Space">X Remove</button>
  `;
  document.body.appendChild(floatBar);

  const overlay = document.createElement('div');
  overlay.id = 'vesper-selection-overlay';
  overlay.innerHTML = `
    <div id="vesper-size-tag"><span>0 x 0</span></div>
    <div class="handle handle-nw" data-handle="nw"></div>
    <div class="handle handle-ne" data-handle="ne"></div>
    <div class="handle handle-sw" data-handle="sw"></div>
    <div class="handle handle-se" data-handle="se"></div>
    <div class="handle handle-n"  data-handle="n"></div>
    <div class="handle handle-s"  data-handle="s"></div>
    <div class="handle handle-w"  data-handle="w"></div>
    <div class="handle handle-e"  data-handle="e"></div>
    <div class="edge-zone edge-n" data-handle="n"></div>
    <div class="edge-zone edge-s" data-handle="s"></div>
    <div class="edge-zone edge-w" data-handle="w"></div>
    <div class="edge-zone edge-e" data-handle="e"></div>
  `;
  document.body.appendChild(overlay);

  const ctxMenu = document.createElement('div');
  ctxMenu.id = 'vesper-editor-context-menu';
  ctxMenu.innerHTML = `
    <div class="vec-header">VESPER Visual Tools</div>
    <div class="vec-item" data-action="unhide-all"><span class="icon" style="color:#10b981;">👁</span> Unhide All Hidden Buttons</div>
    <div class="vec-item" data-action="toggle-vis"><span class="icon" style="color:#00f0ff;">👁</span> Toggle Element Visibility</div>
    <div class="vec-divider"></div>
    <div class="vec-item" data-action="text-color"><span class="icon" style="color:#fb792b;">A</span> Change Text Color</div>
    <div class="vec-item" data-action="bg-color"><span class="icon" style="color:#64748b;">BG</span> Change Background Color</div>
    <div class="vec-item" data-action="border-accent"><span class="icon" style="color:#00f0ff;">-</span> Toggle Border Accent</div>
    <div class="vec-item" data-action="toggle-margin"><span class="icon" style="color:#94a3b8;">| |</span> Toggle Margin Spacing</div>
    <div class="vec-divider"></div>
    <div class="vec-item" data-action="add-card"><span class="icon" style="color:#fb792b;">+</span> Add Command Card</div>
    <div class="vec-item" data-action="add-stat"><span class="icon" style="color:#00f0ff;">+</span> Add Stat Metric Box</div>
    <div class="vec-item" data-action="add-text"><span class="icon" style="color:#e2e8f0;">T</span> Add Text Block</div>
    <div class="vec-item" data-action="preserve-slot"><span class="icon" style="color:#94a3b8;">[_]</span> Insert Preserved Slot</div>
    <div class="vec-divider"></div>
    <div class="vec-item" data-action="duplicate"><span class="icon" style="color:#10b981;">++</span> Duplicate (Ctrl+D)</div>
    <div class="vec-item" data-action="delete" style="color:#ef4444"><span class="icon">X</span> Remove & Preserve Space (Del)</div>
    <div class="vec-item" data-action="hard-delete" style="color:#f87171"><span class="icon">XX</span> Delete Entirely (Collapse)</div>
  `;
  document.body.appendChild(ctxMenu);

  function setSaveStatus(type, msg) {
    const el = document.getElementById('vet-save-status');
    if (!el) return;
    el.className = 'vet-status-pill ' + type;
    el.textContent = msg;
    if (type === 'saved') {
      setTimeout(() => {
        el.className = 'vet-status-pill';
        el.textContent = 'Saved to disk (realtime)';
      }, 3000);
    }
  }

  function hideContextMenu() {
    ctxMenu.style.display = 'none';
  }

  // ── 3. UNHIDE ALL BUTTONS & ELEMENTS ENGINE ──
  function unhideAllButtons() {
    pushUndo();
    let unhiddenCount = 0;

    // Scan all elements in the body
    const allEls = document.body.querySelectorAll('*');
    allEls.forEach(el => {
      // Don't modify editor internal overlay elements
      if (el.closest('#vesper-editor-topbar, #vesper-floating-toolbar, #vesper-selection-overlay, #vesper-editor-context-menu')) return;

      const cs = window.getComputedStyle(el);
      const isHiddenClass = el.classList.contains('hidden');
      const isDisplayNone = el.style.display === 'none' || (cs.display === 'none' && !el.classList.contains('window-panel'));
      const isVisHidden = el.style.visibility === 'hidden' || cs.visibility === 'hidden';
      const isZeroOpacity = el.style.opacity === '0';

      // If it's a modal or non-active window panel, keep standard modal hidden behavior unless it's a button inside
      if (el.classList.contains('window-panel') && !el.classList.contains('active')) return;

      if (isHiddenClass || isDisplayNone || isVisHidden || isZeroOpacity) {
        // If it's a modal backdrop, keep hidden unless user specifically clicked on it
        if (el.classList.contains('modal-backdrop')) return;

        el.classList.remove('hidden');
        if (el.style.display === 'none') {
          el.style.display = (el.tagName === 'BUTTON' || el.tagName === 'A' || el.tagName === 'SPAN') ? 'inline-flex' : 'block';
        }
        if (el.style.visibility === 'hidden') el.style.visibility = 'visible';
        if (el.style.opacity === '0') el.style.opacity = '1';

        el.classList.add('vesper-just-unhidden');
        unhiddenCount++;
      }
    });

    triggerAutoSave(true);
    setSaveStatus('saved', `Unhid ${unhiddenCount} elements/buttons`);
    alert(`VESPER Studio: Unhid ${unhiddenCount} hidden buttons and elements across the interface!`);
  }

  // ── 4. COLOR APPLICATION ENGINE ──
  function applyColorToSelection(color, type = 'text') {
    if (!selectedElement) {
      alert('Please click on any text, button, or card first to select it.');
      return;
    }
    pushUndo();

    if (type === 'text') {
      selectedElement.style.color = color;
      // If it has children text nodes or headings, apply color to them as well
      selectedElement.querySelectorAll('h1, h2, h3, h4, p, span, strong, em, .hs-val, .hs-label').forEach(child => {
        child.style.color = color;
      });
    } else if (type === 'bg') {
      selectedElement.style.backgroundColor = color;
      selectedElement.style.background = color;
    } else if (type === 'border') {
      selectedElement.style.borderColor = color;
      selectedElement.style.border = `1.5px solid ${color}`;
    }

    triggerAutoSave(true);
    setSaveStatus('saved', `Applied ${type} color ${color}`);
    updateOverlayPosition();
  }

  // Topbar Color Swatch Clicks
  document.addEventListener('click', (e) => {
    const swatch = e.target.closest('.vet-color-dot');
    if (swatch) {
      const color = swatch.dataset.color;
      applyColorToSelection(color, 'text');
    }
  });

  // Topbar Color Pickers
  document.getElementById('vet-text-color-input').addEventListener('input', (e) => {
    applyColorToSelection(e.target.value, 'text');
  });
  document.getElementById('vet-bg-color-input').addEventListener('input', (e) => {
    applyColorToSelection(e.target.value, 'bg');
  });

  // Floating Toolbar Handlers
  document.getElementById('vft-color-text').addEventListener('click', () => {
    const col = prompt('Enter text color hex (e.g. #fb792b, #00f0ff, #ffffff, #10b981):', '#fb792b');
    if (col) applyColorToSelection(col, 'text');
  });
  document.getElementById('vft-color-bg').addEventListener('click', () => {
    const col = prompt('Enter background color (e.g. rgba(13,20,36,0.92), #213d77, #0f172a, transparent):', 'rgba(13, 20, 36, 0.92)');
    if (col) applyColorToSelection(col, 'bg');
  });
  document.getElementById('vft-toggle-vis').addEventListener('click', () => {
    if (!selectedElement) return;
    pushUndo();
    if (selectedElement.style.display === 'none') {
      selectedElement.style.display = 'block';
      setSaveStatus('saved', 'Element Visible');
    } else {
      selectedElement.style.display = 'none';
      setSaveStatus('saved', 'Element Hidden (Use Unhide to restore)');
    }
    triggerAutoSave(true);
  });
  document.getElementById('vft-margin').addEventListener('click', () => {
    if (!selectedElement) return;
    const curMargin = parseInt(window.getComputedStyle(selectedElement).marginTop) || 0;
    const newMargin = curMargin >= 20 ? 10 : 24;
    selectedElement.style.margin = newMargin + 'px 0';
    updateOverlayPosition();
    triggerAutoSave(true);
  });
  document.getElementById('vft-dup').addEventListener('click', () => {
    if (!selectedElement) return;
    pushUndo();
    const clone = selectedElement.cloneNode(true);
    clone.classList.remove('live-edit-selected', 'live-edit-focused');
    if (clone.id) clone.id = clone.id + '-copy-' + Date.now().toString(36);
    selectedElement.parentElement.insertBefore(clone, selectedElement.nextSibling);
    selectElement(clone);
    triggerAutoSave(true);
  });
  document.getElementById('vft-del').addEventListener('click', () => {
    if (!selectedElement) return;
    removeElementAndPreserveSpace(selectedElement);
  });

  // ── 5. FULL PLATFORM TAB NAVIGATION ──
  document.addEventListener('click', (e) => {
    const tab = e.target.closest('.nav-tab');
    if (tab) {
      const winId = tab.dataset.window;
      if (winId) {
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        document.querySelectorAll('.window-panel').forEach(p => {
          p.classList.remove('active');
          if (p.id === 'window-' + winId) {
            p.classList.add('active');
          }
        });
        selectElement(null);
        window.dispatchEvent(new Event('resize'));
      }
    }
  });

  // ── 6. SELECTION OVERLAY & FLOATING TOOLBAR POSITIONING ──
  function updateOverlayPosition() {
    if (!selectedElement || !document.body.contains(selectedElement) || selectedElement.style.display === 'none') {
      overlay.classList.remove('active');
      floatBar.classList.remove('active');
      return;
    }

    const rect = selectedElement.getBoundingClientRect();
    const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    overlay.style.left = (rect.left + scrollX) + 'px';
    overlay.style.top = (rect.top + scrollY) + 'px';
    overlay.style.width = rect.width + 'px';
    overlay.style.height = rect.height + 'px';
    overlay.classList.add('active');

    // Position floating toolbar right above selection
    floatBar.style.left = Math.max(10, (rect.left + scrollX)) + 'px';
    floatBar.style.top = Math.max(56, (rect.top + scrollY - 36)) + 'px';
    floatBar.classList.add('active');

    const sizeSpan = overlay.querySelector('#vesper-size-tag span');
    if (sizeSpan) {
      sizeSpan.textContent = Math.round(rect.width) + ' x ' + Math.round(rect.height) + ' px';
    }
  }

  function selectElement(el) {
    if (selectedElement && selectedElement !== el) {
      selectedElement.classList.remove('live-edit-selected');
    }
    selectedElement = el;
    if (selectedElement) {
      selectedElement.classList.add('live-edit-selected');
      updateOverlayPosition();
    } else {
      overlay.classList.remove('active');
      floatBar.classList.remove('active');
    }
  }

  window.addEventListener('resize', updateOverlayPosition);
  window.addEventListener('scroll', updateOverlayPosition, true);

  // ── 7. UNDO / REDO ──
  function pushUndo() {
    try {
      const snap = getCleanHTML();
      undoStack.push(snap);
      if (undoStack.length > MAX_UNDO) undoStack.shift();
      redoStack = [];
    } catch(e) {}
  }

  function undo() {
    if (undoStack.length === 0) return;
    const current = getCleanHTML();
    redoStack.push(current);
    const prev = undoStack.pop();
    applyHTMLSnapshot(prev);
    triggerAutoSave(true);
  }

  function redo() {
    if (redoStack.length === 0) return;
    const current = getCleanHTML();
    undoStack.push(current);
    const next = redoStack.pop();
    applyHTMLSnapshot(next);
    triggerAutoSave(true);
  }

  function applyHTMLSnapshot(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const newMain = doc.querySelector('#windows-container');
    const curMain = document.querySelector('#windows-container');
    if (newMain && curMain) {
      curMain.innerHTML = newMain.innerHTML;
      selectElement(null);
    }
  }

  // ── 8. CLEAN HTML GENERATOR & DISK PERSISTENCE ──
  function getCleanHTML() {
    const clone = document.documentElement.cloneNode(true);

    // Remove Editor internal overlays
    clone.querySelectorAll(
      '#vesper-editor-topbar, #vesper-editor-injected-styles, #vesper-floating-toolbar, #vesper-selection-overlay, #vesper-editor-context-menu'
    ).forEach(el => el.remove());

    // Remove extension artifacts
    clone.querySelectorAll(
      '#preact-border-shadow-host, [popover="manual"], ' +
      '[data-grammarly-shadow-root], grammarly-desktop-integration, ' +
      '#dark-reader-style, .darkreader, ' +
      '[class*="extension-"], [id*="extension-"]'
    ).forEach(el => {
      if (!el.id || (!el.id.startsWith('vesper') && !el.id.startsWith('window-') && !el.id.startsWith('gov-') && !el.id.startsWith('top-bar') && !el.id.startsWith('nav-') && !el.id.startsWith('btn-') && !el.id.startsWith('stat-') && !el.id.startsWith('sc-') && !el.id.startsWith('modal-'))) {
        el.remove();
      }
    });

    // Remove selection styling & editable attributes
    clone.querySelectorAll('.live-edit-focused, .live-edit-selected, .live-dragging, .vesper-just-unhidden').forEach(el => {
      el.classList.remove('live-edit-focused', 'live-edit-selected', 'live-dragging', 'vesper-just-unhidden');
    });
    clone.querySelectorAll('[contenteditable]').forEach(el => {
      el.removeAttribute('contenteditable');
    });

    const body = clone.querySelector('body');
    if (body) {
      body.style.paddingTop = '';
      body.querySelectorAll('script[src="editor.js"], script[src="live-edit.js"]').forEach(s => s.remove());
      let hasApp = false;
      body.querySelectorAll('script[src="app.js"]').forEach(() => { hasApp = true; });
      if (!hasApp) {
        const appS = document.createElement('script');
        appS.src = 'app.js';
        body.appendChild(appS);
      }
    }

    return '<!DOCTYPE html>\n' + clone.outerHTML;
  }

  async function saveToDiskNow() {
    setSaveStatus('saving', 'Saving to disk...');
    try {
      const cleanHTML = getCleanHTML();
      const res = await fetch('/api/save-html', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ html: cleanHTML })
      });
      const data = await res.json();
      if (data.ok) {
        const sizeKB = Math.round(data.size / 1024);
        setSaveStatus('saved', 'Saved to disk (' + sizeKB + 'KB)');
      } else {
        setSaveStatus('saving', 'Save error: ' + data.error);
      }
    } catch(e) {
      setSaveStatus('saving', 'Network save error');
    }
  }

  function triggerAutoSave(immediate = false) {
    if (autoSaveTimeout) clearTimeout(autoSaveTimeout);
    setSaveStatus('saving', 'Auto-saving...');
    if (immediate) {
      saveToDiskNow();
    } else {
      autoSaveTimeout = setTimeout(saveToDiskNow, 800);
    }
  }

  // ── 9. SPACE PRESERVATION ON DELETION ──
  function removeElementAndPreserveSpace(el) {
    if (!el || !el.parentElement) return;
    pushUndo();

    const rect = el.getBoundingClientRect();
    const cs = window.getComputedStyle(el);
    const minH = Math.max(rect.height, 60);
    const minW = rect.width;
    const margin = cs.margin || '12px 0';
    const display = cs.display === 'inline' ? 'inline-block' : (cs.display || 'block');
    const flexGrow = cs.flexGrow || '0';
    const flexShrink = cs.flexShrink || '1';
    const flexBasis = cs.flexBasis || 'auto';

    const slot = document.createElement('div');
    slot.className = 'vesper-preserved-slot';
    slot.style.cssText = `
      min-height: ${minH}px;
      width: ${minW > 100 ? minW + 'px' : '100%'};
      margin: ${margin};
      display: ${display};
      flex-grow: ${flexGrow};
      flex-shrink: ${flexShrink};
      flex-basis: ${flexBasis};
    `;

    slot.innerHTML = `
      <div class="slot-title">Preserved Layout Slot (${Math.round(minW)} x ${Math.round(minH)}px)</div>
      <div class="slot-hint">Space preserved -- Click "+ Insert Card" to fill slot or right-click to customize</div>
      <div class="slot-actions">
        <button class="slot-btn" data-slot-action="insert-card">+ Insert Card</button>
        <button class="slot-btn" data-slot-action="insert-stat">+ Insert Stat</button>
        <button class="slot-btn slot-btn-del" data-slot-action="remove-slot" title="Remove slot and collapse space">X Remove Slot</button>
      </div>
    `;

    el.parentElement.replaceChild(slot, el);
    selectElement(slot);
    triggerAutoSave(true);
  }

  document.addEventListener('click', (e) => {
    const slotBtn = e.target.closest('.slot-btn');
    if (!slotBtn) return;
    const slot = slotBtn.closest('.vesper-preserved-slot');
    if (!slot || !slot.parentElement) return;

    const action = slotBtn.dataset.slotAction;
    pushUndo();

    if (action === 'insert-card') {
      const card = createVesperCard();
      slot.parentElement.replaceChild(card, slot);
      selectElement(card);
      triggerAutoSave(true);
    }
    else if (action === 'insert-stat') {
      const stat = createVesperStat();
      slot.parentElement.replaceChild(stat, slot);
      selectElement(stat);
      triggerAutoSave(true);
    }
    else if (action === 'remove-slot') {
      slot.remove();
      selectElement(null);
      triggerAutoSave(true);
    }
  });

  // ── 10. FACTORY FUNCTIONS (VESPER DESIGN SYSTEM) ──
  function createVesperCard() {
    const card = document.createElement('div');
    card.className = 'vesper-custom-card';
    card.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
        <span style="font-size:11px;font-weight:800;letter-spacing:0.8px;color:#fb792b;background:rgba(251,121,43,0.15);padding:2px 8px;border-radius:4px;border:1px solid rgba(251,121,43,0.3);font-family:'Inter',sans-serif;">TACTICAL MODULE</span>
        <span style="font-size:10px;color:#00f0ff;font-family:'JetBrains Mono',monospace;">STATUS // ONLINE</span>
      </div>
      <h3 style="color:#ffffff;font-size:16px;font-weight:700;margin:0 0 6px 0;font-family:'Inter',sans-serif;">Command Card Title</h3>
      <p style="color:#94a3b8;font-size:13px;line-height:1.5;margin:0;font-family:'Inter',sans-serif;">Double-click this text to edit directly. Drag borders or handles to resize effortlessly.</p>
    `;
    return card;
  }

  function createVesperStat() {
    const stat = document.createElement('div');
    stat.className = 'hero-stat-card vesper-custom-stat-card';
    stat.innerHTML = `
      <div class="hs-val" style="color:#00f0ff;font-size:24px;font-weight:800;font-family:'Inter',sans-serif;">99.8%</div>
      <div class="hs-label" style="color:#e2e8f0;font-size:12px;font-weight:600;margin-top:2px;font-family:'Inter',sans-serif;">Metric Title</div>
      <div class="hs-sub" style="color:#64748b;font-size:10px;margin-top:2px;font-family:'JetBrains Mono',monospace;">Real-Time Fleet Telemetry</div>
    `;
    return stat;
  }

  // ── 11. IN-PLACE TEXT EDITING (DOUBLE CLICK) ──
  const editableTextSelector = 'h1, h2, h3, h4, h5, h6, p, span, strong, em, b, i, td, th, li, .title, .desc, .stat-value, .hs-val, .hs-label, .hs-sub, .hero-subtitle, .hero-badge, .wfh-title';

  document.addEventListener('dblclick', (e) => {
    if (e.target.closest('#vesper-editor-topbar, #vesper-floating-toolbar, #vesper-selection-overlay, #vesper-editor-context-menu')) return;
    if (e.target.closest(INTERACTIVE_SELECTOR)) return;

    const txt = e.target.closest(editableTextSelector);
    if (txt && !txt.isContentEditable) {
      pushUndo();
      txt.contentEditable = 'true';
      txt.classList.add('live-edit-focused');
      txt.focus();

      const range = document.createRange();
      range.selectNodeContents(txt);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);

      const onBlur = () => {
        txt.contentEditable = 'false';
        txt.classList.remove('live-edit-focused');
        txt.removeEventListener('blur', onBlur);
        updateOverlayPosition();
        triggerAutoSave();
      };
      txt.addEventListener('blur', onBlur);

      e.preventDefault();
      e.stopPropagation();
    }
  });

  document.addEventListener('input', (e) => {
    if (e.target.isContentEditable) {
      updateOverlayPosition();
      triggerAutoSave();
    }
  });

  // ── 12. DIRECT DRAG & RESIZE ──
  document.addEventListener('mousedown', (e) => {
    if (e.button !== 0) return;
    hideContextMenu();

    const handleEl = e.target.closest('#vesper-selection-overlay [data-handle]');
    if (handleEl && selectedElement) {
      pushUndo();
      isResizing = true;
      resizeDir = handleEl.dataset.handle;
      const rect = selectedElement.getBoundingClientRect();
      const cs = window.getComputedStyle(selectedElement);
      
      dragStartPos = {
        mouseX: e.clientX,
        mouseY: e.clientY,
        width: rect.width,
        height: rect.height,
        marginT: parseFloat(cs.marginTop) || 0,
        marginB: parseFloat(cs.marginBottom) || 0,
        marginL: parseFloat(cs.marginLeft) || 0,
        marginR: parseFloat(cs.marginRight) || 0
      };
      e.preventDefault();
      e.stopPropagation();
      return;
    }

    if (e.target.closest('#vesper-editor-topbar, #vesper-floating-toolbar, #vesper-selection-overlay, #vesper-editor-context-menu')) return;
    if (e.target.isContentEditable) return;
    if (e.target.closest(INTERACTIVE_SELECTOR)) return;

    const target = findDraggableParent(e.target);
    if (target) {
      isMouseDown = true;
      pendingTarget = target;
      hasMovedDuringDrag = false;

      const rect = target.getBoundingClientRect();
      dragStartPos = {
        mouseX: e.clientX,
        mouseY: e.clientY,
        elX: parseFloat(target.style.left) || 0,
        elY: parseFloat(target.style.top) || 0,
        width: rect.width,
        height: rect.height
      };
      selectElement(target);
    } else {
      selectElement(null);
    }
  });

  function findDraggableParent(el) {
    const card = el.closest(DRAGGABLE_SELECTOR);
    if (card && card !== document.body && card !== document.documentElement) {
      return card;
    }
    let target = el.closest('div, section, article');
    if (!target || target === document.body || target === document.documentElement) return null;
    const layoutIds = ['windows-container', 'window-nav', 'top-bar', 'gov-utility-bar', 'bottom-status-bar'];
    if (layoutIds.includes(target.id)) return null;
    if (target.classList.contains('window-panel') && !target.classList.contains('vesper-custom-card')) return null;
    return target;
  }

  document.addEventListener('mousemove', (e) => {
    // Edge/Margin Resizing
    if (isResizing && selectedElement) {
      const dx = e.clientX - dragStartPos.mouseX;
      const dy = e.clientY - dragStartPos.mouseY;

      if (resizeDir.includes('e')) {
        const newW = Math.max(80, dragStartPos.width + dx);
        selectedElement.style.width = newW + 'px';
        selectedElement.style.maxWidth = 'none';
      } else if (resizeDir.includes('w')) {
        const newW = Math.max(80, dragStartPos.width - dx);
        selectedElement.style.width = newW + 'px';
        selectedElement.style.maxWidth = 'none';
        selectedElement.style.marginLeft = (dragStartPos.marginL + dx) + 'px';
      }

      if (resizeDir.includes('s')) {
        const newH = Math.max(40, dragStartPos.height + dy);
        selectedElement.style.height = newH + 'px';
        selectedElement.style.minHeight = newH + 'px';
      } else if (resizeDir.includes('n')) {
        const newH = Math.max(40, dragStartPos.height - dy);
        selectedElement.style.height = newH + 'px';
        selectedElement.style.minHeight = newH + 'px';
        selectedElement.style.marginTop = (dragStartPos.marginT + dy) + 'px';
      }

      updateOverlayPosition();
      e.preventDefault();
      return;
    }

    // Direct Dragging
    if (isMouseDown && pendingTarget) {
      const dx = e.clientX - dragStartPos.mouseX;
      const dy = e.clientY - dragStartPos.mouseY;
      const distance = Math.hypot(dx, dy);

      if (!isDragging && distance > 5) {
        pushUndo();
        isDragging = true;
        dragTarget = pendingTarget;
        hasMovedDuringDrag = true;

        const cs = window.getComputedStyle(dragTarget);
        if (cs.position === 'static') {
          dragTarget.style.position = 'relative';
        }
        dragTarget.classList.add('live-dragging');
      }

      if (isDragging && dragTarget) {
        dragTarget.style.left = (dragStartPos.elX + dx) + 'px';
        dragTarget.style.top = (dragStartPos.elY + dy) + 'px';
        updateOverlayPosition();
        e.preventDefault();
      }
    }
  });

  document.addEventListener('mouseup', (e) => {
    if (isResizing) {
      isResizing = false;
      resizeDir = null;
      triggerAutoSave(true);
      updateOverlayPosition();
    }

    if (isDragging && dragTarget) {
      dragTarget.classList.remove('live-dragging');
      isDragging = false;
      dragTarget = null;
      triggerAutoSave(true);
      updateOverlayPosition();
    }

    isMouseDown = false;
    pendingTarget = null;
  });

  document.addEventListener('click', (e) => {
    if (hasMovedDuringDrag) {
      e.preventDefault();
      e.stopPropagation();
      hasMovedDuringDrag = false;
    }
  }, true);

  // ── 13. CONTEXT MENU & TOPBAR ACTION LISTENERS ──
  document.addEventListener('contextmenu', (e) => {
    if (e.target.closest('#vesper-editor-topbar, #vesper-floating-toolbar')) return;
    if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;

    e.preventDefault();
    const target = e.target.closest('h1, h2, h3, h4, p, span, button, a, div, section, img, table, .vesper-custom-card, .hero-stat-card, .vesper-preserved-slot');
    if (!target || target === document.body) return;

    selectElement(target);

    ctxMenu.style.left = Math.min(e.clientX, window.innerWidth - 240) + 'px';
    ctxMenu.style.top = Math.min(e.clientY, window.innerHeight - 450) + 'px';
    ctxMenu.style.display = 'flex';
  });

  // Topbar Button Click Handlers
  document.getElementById('vet-btn-unhide').addEventListener('click', () => {
    unhideAllButtons();
  });
  document.getElementById('vet-btn-save').addEventListener('click', () => {
    saveToDiskNow();
  });
  document.getElementById('vet-btn-undo').addEventListener('click', () => {
    undo();
  });
  document.getElementById('vet-btn-redo').addEventListener('click', () => {
    redo();
  });
  document.getElementById('vet-btn-add-card').addEventListener('click', () => {
    const card = createVesperCard();
    const activeWin = document.querySelector('.window-panel.active') || document.body;
    activeWin.appendChild(card);
    selectElement(card);
    triggerAutoSave(true);
  });
  document.getElementById('vet-btn-add-stat').addEventListener('click', () => {
    const stat = createVesperStat();
    const activeWin = document.querySelector('.window-panel.active') || document.body;
    activeWin.appendChild(stat);
    selectElement(stat);
    triggerAutoSave(true);
  });
  document.getElementById('vet-btn-preserve-slot').addEventListener('click', () => {
    const activeWin = document.querySelector('.window-panel.active') || document.body;
    const slot = document.createElement('div');
    slot.className = 'vesper-preserved-slot';
    slot.innerHTML = `
      <div class="slot-title">Preserved Layout Slot</div>
      <div class="slot-hint">Space preserved -- Click "+ Insert Card" to fill slot</div>
      <div class="slot-actions">
        <button class="slot-btn" data-slot-action="insert-card">+ Insert Card</button>
        <button class="slot-btn" data-slot-action="insert-stat">+ Insert Stat</button>
        <button class="slot-btn slot-btn-del" data-slot-action="remove-slot">X Remove Slot</button>
      </div>
    `;
    activeWin.appendChild(slot);
    selectElement(slot);
    triggerAutoSave(true);
  });
  document.getElementById('vet-btn-margin').addEventListener('click', () => {
    if (!selectedElement) return;
    const curMargin = parseInt(window.getComputedStyle(selectedElement).marginTop) || 0;
    const newMargin = curMargin >= 20 ? 10 : 24;
    selectedElement.style.margin = newMargin + 'px 0';
    updateOverlayPosition();
    triggerAutoSave(true);
  });

  // Context Menu Actions
  ctxMenu.addEventListener('click', (e) => {
    const item = e.target.closest('.vec-item');
    if (!item) return;
    const action = item.dataset.action;
    hideContextMenu();

    if (action === 'unhide-all') {
      unhideAllButtons();
      return;
    }

    if (!selectedElement) return;
    pushUndo();

    if (action === 'toggle-vis') {
      if (selectedElement.style.display === 'none') {
        selectedElement.style.display = 'block';
        setSaveStatus('saved', 'Element Visible');
      } else {
        selectedElement.style.display = 'none';
        setSaveStatus('saved', 'Element Hidden');
      }
      triggerAutoSave(true);
    }
    else if (action === 'text-color') {
      const col = prompt('Enter text color (e.g. #fb792b, #00f0ff, #10b981, #ffffff):', '#fb792b');
      if (col) applyColorToSelection(col, 'text');
    } 
    else if (action === 'bg-color') {
      const bg = prompt('Enter background color (e.g. rgba(13,20,36,0.92), rgba(33,61,119,0.25), #0f172a):', 'rgba(13, 20, 36, 0.92)');
      if (bg) applyColorToSelection(bg, 'bg');
    } 
    else if (action === 'border-accent') {
      const curBorder = window.getComputedStyle(selectedElement).borderColor;
      const newBorder = (curBorder.includes('251') || curBorder.includes('orange')) ? '#00f0ff' : '#fb792b';
      applyColorToSelection(newBorder, 'border');
    }
    else if (action === 'toggle-margin') {
      const curMargin = parseInt(window.getComputedStyle(selectedElement).marginTop) || 0;
      const newMargin = curMargin >= 20 ? 10 : 24;
      selectedElement.style.margin = newMargin + 'px 0';
      updateOverlayPosition();
      triggerAutoSave(true);
    }
    else if (action === 'add-card') {
      const card = createVesperCard();
      selectedElement.parentElement.insertBefore(card, selectedElement.nextSibling);
      selectElement(card);
      triggerAutoSave(true);
    } 
    else if (action === 'add-stat') {
      const stat = createVesperStat();
      selectedElement.parentElement.insertBefore(stat, selectedElement.nextSibling);
      selectElement(stat);
      triggerAutoSave(true);
    }
    else if (action === 'add-text') {
      const p = document.createElement('p');
      p.textContent = 'New text block -- double click to edit';
      p.style.cssText = 'color:#cbd5e1;font-size:13px;margin:12px 0;line-height:1.6;font-family:Inter,sans-serif;';
      selectedElement.parentElement.insertBefore(p, selectedElement.nextSibling);
      selectElement(p);
      triggerAutoSave(true);
    }
    else if (action === 'preserve-slot') {
      const slot = document.createElement('div');
      slot.className = 'vesper-preserved-slot';
      slot.innerHTML = `
        <div class="slot-title">Preserved Layout Slot</div>
        <div class="slot-hint">Space preserved -- Click "+ Insert Card" to fill slot</div>
        <div class="slot-actions">
          <button class="slot-btn" data-slot-action="insert-card">+ Insert Card</button>
          <button class="slot-btn" data-slot-action="insert-stat">+ Insert Stat</button>
          <button class="slot-btn slot-btn-del" data-slot-action="remove-slot">X Remove Slot</button>
        </div>
      `;
      selectedElement.parentElement.insertBefore(slot, selectedElement.nextSibling);
      selectElement(slot);
      triggerAutoSave(true);
    }
    else if (action === 'duplicate') {
      const clone = selectedElement.cloneNode(true);
      clone.classList.remove('live-edit-selected', 'live-edit-focused');
      if (clone.id) clone.id = clone.id + '-copy-' + Date.now().toString(36);
      selectedElement.parentElement.insertBefore(clone, selectedElement.nextSibling);
      selectElement(clone);
      triggerAutoSave(true);
    } 
    else if (action === 'delete') {
      removeElementAndPreserveSpace(selectedElement);
    }
    else if (action === 'hard-delete') {
      selectedElement.remove();
      selectElement(null);
      triggerAutoSave(true);
    }
  });

  // ── 14. KEYBOARD SHORTCUTS ──
  document.addEventListener('keydown', (e) => {
    // Ctrl+S
    if (e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 's') {
      e.preventDefault();
      saveToDiskNow();
      return;
    }
    // Ctrl+Z
    if (e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 'z') {
      if (document.activeElement && document.activeElement.isContentEditable) return;
      e.preventDefault();
      undo();
      return;
    }
    // Ctrl+Y or Ctrl+Shift+Z
    if (e.ctrlKey && (e.key.toLowerCase() === 'y' || (e.shiftKey && e.key.toLowerCase() === 'z'))) {
      if (document.activeElement && document.activeElement.isContentEditable) return;
      e.preventDefault();
      redo();
      return;
    }
    // Ctrl+D
    if (e.ctrlKey && selectedElement && e.key.toLowerCase() === 'd') {
      if (document.activeElement && document.activeElement.isContentEditable) return;
      e.preventDefault();
      pushUndo();
      const clone = selectedElement.cloneNode(true);
      clone.classList.remove('live-edit-selected', 'live-edit-focused');
      if (clone.id) clone.id = clone.id + '-copy-' + Date.now().toString(36);
      selectedElement.parentElement.insertBefore(clone, selectedElement.nextSibling);
      selectElement(clone);
      triggerAutoSave(true);
      return;
    }
    // Delete / Backspace
    if (selectedElement && (e.key === 'Delete' || e.key === 'Backspace')) {
      if (document.activeElement && (document.activeElement.isContentEditable || ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName))) {
        return;
      }
      e.preventDefault();
      if (e.shiftKey) {
        selectedElement.remove();
        selectElement(null);
        triggerAutoSave(true);
      } else {
        removeElementAndPreserveSpace(selectedElement);
      }
      return;
    }
    // Escape
    if (e.key === 'Escape') {
      selectElement(null);
      if (document.activeElement) document.activeElement.blur();
      hideContextMenu();
    }
  });

  document.addEventListener('mousedown', (e) => {
    if (!e.target.closest('#vesper-editor-context-menu')) {
      hideContextMenu();
    }
  });

  console.log('%c VESPER Visual Studio Editor v3 Active %c Color System & Unhide Engine Ready', 'background:#fb792b;color:#ffffff;font-weight:bold;padding:4px 8px;border-radius:4px', 'color:#00f0ff;padding:4px');
})();
