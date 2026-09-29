/* ═══════════════════════════════════════════════════════════════════
   VESPER LIVE EDIT SYSTEM v2 — Direct Drag, Edge Resize & Space Preservation
   
   1. Direct Click & Drag: Click & drag any element/card directly without keyboard keys.
   2. Edge & Handle Resize: Grab borders or corner handles to resize width, height & margins.
   3. Space Preservation: When an element is deleted, its layout space is kept as a placeholder slot.
   4. Native In-Place Editing: Double-click any text to edit in-place with instant disk persistence.
   5. Zero-Interference: Tabs, buttons, links, inputs, and maps work natively without interception.
   6. Anti-Contamination: Browser extension artifacts are stripped before saving to disk.
   ═══════════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // Prevent double-initialization
  if (window.__vesperLiveEditInitialized) return;
  window.__vesperLiveEditInitialized = true;

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

  // ═══ INTERACTIVE ELEMENTS — these must NEVER be intercepted for dragging ═══
  const INTERACTIVE_SELECTOR = [
    'button', 'a', 'input', 'select', 'textarea', 'label',
    '.nav-tab', '.layout-btn', '.hero-cta', '.wfh-btn', '.iub-btn',
    '.top-bar-action', '.stat-pill', '.global-plate-btn', '.global-plate-input',
    '.api-status-action', '.studio-btn-link',
    '.slot-btn', '.assc-btn',
    '[onclick]', '[data-window]', '[data-layout]',
    '.leaflet-control', '.leaflet-container'
  ].join(', ');

  // Elements that are actually draggable cards/sections
  const DRAGGABLE_SELECTOR = [
    '.hero-stat-card', '.vesper-custom-card', '.vesper-custom-stat-card', '.vesper-preserved-slot',
    '.home-hero', '.card', '.modal-box', '.pane',
    '.info-card', '.stat-card', '.command-card', '.dashboard-card'
  ].join(', ');

  // ── 1. Inject Styles ──
  const styleEl = document.createElement('style');
  styleEl.id = 'vesper-live-edit-styles';
  styleEl.textContent = `
    /* Selection Outline & Handles Overlay */
    #vesper-selection-overlay {
      position: absolute;
      pointer-events: none;
      border: 1.5px solid #00f0ff;
      border-radius: 6px;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.4), inset 0 0 8px rgba(0, 240, 255, 0.1);
      z-index: 99990;
      display: none;
      transition: border-color 0.15s;
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
    /* 8 resize handle positions */
    #vesper-selection-overlay .handle-nw { top: -6px; left: -6px; cursor: nwse-resize; }
    #vesper-selection-overlay .handle-ne { top: -6px; right: -6px; cursor: nesw-resize; }
    #vesper-selection-overlay .handle-sw { bottom: -6px; left: -6px; cursor: nesw-resize; }
    #vesper-selection-overlay .handle-se { bottom: -6px; right: -6px; cursor: nwse-resize; }
    #vesper-selection-overlay .handle-n  { top: -6px; left: calc(50% - 5px); cursor: ns-resize; }
    #vesper-selection-overlay .handle-s  { bottom: -6px; left: calc(50% - 5px); cursor: ns-resize; }
    #vesper-selection-overlay .handle-w  { top: calc(50% - 5px); left: -6px; cursor: ew-resize; }
    #vesper-selection-overlay .handle-e  { top: calc(50% - 5px); right: -6px; cursor: ew-resize; }

    /* Edge drag zones inside overlay */
    #vesper-selection-overlay .edge-zone {
      position: absolute;
      pointer-events: auto;
    }
    #vesper-selection-overlay .edge-n { top: -4px; left: 6px; right: 6px; height: 8px; cursor: ns-resize; }
    #vesper-selection-overlay .edge-s { bottom: -4px; left: 6px; right: 6px; height: 8px; cursor: ns-resize; }
    #vesper-selection-overlay .edge-w { left: -4px; top: 6px; bottom: 6px; width: 8px; cursor: ew-resize; }
    #vesper-selection-overlay .edge-e { right: -4px; top: 6px; bottom: 6px; width: 8px; cursor: ew-resize; }

    /* Size Tag */
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
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* In-place focused editing */
    .live-edit-focused {
      outline: 2px solid #fb792b !important;
      outline-offset: 2px;
      background: rgba(251, 121, 43, 0.12) !important;
      border-radius: 4px;
      caret-color: #fb792b !important;
      box-shadow: 0 0 12px rgba(251, 121, 43, 0.4) !important;
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

    /* ── PRESERVED SPACE SLOTS ── */
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
      transition: border-color 0.2s, background-color 0.2s !important;
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

    /* VESPER Custom Card Styles (match site design system) */
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
      transition: border-color 0.2s, box-shadow 0.2s !important;
      font-family: 'Inter', system-ui, sans-serif !important;
    }
    .vesper-custom-card:hover {
      border-color: rgba(251, 121, 43, 0.6) !important;
      box-shadow: 0 6px 24px rgba(0, 0, 0, 0.6), 0 0 15px rgba(251, 121, 43, 0.15) !important;
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

    /* Toast Indicator */
    #live-edit-indicator {
      position: fixed;
      bottom: 18px;
      right: 18px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: rgba(10, 14, 23, 0.92);
      border: 1px solid rgba(0, 240, 255, 0.35);
      border-radius: 20px;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 24px rgba(0,0,0,0.6);
      z-index: 100000;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 11px;
      font-weight: 600;
      color: #94a3b8;
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      user-select: none;
    }
    #live-edit-indicator .live-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      transition: background 0.2s, box-shadow 0.2s;
    }
    #live-edit-indicator.saving .live-dot {
      background: #fb792b;
      box-shadow: 0 0 8px #fb792b;
      animation: live-pulse 0.6s infinite alternate;
    }
    #live-edit-indicator.saved .live-dot {
      background: #00f0ff;
      box-shadow: 0 0 8px #00f0ff;
    }
    @keyframes live-pulse {
      from { opacity: 0.4; transform: scale(0.8); }
      to { opacity: 1; transform: scale(1.2); }
    }

    /* Context Menu */
    #live-edit-context-menu {
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
      min-width: 230px;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 12px;
      backdrop-filter: blur(16px);
    }
    .live-ctx-header {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.8px;
      color: #fb792b;
      padding: 4px 10px;
      text-transform: uppercase;
    }
    .live-ctx-item {
      padding: 7px 12px;
      color: #cbd5e1;
      border-radius: 5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: background 0.15s, color 0.15s;
    }
    .live-ctx-item:hover {
      background: rgba(251, 121, 43, 0.2);
      color: #ffffff;
    }
    .live-ctx-item span.icon {
      font-size: 14px;
      width: 16px;
      text-align: center;
    }
    .live-ctx-divider {
      height: 1px;
      background: rgba(255,255,255,0.08);
      margin: 4px 0;
    }
  `;
  document.head.appendChild(styleEl);

  // ── 2. Create Overlay & Indicator ──
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

  const indicator = document.createElement('div');
  indicator.id = 'live-edit-indicator';
  indicator.innerHTML = '<span class="live-dot"></span><span id="live-indicator-text">VESPER Direct Edit Active</span>';
  document.body.appendChild(indicator);

  function setIndicatorStatus(type, msg) {
    indicator.className = type;
    const txt = document.getElementById('live-indicator-text');
    if (txt) txt.textContent = msg;
    if (type === 'saved') {
      setTimeout(() => {
        indicator.className = '';
        if (txt) txt.textContent = 'VESPER Direct Edit Active';
      }, 2500);
    }
  }

  // ── 3. Build Context Menu ──
  const ctxMenu = document.createElement('div');
  ctxMenu.id = 'live-edit-context-menu';
  ctxMenu.innerHTML = `
    <div class="live-ctx-header">VESPER Precision Controls</div>
    <div class="live-ctx-item" data-action="add-vesper-card"><span class="icon" style="font-weight:800;color:#fb792b;">+</span> Add Command Card</div>
    <div class="live-ctx-item" data-action="add-stat-card"><span class="icon" style="font-weight:800;color:#00f0ff;">+</span> Add Stat Metric Box</div>
    <div class="live-ctx-item" data-action="add-text"><span class="icon" style="font-weight:800;color:#e2e8f0;">T</span> Add Text Block</div>
    <div class="live-ctx-divider"></div>
    <div class="live-ctx-item" data-action="preserve-slot"><span class="icon" style="font-weight:800;color:#94a3b8;">[_]</span> Insert Preserved Slot Spacer</div>
    <div class="live-ctx-item" data-action="separate-box"><span class="icon" style="font-weight:800;color:#94a3b8;">| |</span> Toggle Margin Spacing</div>
    <div class="live-ctx-item" data-action="text-color"><span class="icon" style="font-weight:800;color:#fb792b;">A</span> Change Text Color</div>
    <div class="live-ctx-item" data-action="bg-color"><span class="icon" style="font-weight:800;color:#64748b;">BG</span> Change Background Color</div>
    <div class="live-ctx-item" data-action="border-accent"><span class="icon" style="font-weight:800;color:#00f0ff;">-</span> Toggle Border Accent</div>
    <div class="live-ctx-divider"></div>
    <div class="live-ctx-item" data-action="duplicate"><span class="icon" style="font-weight:800;color:#10b981;">++</span> Duplicate (Ctrl+D)</div>
    <div class="live-ctx-item" data-action="delete" style="color:#ef4444"><span class="icon" style="font-weight:800;">X</span> Remove & Preserve Space (Del)</div>
    <div class="live-ctx-item" data-action="hard-delete" style="color:#f87171"><span class="icon" style="font-weight:800;">XX</span> Delete Entirely (Collapse)</div>
  `;
  document.body.appendChild(ctxMenu);

  function hideContextMenu() {
    ctxMenu.style.display = 'none';
  }

  // ── 4. Undo / Redo System ──
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
    setIndicatorStatus('saved', 'Undo applied & saved');
  }

  function redo() {
    if (redoStack.length === 0) return;
    const current = getCleanHTML();
    undoStack.push(current);
    const next = redoStack.pop();
    applyHTMLSnapshot(next);
    triggerAutoSave(true);
    setIndicatorStatus('saved', 'Redo applied & saved');
  }

  function applyHTMLSnapshot(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const newBody = doc.body;
    
    // Remove all non-live-edit children from current body
    Array.from(document.body.children).forEach(child => {
      if (child.id !== 'live-edit-indicator' && 
          child.id !== 'live-edit-context-menu' && 
          child.id !== 'vesper-live-edit-styles' &&
          child.id !== 'vesper-selection-overlay') {
        child.remove();
      }
    });

    // Import new children
    Array.from(newBody.children).forEach(child => {
      if (child.tagName === 'SCRIPT' && child.getAttribute('src') === 'live-edit.js') return;
      document.body.appendChild(document.importNode(child, true));
    });

    // Re-add scripts
    const s = document.createElement('script');
    s.src = 'app.js';
    document.body.appendChild(s);
  }

  // ── 5. Clean HTML Generation — ANTI-CONTAMINATION FILTER ──
  function getCleanHTML() {
    const clone = document.documentElement.cloneNode(true);

    // Remove live-edit internal elements
    clone.querySelectorAll(
      '#vesper-live-edit-styles, #live-edit-indicator, #live-edit-context-menu, #vesper-selection-overlay'
    ).forEach(el => el.remove());
    
    // CRITICAL: Remove browser extension artifacts that pollute the DOM
    clone.querySelectorAll(
      '#preact-border-shadow-host, [popover="manual"], ' +
      '[data-grammarly-shadow-root], grammarly-desktop-integration, ' +
      '#dark-reader-style, .darkreader, ' +
      '[class*="extension-"], [id*="extension-"], ' +
      '[style*="position: fixed"][style*="width: 100vw"][style*="height: 100vh"][style*="pointer-events: none"]'
    ).forEach(el => {
      // Only remove if it looks like an extension artifact (not a VESPER element)
      if (!el.id || !el.id.startsWith('vesper') && !el.id.startsWith('window-') && 
          !el.id.startsWith('gov-') && !el.id.startsWith('top-bar') && 
          !el.id.startsWith('nav-') && !el.id.startsWith('btn-') &&
          !el.id.startsWith('stat-') && !el.id.startsWith('sc-') &&
          !el.id.startsWith('split-') && !el.id.startsWith('windows-') &&
          !el.id.startsWith('system-') && !el.id.startsWith('global-')) {
        el.remove();
      }
    });

    // Remove Antigravity scroll-lock artifacts
    clone.querySelectorAll('#antigravity-scroll-lock-style').forEach(el => el.remove());
    
    // Clean interactive classes
    clone.querySelectorAll('.live-edit-focused, .live-edit-selected, .live-dragging').forEach(el => {
      el.classList.remove('live-edit-focused', 'live-edit-selected', 'live-dragging');
    });

    // Clean body class from scroll-lock
    const body = clone.querySelector('body');
    if (body) {
      body.classList.remove('antigravity-scroll-lock');
    }

    clone.querySelectorAll('[contenteditable]').forEach(el => {
      el.removeAttribute('contenteditable');
    });

    // Ensure correct scripts in body
    if (body) {
      // Remove any existing live-edit, admin, or layout-loader scripts
      body.querySelectorAll(
        'script[src="live-edit.js"], script[src="admin.js"], script[src="layout-loader.js"]'
      ).forEach(s => s.remove());
      
      // Ensure app.js is present
      let hasApp = false;
      body.querySelectorAll('script[src="app.js"]').forEach(() => { hasApp = true; });
      if (!hasApp) {
        const appS = document.createElement('script');
        appS.src = 'app.js';
        body.appendChild(appS);
      }

      // Add live-edit.js last
      const editS = document.createElement('script');
      editS.src = 'live-edit.js';
      body.appendChild(editS);
    }

    return '<!DOCTYPE html>\n' + clone.outerHTML;
  }

  // ── 6. Disk Auto-Save ──
  async function saveToDiskNow() {
    setIndicatorStatus('saving', 'Saving to disk...');
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
        setIndicatorStatus('saved', 'Saved to disk (' + sizeKB + 'KB)');
      } else {
        setIndicatorStatus('saving', 'Save error: ' + data.error);
      }
    } catch(e) {
      setIndicatorStatus('saving', 'Network save error');
    }
  }

  function triggerAutoSave(immediate = false) {
    if (autoSaveTimeout) clearTimeout(autoSaveTimeout);
    setIndicatorStatus('saving', 'Auto-saving...');
    if (immediate) {
      saveToDiskNow();
    } else {
      autoSaveTimeout = setTimeout(saveToDiskNow, 800);
    }
  }

  // ── 7. Selection Overlay Positioning ──
  function updateOverlayPosition() {
    if (!selectedElement || !document.body.contains(selectedElement)) {
      overlay.classList.remove('active');
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
    }
  }

  window.addEventListener('resize', updateOverlayPosition);
  window.addEventListener('scroll', updateOverlayPosition, true);

  // ── 8. Space Preservation ──
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
    setIndicatorStatus('saved', 'Element Removed & Space Preserved');
  }

  // ── Slot button click handlers ──
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
      setIndicatorStatus('saved', 'Card Inserted into Slot');
    }
    else if (action === 'insert-stat') {
      const stat = createVesperStat();
      slot.parentElement.replaceChild(stat, slot);
      selectElement(stat);
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Stat Metric Inserted into Slot');
    }
    else if (action === 'remove-slot') {
      slot.remove();
      selectElement(null);
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Preserved Slot Removed');
    }
  });

  // ── Card & Stat Factories (matching VESPER design system) ──
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

  // ── 9. In-Place Text Editing (Double Click) ──
  const editableTextSelector = 'h1, h2, h3, h4, h5, h6, p, span, strong, em, b, i, td, th, li, .title, .desc, .stat-value, .hs-val, .hs-label, .hs-sub, .hero-subtitle, .hero-badge, .wfh-title';

  document.addEventListener('dblclick', (e) => {
    if (e.target.closest('#live-edit-indicator, #live-edit-context-menu, #vesper-selection-overlay')) return;
    // Don't intercept double-clicks on interactive elements
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

  // ── 10. DIRECT DRAG & RESIZE (NO KEYBOARD KEYS REQUIRED) ──
  
  // Handle Mousedown
  document.addEventListener('mousedown', (e) => {
    if (e.button !== 0) return;
    hideContextMenu();

    // 10A: Check if clicked on Resize Handle in Overlay
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

    // Ignore clicks on internal overlays
    if (e.target.closest('#live-edit-indicator, #live-edit-context-menu, #vesper-selection-overlay')) return;

    // Skip if actively editing text
    if (e.target.isContentEditable) return;

    // *** CRITICAL FIX: Let interactive elements work natively ***
    // If clicking on a button, tab, link, input etc., DO NOT initiate any drag.
    // Just let the native click happen.
    if (e.target.closest(INTERACTIVE_SELECTOR)) {
      return; // <-- This is the key fix for tab navigation
    }

    // 10B: Candidate for direct drag or selection
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
      // Click on empty space — deselect
      selectElement(null);
    }
  });

  // Find the best draggable parent for a given element
  function findDraggableParent(el) {
    // First try matching specific card/panel selectors
    const card = el.closest(DRAGGABLE_SELECTOR);
    if (card && card !== document.body && card !== document.documentElement) {
      return card;
    }

    // Fall back to generic containers, but be selective:
    // Only pick elements that are actual content containers, not the body/html/main layout shells
    let target = el.closest('div, section, article');
    if (!target || target === document.body || target === document.documentElement) return null;

    // Skip major layout containers (these shouldn't be dragged)
    const layoutIds = ['windows-container', 'window-nav', 'top-bar', 'gov-utility-bar', 'bottom-status-bar'];
    if (layoutIds.includes(target.id)) return null;
    
    // Skip if it's a window-panel (the main tab panels) - these are page sections not cards
    if (target.classList.contains('window-panel') && !target.classList.contains('vesper-custom-card')) return null;

    return target;
  }

  // Handle Mousemove
  document.addEventListener('mousemove', (e) => {
    // 10C: Border / Margin Resizing
    if (isResizing && selectedElement) {
      const dx = e.clientX - dragStartPos.mouseX;
      const dy = e.clientY - dragStartPos.mouseY;

      // Horizontal resize
      if (resizeDir.includes('e')) {
        const newW = Math.max(80, dragStartPos.width + dx);
        selectedElement.style.width = newW + 'px';
        selectedElement.style.maxWidth = 'none';
      } else if (resizeDir.includes('w')) {
        const newW = Math.max(80, dragStartPos.width - dx);
        selectedElement.style.width = newW + 'px';
        selectedElement.style.maxWidth = 'none';
        // Adjust margin-left for smooth west-side resize feel
        selectedElement.style.marginLeft = (dragStartPos.marginL + dx) + 'px';
      }

      // Vertical resize
      if (resizeDir.includes('s')) {
        const newH = Math.max(40, dragStartPos.height + dy);
        selectedElement.style.height = newH + 'px';
        selectedElement.style.minHeight = newH + 'px';
      } else if (resizeDir.includes('n')) {
        const newH = Math.max(40, dragStartPos.height - dy);
        selectedElement.style.height = newH + 'px';
        selectedElement.style.minHeight = newH + 'px';
        // Adjust margin-top for smooth north-side resize feel
        selectedElement.style.marginTop = (dragStartPos.marginT + dy) + 'px';
      }

      updateOverlayPosition();
      e.preventDefault();
      return;
    }

    // 10D: Direct Dragging
    if (isMouseDown && pendingTarget) {
      const dx = e.clientX - dragStartPos.mouseX;
      const dy = e.clientY - dragStartPos.mouseY;
      const distance = Math.hypot(dx, dy);

      // Drag threshold: 5px prevents accidental drags from normal clicks
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

  // Handle Mouseup
  document.addEventListener('mouseup', (e) => {
    if (isResizing) {
      isResizing = false;
      resizeDir = null;
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Resized & Saved');
      updateOverlayPosition();
    }

    if (isDragging && dragTarget) {
      dragTarget.classList.remove('live-dragging');
      isDragging = false;
      dragTarget = null;
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Repositioned & Saved');
      updateOverlayPosition();
    }

    isMouseDown = false;
    pendingTarget = null;
  });

  // Prevent ghost clicks after dragging
  document.addEventListener('click', (e) => {
    if (hasMovedDuringDrag) {
      e.preventDefault();
      e.stopPropagation();
      hasMovedDuringDrag = false;
    }
  }, true);

  // ── 11. Right-Click Context Menu ──
  document.addEventListener('contextmenu', (e) => {
    if (e.target.closest('#live-edit-indicator')) return;
    if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;

    e.preventDefault();
    const target = e.target.closest('h1, h2, h3, h4, p, span, button, a, div, section, img, table, .vesper-custom-card, .hero-stat-card, .vesper-preserved-slot');
    if (!target || target === document.body) return;

    selectElement(target);

    ctxMenu.style.left = Math.min(e.clientX, window.innerWidth - 240) + 'px';
    ctxMenu.style.top = Math.min(e.clientY, window.innerHeight - 400) + 'px';
    ctxMenu.style.display = 'flex';
  });

  // Context Menu Item Click Handlers
  ctxMenu.addEventListener('click', (e) => {
    const item = e.target.closest('.live-ctx-item');
    if (!item || !selectedElement) return;
    const action = item.dataset.action;
    hideContextMenu();

    pushUndo();

    if (action === 'add-vesper-card') {
      const card = createVesperCard();
      selectedElement.parentElement.insertBefore(card, selectedElement.nextSibling);
      selectElement(card);
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'VESPER Command Card Added & Saved');
    } 
    else if (action === 'add-stat-card') {
      const stat = createVesperStat();
      selectedElement.parentElement.insertBefore(stat, selectedElement.nextSibling);
      selectElement(stat);
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Stat Metric Box Added & Saved');
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
      setIndicatorStatus('saved', 'Preserved Slot Spacer Inserted');
    }
    else if (action === 'separate-box') {
      const curMargin = parseInt(window.getComputedStyle(selectedElement).marginTop) || 0;
      const newMargin = curMargin >= 20 ? 10 : 24;
      selectedElement.style.margin = newMargin + 'px 0';
      selectedElement.style.display = 'block';
      updateOverlayPosition();
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Margin Spacing: ' + newMargin + 'px');
    }
    else if (action === 'border-accent') {
      const curBorder = window.getComputedStyle(selectedElement).borderColor;
      if (curBorder.includes('251') || curBorder.includes('orange')) {
        selectedElement.style.borderColor = 'rgba(0, 240, 255, 0.4)';
        selectedElement.style.boxShadow = '0 0 15px rgba(0, 240, 255, 0.2)';
      } else {
        selectedElement.style.borderColor = 'rgba(251, 121, 43, 0.4)';
        selectedElement.style.boxShadow = '0 0 15px rgba(251, 121, 43, 0.2)';
      }
      triggerAutoSave(true);
    }
    else if (action === 'text-color') {
      const col = prompt('Enter text color (e.g. #fb792b (Saffron), #00f0ff (Cyan), #10b981 (Green), #ffffff):', '#fb792b');
      if (col) {
        selectedElement.style.color = col;
        triggerAutoSave(true);
      }
    } 
    else if (action === 'bg-color') {
      const bg = prompt('Enter background color (e.g. rgba(13,20,36,0.92), rgba(33,61,119,0.25), #0f172a):', 'rgba(13, 20, 36, 0.92)');
      if (bg) {
        selectedElement.style.backgroundColor = bg;
        triggerAutoSave(true);
      }
    } 
    else if (action === 'duplicate') {
      const clone = selectedElement.cloneNode(true);
      clone.classList.remove('live-edit-selected', 'live-edit-focused');
      if (clone.id) clone.id = clone.id + '-copy-' + Date.now().toString(36);
      selectedElement.parentElement.insertBefore(clone, selectedElement.nextSibling);
      selectElement(clone);
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Element Duplicated & Saved');
    } 
    else if (action === 'delete') {
      removeElementAndPreserveSpace(selectedElement);
    }
    else if (action === 'hard-delete') {
      selectedElement.remove();
      selectElement(null);
      triggerAutoSave(true);
      setIndicatorStatus('saved', 'Element Deleted & Layout Collapsed');
    }
  });

  // ── 12. Keyboard Shortcuts ──
  document.addEventListener('keydown', (e) => {
    // F2: start in-place text editing
    if (e.key === 'F2' && selectedElement) {
      const txt = selectedElement.closest(editableTextSelector) || selectedElement;
      if (txt && !txt.isContentEditable) {
        e.preventDefault();
        pushUndo();
        txt.contentEditable = 'true';
        txt.classList.add('live-edit-focused');
        txt.focus();
        const onBlur = () => {
          txt.contentEditable = 'false';
          txt.classList.remove('live-edit-focused');
          txt.removeEventListener('blur', onBlur);
          triggerAutoSave();
        };
        txt.addEventListener('blur', onBlur);
      }
      return;
    }

    // Ctrl+S: Manual save
    if (e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 's') {
      e.preventDefault();
      saveToDiskNow();
      return;
    }

    // Ctrl+Z: Undo
    if (e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 'z') {
      if (document.activeElement && document.activeElement.isContentEditable) return;
      e.preventDefault();
      undo();
      return;
    }

    // Ctrl+Y or Ctrl+Shift+Z: Redo
    if (e.ctrlKey && (e.key.toLowerCase() === 'y' || (e.shiftKey && e.key.toLowerCase() === 'z'))) {
      if (document.activeElement && document.activeElement.isContentEditable) return;
      e.preventDefault();
      redo();
      return;
    }

    // Ctrl+D: Duplicate
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
      setIndicatorStatus('saved', 'Duplicated (Ctrl+D)');
      return;
    }

    // Delete or Backspace: Remove & preserve space
    if (selectedElement && (e.key === 'Delete' || e.key === 'Backspace')) {
      if (document.activeElement && (document.activeElement.isContentEditable || ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName))) {
        return;
      }
      e.preventDefault();
      if (e.shiftKey) {
        // Shift+Del: hard delete (collapse layout)
        selectedElement.remove();
        selectElement(null);
        triggerAutoSave(true);
        setIndicatorStatus('saved', 'Hard Deleted (Layout Collapsed)');
      } else {
        // Normal Del: preserve space
        removeElementAndPreserveSpace(selectedElement);
      }
      return;
    }

    // Escape: clear selection
    if (e.key === 'Escape') {
      selectElement(null);
      if (document.activeElement) document.activeElement.blur();
      hideContextMenu();
    }
  });

  // ── 13. Click Anywhere to Dismiss Context Menu ──
  document.addEventListener('mousedown', (e) => {
    if (!e.target.closest('#live-edit-context-menu')) {
      hideContextMenu();
    }
  });

  console.log(
    '%c VESPER Direct Edit v2 Active %c Click & drag cards | Grab handles to resize | Tab navigation works | Del preserves slots', 
    'background:#00f0ff;color:#0b111e;font-weight:bold;padding:4px 8px;border-radius:4px',
    'color:#fb792b;padding:4px'
  );
})();
