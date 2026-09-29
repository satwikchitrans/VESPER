/* ═══════════════════════════════════════════════════════════════
   VESPER ADMIN PANEL — Permanent Visual Site Editor
   Toggle: Ctrl+Shift+A  or  floating button (bottom-right)
   
   ALL changes are saved PERMANENTLY to index.html on disk.
   The server creates automatic backups before each save.
   ═══════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // ── State ──
  let adminActive = false;
  let currentTool = 'select';
  let selectedEl = null;
  let isDragging = false;
  let isResizing = false;
  let dragOffset = { x: 0, y: 0 };
  let resizeDir = '';
  let resizeStart = { x: 0, y: 0, w: 0, h: 0, l: 0, t: 0 };
  let hasUnsavedChanges = false;
  let undoStack = [];
  let redoStack = [];
  const MAX_UNDO = 30;

  // ── Build Admin Panel DOM ──
  function buildPanel() {
    // Floating toggle button
    const fab = document.createElement('button');
    fab.className = 'admin-toggle-fab';
    fab.innerHTML = '⚙';
    fab.title = 'Toggle Admin Panel (Ctrl+Shift+A)';
    fab.addEventListener('click', toggleAdmin);
    document.body.appendChild(fab);

    // Toast notification
    const toast = document.createElement('div');
    toast.className = 'admin-toast';
    toast.id = 'admin-toast';
    document.body.appendChild(toast);

    // Sidebar
    const sidebar = document.createElement('div');
    sidebar.className = 'admin-panel-sidebar';
    sidebar.id = 'admin-panel';
    sidebar.innerHTML = `
      <!-- Header -->
      <div class="admin-header">
        <div class="admin-header-title">
          <span class="admin-badge">ADMIN</span>
          <span class="admin-name">Permanent Editor</span>
        </div>
        <button class="admin-close-btn" id="admin-close-btn">✕</button>
      </div>

      <!-- Status Bar -->
      <div class="admin-status-bar">
        <div style="display:flex;align-items:center">
          <span class="admin-status-dot" id="admin-status-dot"></span>
          <span class="admin-status-text" id="admin-status-text">Ready</span>
        </div>
        <div style="display:flex;gap:4px">
          <button class="admin-save-btn" id="admin-undo-btn" title="Undo (Ctrl+Z)">↩</button>
          <button class="admin-save-btn" id="admin-redo-btn" title="Redo (Ctrl+Y)">↪</button>
        </div>
      </div>

      <!-- Toolbar -->
      <div class="admin-toolbar">
        <button class="admin-tool-btn active" data-tool="select" title="Select & inspect elements">
          <span class="admin-tool-icon">⊕</span>
          <span class="admin-tool-label">Select</span>
        </button>
        <button class="admin-tool-btn" data-tool="move" title="Move elements freely">
          <span class="admin-tool-icon">✥</span>
          <span class="admin-tool-label">Move</span>
        </button>
        <button class="admin-tool-btn" data-tool="resize" title="Resize elements">
          <span class="admin-tool-icon">⤡</span>
          <span class="admin-tool-label">Resize</span>
        </button>
        <button class="admin-tool-btn" data-tool="edit" title="Edit text in-place">
          <span class="admin-tool-icon">T|</span>
          <span class="admin-tool-label">Edit</span>
        </button>
        <button class="admin-tool-btn" data-tool="text" title="Add a new text block">
          <span class="admin-tool-icon">T+</span>
          <span class="admin-tool-label">Text</span>
        </button>
        <button class="admin-tool-btn" data-tool="box" title="Add a new box/container">
          <span class="admin-tool-icon">☐</span>
          <span class="admin-tool-label">Box</span>
        </button>
        <button class="admin-tool-btn" data-tool="image" title="Add an image from URL">
          <span class="admin-tool-icon">🖼</span>
          <span class="admin-tool-label">Image</span>
        </button>
        <button class="admin-tool-btn" data-tool="color" title="Change colors of selected element">
          <span class="admin-tool-icon">🎨</span>
          <span class="admin-tool-label">Color</span>
        </button>
      </div>

      <!-- Scrollable Content -->
      <div class="admin-content" id="admin-content">
        <!-- Properties Section -->
        <div class="admin-section" id="admin-props-section" style="display:none">
          <div class="admin-section-header">SELECTED ELEMENT PROPERTIES</div>
          <div id="admin-selected-tag" style="margin-bottom:8px"></div>

          <div class="admin-prop-row">
            <span class="admin-prop-label">X (left)</span>
            <input class="admin-prop-input" id="prop-x" type="number" step="1">
            <span class="admin-prop-label" style="margin-left:8px">Y (top)</span>
            <input class="admin-prop-input" id="prop-y" type="number" step="1">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Width</span>
            <input class="admin-prop-input" id="prop-w" type="text" placeholder="auto">
            <span class="admin-prop-label" style="margin-left:8px">Height</span>
            <input class="admin-prop-input" id="prop-h" type="text" placeholder="auto">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Font Size</span>
            <input class="admin-prop-input" id="prop-fs" type="text" placeholder="14px">
            <span class="admin-prop-label" style="margin-left:8px">Weight</span>
            <select class="admin-prop-input" id="prop-fw" style="max-width:80px">
              <option value="">default</option>
              <option value="300">300</option>
              <option value="400">400</option>
              <option value="500">500</option>
              <option value="600">600</option>
              <option value="700">700</option>
              <option value="800">800</option>
              <option value="900">900</option>
            </select>
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">BG Color</span>
            <input class="admin-color-input" id="prop-bg" type="color" value="#111827">
            <span class="admin-prop-label" style="margin-left:8px">Text</span>
            <input class="admin-color-input" id="prop-color" type="color" value="#e2e8f0">
            <span class="admin-prop-label" style="margin-left:8px">Border</span>
            <input class="admin-color-input" id="prop-border-color" type="color" value="#333333">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Border</span>
            <input class="admin-prop-input" id="prop-border" type="text" placeholder="none" style="max-width:220px">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Radius</span>
            <input class="admin-prop-input" id="prop-radius" type="text" placeholder="0px">
            <span class="admin-prop-label" style="margin-left:8px">Padding</span>
            <input class="admin-prop-input" id="prop-padding" type="text" placeholder="0px">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Margin</span>
            <input class="admin-prop-input" id="prop-margin" type="text" placeholder="0px">
            <span class="admin-prop-label" style="margin-left:8px">Opacity</span>
            <input class="admin-prop-input" id="prop-opacity" type="number" min="0" max="1" step="0.05" value="1">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Display</span>
            <select class="admin-prop-input" id="prop-display" style="max-width:100px">
              <option value="">default</option>
              <option value="block">block</option>
              <option value="flex">flex</option>
              <option value="grid">grid</option>
              <option value="inline">inline</option>
              <option value="inline-block">inline-block</option>
              <option value="inline-flex">inline-flex</option>
              <option value="none">none (hidden)</option>
            </select>
            <span class="admin-prop-label" style="margin-left:8px">Position</span>
            <select class="admin-prop-input" id="prop-position" style="max-width:100px">
              <option value="">default</option>
              <option value="static">static</option>
              <option value="relative">relative</option>
              <option value="absolute">absolute</option>
              <option value="fixed">fixed</option>
              <option value="sticky">sticky</option>
            </select>
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Z-Index</span>
            <input class="admin-prop-input" id="prop-zindex" type="number" step="1" placeholder="auto">
            <span class="admin-prop-label" style="margin-left:8px">Overflow</span>
            <select class="admin-prop-input" id="prop-overflow" style="max-width:100px">
              <option value="">default</option>
              <option value="hidden">hidden</option>
              <option value="auto">auto</option>
              <option value="scroll">scroll</option>
              <option value="visible">visible</option>
            </select>
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Box Shadow</span>
            <input class="admin-prop-input" id="prop-shadow" type="text" placeholder="none" style="max-width:220px">
          </div>
          <div class="admin-prop-row">
            <span class="admin-prop-label">Text Align</span>
            <select class="admin-prop-input" id="prop-textalign" style="max-width:100px">
              <option value="">default</option>
              <option value="left">left</option>
              <option value="center">center</option>
              <option value="right">right</option>
              <option value="justify">justify</option>
            </select>
            <span class="admin-prop-label" style="margin-left:8px">Line H</span>
            <input class="admin-prop-input" id="prop-lineheight" type="text" placeholder="normal" style="max-width:60px">
          </div>

          <div class="admin-prop-row" style="margin-top:8px">
            <button class="admin-action-btn primary" id="admin-apply-props" style="flex:1;padding:5px 0;font-size:9px">APPLY CHANGES</button>
            <button class="admin-action-btn danger" id="admin-duplicate-el" style="flex:0.5;padding:5px 0;font-size:9px;margin-left:6px">CLONE</button>
            <button class="admin-action-btn danger" id="admin-delete-el" style="flex:0.5;padding:5px 0;font-size:9px;margin-left:6px">DELETE</button>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="admin-section">
          <div class="admin-section-header">QUICK ACTIONS</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px">
            <button class="admin-quick-btn" id="admin-add-section">+ Section</button>
            <button class="admin-quick-btn" id="admin-add-card">+ Card</button>
            <button class="admin-quick-btn" id="admin-add-heading">+ Heading</button>
            <button class="admin-quick-btn" id="admin-add-button">+ Button</button>
            <button class="admin-quick-btn" id="admin-add-divider">+ Divider</button>
            <button class="admin-quick-btn" id="admin-add-icon-box">+ Icon Box</button>
          </div>
        </div>

        <!-- Backups Section -->
        <div class="admin-section">
          <div class="admin-section-header">BACKUPS & HISTORY</div>
          <div id="admin-backups-list" style="max-height:120px;overflow-y:auto">
            <div style="color:#64748b;font-size:10px;padding:8px 0;text-align:center">Click 'SAVE' to create a backup</div>
          </div>
        </div>
      </div>

      <!-- Bottom Actions -->
      <div class="admin-actions">
        <button class="admin-action-btn primary" id="admin-save-all" style="flex:2">💾 SAVE TO DISK</button>
        <button class="admin-action-btn danger" id="admin-restore-btn" style="flex:1">↩ RESTORE</button>
      </div>
    `;

    document.body.appendChild(sidebar);
    bindPanelEvents();
  }

  // ── Bind Panel Events ──
  function bindPanelEvents() {
    document.getElementById('admin-close-btn').addEventListener('click', toggleAdmin);
    document.getElementById('admin-save-all').addEventListener('click', saveToDisk);
    document.getElementById('admin-restore-btn').addEventListener('click', restoreLastBackup);
    document.getElementById('admin-apply-props').addEventListener('click', applyProps);
    document.getElementById('admin-delete-el').addEventListener('click', deleteSelected);
    document.getElementById('admin-duplicate-el').addEventListener('click', duplicateSelected);
    document.getElementById('admin-undo-btn').addEventListener('click', undo);
    document.getElementById('admin-redo-btn').addEventListener('click', redo);

    // Quick actions
    document.getElementById('admin-add-section').addEventListener('click', () => addQuickElement('section'));
    document.getElementById('admin-add-card').addEventListener('click', () => addQuickElement('card'));
    document.getElementById('admin-add-heading').addEventListener('click', () => addQuickElement('heading'));
    document.getElementById('admin-add-button').addEventListener('click', () => addQuickElement('button'));
    document.getElementById('admin-add-divider').addEventListener('click', () => addQuickElement('divider'));
    document.getElementById('admin-add-icon-box').addEventListener('click', () => addQuickElement('icon-box'));

    // Tool buttons
    document.querySelectorAll('.admin-tool-btn[data-tool]').forEach(btn => {
      btn.addEventListener('click', () => {
        currentTool = btn.dataset.tool;
        document.querySelectorAll('.admin-tool-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        if (['text', 'box', 'image'].includes(currentTool)) {
          showToast(`Click anywhere on the page to place a new ${currentTool}`);
        }
      });
    });
  }

  // ── Toggle Admin ──
  function toggleAdmin() {
    adminActive = !adminActive;
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('open', adminActive);
    document.body.classList.toggle('admin-mode-active', adminActive);

    if (adminActive) {
      showToast('Admin mode ON — Edit the page, then SAVE TO DISK to make changes permanent');
      loadBackupsList();
    } else {
      clearSelection();
      removeAllHighlights();
      showToast('Admin mode OFF');
      if (hasUnsavedChanges) {
        showToast('⚠ You have unsaved changes! Open admin panel and click SAVE TO DISK');
      }
    }
  }

  // ── Toast ──
  function showToast(msg) {
    const t = document.getElementById('admin-toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timeout);
    t._timeout = setTimeout(() => t.classList.remove('show'), 3000);
  }

  // ── Status ──
  function setStatus(state, text) {
    const dot = document.getElementById('admin-status-dot');
    const txt = document.getElementById('admin-status-text');
    if (dot) dot.className = 'admin-status-dot ' + (state || '');
    if (txt) txt.textContent = text;
  }

  // ══════════════════════════════════════════════════════════════
  // UNDO / REDO SYSTEM
  // ══════════════════════════════════════════════════════════════
  function pushUndo() {
    // Snapshot relevant part of DOM for undo
    const snapshot = getCleanHTML();
    undoStack.push(snapshot);
    if (undoStack.length > MAX_UNDO) undoStack.shift();
    redoStack = []; // Clear redo on new action
    markUnsaved();
  }

  function undo() {
    if (undoStack.length === 0) {
      showToast('Nothing to undo');
      return;
    }
    // Save current state to redo
    redoStack.push(getCleanHTML());
    const prev = undoStack.pop();
    applyHTMLSnapshot(prev);
    showToast('Undone');
  }

  function redo() {
    if (redoStack.length === 0) {
      showToast('Nothing to redo');
      return;
    }
    undoStack.push(getCleanHTML());
    const next = redoStack.pop();
    applyHTMLSnapshot(next);
    showToast('Redone');
  }

  function applyHTMLSnapshot(html) {
    // We only snapshot the body content — parse and replace
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    
    // Get just the body children, excluding admin elements
    const newBody = doc.body;
    
    // Remove current non-admin body children
    Array.from(document.body.children).forEach(child => {
      if (!child.classList.contains('admin-panel-sidebar') &&
          !child.classList.contains('admin-toggle-fab') &&
          !child.classList.contains('admin-toast')) {
        child.remove();
      }
    });
    
    // Insert new content before admin elements
    const adminPanel = document.getElementById('admin-panel');
    Array.from(newBody.children).forEach(child => {
      document.body.insertBefore(document.importNode(child, true), adminPanel);
    });
  }

  function markUnsaved() {
    hasUnsavedChanges = true;
    setStatus('saving', 'Unsaved changes');
  }

  // ══════════════════════════════════════════════════════════════
  // CORE: GET CLEAN HTML (strips all admin UI from the DOM)
  // ══════════════════════════════════════════════════════════════
  function getCleanHTML() {
    // Clone the entire document
    const clone = document.documentElement.cloneNode(true);

    // Remove ALL admin panel elements from the clone
    const removeSelectors = [
      '.admin-panel-sidebar',
      '.admin-toggle-fab',
      '.admin-toast',
      '.admin-resize-handle',
      '.admin-highlight',
      '.admin-selected',
      '[data-admin-temp]'
    ];

    removeSelectors.forEach(sel => {
      clone.querySelectorAll(sel).forEach(el => el.remove());
    });

    // Remove admin-specific classes from elements
    clone.querySelectorAll('.admin-highlight, .admin-selected').forEach(el => {
      el.classList.remove('admin-highlight', 'admin-selected');
    });

    // Remove admin-mode-active class from body
    const bodyEl = clone.querySelector('body');
    if (bodyEl) {
      bodyEl.classList.remove('admin-mode-active');
    }

    // Remove contentEditable attribute that was set by admin
    clone.querySelectorAll('[contenteditable="true"]').forEach(el => {
      // Only remove if it was added by admin (not original)
      if (!el.dataset.originalEditable) {
        el.removeAttribute('contenteditable');
      }
    });

    // Ensure admin.css is in head
    const head = clone.querySelector('head');
    if (head) {
      let hasAdminCss = false;
      head.querySelectorAll('link').forEach(l => {
        if (l.getAttribute('href') === 'admin.css') hasAdminCss = true;
      });
      if (!hasAdminCss) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'admin.css';
        head.appendChild(link);
      }
    }

    // Ensure scripts in body
    const body = clone.querySelector('body');
    if (body) {
      // Remove any existing duplicate script tags for app, layout-loader, admin
      body.querySelectorAll('script[src="app.js"], script[src="layout-loader.js"], script[src="admin.js"]').forEach(s => s.remove());
      
      const appScript = document.createElement('script');
      appScript.src = 'app.js';
      body.appendChild(appScript);

      const loaderScript = document.createElement('script');
      loaderScript.src = 'layout-loader.js';
      body.appendChild(loaderScript);

      const adminScript = document.createElement('script');
      adminScript.src = 'admin.js';
      body.appendChild(adminScript);
    }

    // Get the full HTML string
    const doctype = '<!DOCTYPE html>';
    const html = doctype + '\n' + clone.outerHTML;

    return html;
  }

  // ══════════════════════════════════════════════════════════════
  // CORE: SAVE TO DISK — writes index.html permanently
  // ══════════════════════════════════════════════════════════════
  async function saveToDisk() {
    setStatus('saving', 'Saving to disk...');
    clearSelection();
    removeAllHighlights();

    try {
      const cleanHTML = getCleanHTML();
      
      const res = await fetch('/api/save-html', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ html: cleanHTML })
      });
      
      const data = await res.json();
      
      if (data.ok) {
        hasUnsavedChanges = false;
        const sizeKB = Math.round(data.size / 1024);
        setStatus('', `✓ Saved to disk (${sizeKB}KB) — ${new Date().toLocaleTimeString()}`);
        showToast(`✓ index.html saved permanently to disk (${sizeKB}KB). Backup: ${data.backup}`);
        loadBackupsList();
      } else {
        setStatus('error', 'Save failed: ' + data.error);
        showToast('✗ Save failed: ' + data.error);
      }
    } catch(e) {
      setStatus('error', 'Save error: ' + e.message);
      showToast('✗ Network error saving to disk');
      console.error('Save error:', e);
    }
  }

  // ── Restore from last backup ──
  async function restoreLastBackup() {
    if (!confirm('Restore the last backup? This will overwrite current index.html with the previous version. A new backup will be created first.')) return;

    try {
      const res = await fetch('/api/backups');
      const data = await res.json();
      
      if (!data.ok || data.backups.length === 0) {
        showToast('No backups found');
        return;
      }

      // Find most recent index.html backup
      const htmlBackup = data.backups.find(b => b.name.startsWith('index_'));
      if (!htmlBackup) {
        showToast('No HTML backups found');
        return;
      }

      const restoreRes = await fetch('/api/restore', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ backup: htmlBackup.name })
      });
      
      const restoreData = await restoreRes.json();
      if (restoreData.ok) {
        showToast('✓ Restored from backup — Reloading page...');
        setTimeout(() => location.reload(), 1000);
      } else {
        showToast('Restore failed: ' + restoreData.error);
      }
    } catch(e) {
      showToast('Restore error: ' + e.message);
    }
  }

  // ── Load backups list ──
  async function loadBackupsList() {
    try {
      const res = await fetch('/api/backups');
      const data = await res.json();
      const container = document.getElementById('admin-backups-list');
      
      if (!data.ok || data.backups.length === 0) {
        container.innerHTML = '<div style="color:#64748b;font-size:10px;padding:8px 0;text-align:center">No backups yet</div>';
        return;
      }

      container.innerHTML = data.backups.slice(0, 10).map(b => {
        const sizeKB = Math.round(b.size / 1024);
        const date = new Date(b.created).toLocaleString();
        return `<div class="admin-element-item" data-backup="${b.name}">
          <span class="admin-element-tag">BAK</span>
          <span class="admin-element-name" title="${b.name}">${date} (${sizeKB}KB)</span>
        </div>`;
      }).join('');

      container.querySelectorAll('.admin-element-item').forEach(item => {
        item.addEventListener('click', async () => {
          if (!confirm(`Restore backup ${item.dataset.backup}?`)) return;
          try {
            const res = await fetch('/api/restore', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ backup: item.dataset.backup })
            });
            const data = await res.json();
            if (data.ok) {
              showToast('✓ Restored — Reloading...');
              setTimeout(() => location.reload(), 1000);
            }
          } catch(e) {
            showToast('Restore error');
          }
        });
      });
    } catch(e) {
      console.warn('Could not load backups:', e);
    }
  }

  // ══════════════════════════════════════════════════════════════
  // ELEMENT SELECTION & PROPERTIES
  // ══════════════════════════════════════════════════════════════

  function removeAllHighlights() {
    document.querySelectorAll('.admin-highlight, .admin-selected').forEach(el => {
      el.classList.remove('admin-highlight', 'admin-selected');
    });
    removeResizeHandles();
  }

  function clearSelection() {
    if (selectedEl) {
      selectedEl.classList.remove('admin-selected');
      // Remove contentEditable if we set it
      if (selectedEl._adminSetEditable) {
        selectedEl.contentEditable = 'false';
        selectedEl.removeAttribute('contenteditable');
        delete selectedEl._adminSetEditable;
      }
      removeResizeHandles();
    }
    selectedEl = null;
    const propsSection = document.getElementById('admin-props-section');
    if (propsSection) propsSection.style.display = 'none';
  }

  function addResizeHandles(el) {
    removeResizeHandles();
    if (!el) return;

    const pos = window.getComputedStyle(el).position;
    if (pos === 'static') {
      el.style.position = 'relative';
    }

    ['nw','n','ne','w','e','sw','s','se'].forEach(dir => {
      const h = document.createElement('div');
      h.className = `admin-resize-handle ${dir}`;
      h.dataset.dir = dir;
      h.dataset.adminTemp = 'true';
      h.addEventListener('mousedown', startResize);
      el.appendChild(h);
    });
  }

  function removeResizeHandles() {
    document.querySelectorAll('.admin-resize-handle').forEach(h => h.remove());
  }

  function selectElement(el) {
    clearSelection();
    selectedEl = el;
    el.classList.add('admin-selected');
    addResizeHandles(el);
    populateProps(el);
    document.getElementById('admin-props-section').style.display = 'block';
  }

  function populateProps(el) {
    const cs = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();

    document.getElementById('admin-selected-tag').innerHTML =
      `<span class="admin-element-tag">${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').filter(c => !c.startsWith('admin-')).slice(0,2).join('.') : ''}</span>`;

    document.getElementById('prop-x').value = Math.round(rect.left + window.scrollX);
    document.getElementById('prop-y').value = Math.round(rect.top + window.scrollY);
    document.getElementById('prop-w').value = cs.width;
    document.getElementById('prop-h').value = cs.height;
    document.getElementById('prop-fs').value = cs.fontSize;
    document.getElementById('prop-fw').value = cs.fontWeight;
    document.getElementById('prop-border').value = el.style.border || '';
    document.getElementById('prop-radius').value = cs.borderRadius;
    document.getElementById('prop-padding').value = cs.padding;
    document.getElementById('prop-margin').value = cs.margin;
    document.getElementById('prop-opacity').value = cs.opacity;
    document.getElementById('prop-display').value = el.style.display || '';
    document.getElementById('prop-position').value = el.style.position || '';
    document.getElementById('prop-zindex').value = el.style.zIndex || '';
    document.getElementById('prop-overflow').value = el.style.overflow || '';
    document.getElementById('prop-shadow').value = el.style.boxShadow || '';
    document.getElementById('prop-textalign').value = el.style.textAlign || '';
    document.getElementById('prop-lineheight').value = el.style.lineHeight || '';

    // Color inputs
    try { document.getElementById('prop-bg').value = rgbToHex(cs.backgroundColor); } catch(e) { document.getElementById('prop-bg').value = '#111827'; }
    try { document.getElementById('prop-color').value = rgbToHex(cs.color); } catch(e) { document.getElementById('prop-color').value = '#e2e8f0'; }
    try { document.getElementById('prop-border-color').value = rgbToHex(cs.borderColor); } catch(e) { document.getElementById('prop-border-color').value = '#333333'; }
  }

  // ── Apply Properties ──
  function applyProps() {
    if (!selectedEl) return;
    pushUndo();

    const props = {
      width: document.getElementById('prop-w').value,
      height: document.getElementById('prop-h').value,
      fontSize: document.getElementById('prop-fs').value,
      fontWeight: document.getElementById('prop-fw').value,
      backgroundColor: document.getElementById('prop-bg').value,
      color: document.getElementById('prop-color').value,
      border: document.getElementById('prop-border').value,
      borderRadius: document.getElementById('prop-radius').value,
      padding: document.getElementById('prop-padding').value,
      margin: document.getElementById('prop-margin').value,
      opacity: document.getElementById('prop-opacity').value,
      display: document.getElementById('prop-display').value,
      position: document.getElementById('prop-position').value,
      zIndex: document.getElementById('prop-zindex').value,
      overflow: document.getElementById('prop-overflow').value,
      boxShadow: document.getElementById('prop-shadow').value,
      textAlign: document.getElementById('prop-textalign').value,
      lineHeight: document.getElementById('prop-lineheight').value,
    };

    // Apply each property
    Object.entries(props).forEach(([prop, val]) => {
      if (val === '' || val === undefined) return;
      
      // Handle numeric values that need units
      if (['width', 'height'].includes(prop) && val && isFinite(val)) {
        selectedEl.style[prop] = val + 'px';
      } else if (val) {
        selectedEl.style[prop] = val;
      }
    });

    // Position
    const x = document.getElementById('prop-x').value;
    const y = document.getElementById('prop-y').value;
    if (x && y) {
      if (!selectedEl.style.position || selectedEl.style.position === 'static') {
        selectedEl.style.position = 'absolute';
      }
      selectedEl.style.left = x + 'px';
      selectedEl.style.top = y + 'px';
    }

    markUnsaved();
    showToast('Properties applied (SAVE TO DISK to make permanent)');
  }

  // ── Delete Selected ──
  function deleteSelected() {
    if (!selectedEl) return;
    if (!confirm('Delete this element? Save to disk to make permanent.')) return;

    pushUndo();
    selectedEl.remove();
    clearSelection();
    markUnsaved();
    showToast('Element deleted (SAVE TO DISK to make permanent)');
  }

  // ── Duplicate Selected ──
  function duplicateSelected() {
    if (!selectedEl) return;
    pushUndo();

    const clone = selectedEl.cloneNode(true);
    clone.classList.remove('admin-selected', 'admin-highlight');
    clone.querySelectorAll('.admin-resize-handle').forEach(h => h.remove());
    
    // Offset position
    const cs = window.getComputedStyle(selectedEl);
    if (cs.position === 'absolute' || cs.position === 'fixed') {
      clone.style.left = (parseFloat(clone.style.left) || 0) + 20 + 'px';
      clone.style.top = (parseFloat(clone.style.top) || 0) + 20 + 'px';
    }
    
    // Remove any IDs to avoid duplicates
    if (clone.id) clone.id = clone.id + '-copy-' + Date.now();

    selectedEl.parentElement.insertBefore(clone, selectedEl.nextSibling);
    selectElement(clone);
    markUnsaved();
    showToast('Element cloned');
  }

  // ── Create New Elements ──
  function createElement(type, x, y) {
    pushUndo();

    const el = document.createElement('div');
    el.style.position = 'absolute';
    el.style.left = (x + window.scrollX) + 'px';
    el.style.top = (y + window.scrollY) + 'px';
    el.style.zIndex = '9990';

    if (type === 'text') {
      el.style.width = '200px';
      el.style.padding = '8px 12px';
      el.style.color = '#e2e8f0';
      el.style.fontFamily = 'Inter, sans-serif';
      el.style.fontSize = '14px';
      el.textContent = 'New Text Block';
      el.contentEditable = 'true';
    } else if (type === 'box') {
      el.style.width = '200px';
      el.style.height = '120px';
      el.style.background = 'rgba(33, 61, 119, 0.15)';
      el.style.border = '1.5px solid rgba(33, 61, 119, 0.4)';
      el.style.borderRadius = '6px';
      el.style.padding = '12px';
      el.innerHTML = '<span style="color:#94a3b8;font-size:11px">New Container</span>';
    } else if (type === 'image') {
      const url = prompt('Enter image URL:');
      if (!url) return;
      el.style.width = '200px';
      el.style.height = '150px';
      el.style.borderRadius = '6px';
      el.style.overflow = 'hidden';
      el.innerHTML = `<img src="${url}" alt="Image" style="width:100%;height:100%;object-fit:cover;display:block">`;
    }

    document.body.appendChild(el);
    selectElement(el);
    markUnsaved();
    showToast(`${type} created (SAVE TO DISK to keep permanently)`);

    // Switch back to select tool
    currentTool = 'select';
    document.querySelectorAll('.admin-tool-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.admin-tool-btn[data-tool="select"]').classList.add('active');
  }

  // ── Quick Add Elements ──
  function addQuickElement(type) {
    pushUndo();

    const el = document.createElement('div');
    // Insert at a reasonable position — center of viewport
    const cx = window.innerWidth / 2 - 150 + window.scrollX;
    const cy = window.innerHeight / 2 - 60 + window.scrollY;

    switch(type) {
      case 'section':
        el.style.cssText = `width:100%;padding:40px 20px;margin:20px 0;background:rgba(33,61,119,0.08);border:1px solid rgba(33,61,119,0.2);border-radius:12px;`;
        el.innerHTML = `<h2 style="color:#e2e8f0;font-size:20px;font-weight:700;margin:0 0 12px 0;font-family:Inter,sans-serif">New Section</h2><p style="color:#94a3b8;font-size:13px;margin:0;font-family:Inter,sans-serif">Add content here</p>`;
        // Insert before the scripts at the bottom
        const scripts = document.querySelectorAll('body > script');
        if (scripts.length > 0) {
          document.body.insertBefore(el, scripts[0]);
        } else {
          document.body.appendChild(el);
        }
        break;
      case 'card':
        el.style.cssText = `position:absolute;left:${cx}px;top:${cy}px;width:280px;padding:20px;background:rgba(17,24,39,0.9);border:1px solid rgba(251,121,43,0.2);border-radius:10px;backdrop-filter:blur(8px);z-index:9990;`;
        el.innerHTML = `<div style="font-size:14px;font-weight:700;color:#fb792b;margin-bottom:8px;font-family:Inter,sans-serif">Card Title</div><div style="font-size:12px;color:#94a3b8;line-height:1.5;font-family:Inter,sans-serif">Card description text goes here. Click Edit tool to change.</div>`;
        document.body.appendChild(el);
        break;
      case 'heading':
        el.style.cssText = `position:absolute;left:${cx}px;top:${cy}px;z-index:9990;`;
        el.innerHTML = `<h2 style="color:#e2e8f0;font-size:24px;font-weight:800;margin:0;font-family:Inter,sans-serif;letter-spacing:-0.5px">New Heading</h2>`;
        document.body.appendChild(el);
        break;
      case 'button':
        const btn = document.createElement('button');
        btn.style.cssText = `position:absolute;left:${cx}px;top:${cy}px;padding:10px 24px;background:linear-gradient(135deg,#fb792b,#ea580c);color:#fff;border:none;border-radius:6px;font-size:13px;font-weight:700;font-family:Inter,sans-serif;cursor:pointer;letter-spacing:0.5px;z-index:9990;`;
        btn.textContent = 'New Button';
        document.body.appendChild(btn);
        selectElement(btn);
        markUnsaved();
        showToast('Button created');
        return;
      case 'divider':
        const hr = document.createElement('hr');
        hr.style.cssText = `margin:20px 0;border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(251,121,43,0.3),transparent);`;
        const scripts2 = document.querySelectorAll('body > script');
        if (scripts2.length > 0) {
          document.body.insertBefore(hr, scripts2[0]);
        } else {
          document.body.appendChild(hr);
        }
        selectElement(hr);
        markUnsaved();
        showToast('Divider created');
        return;
      case 'icon-box':
        el.style.cssText = `position:absolute;left:${cx}px;top:${cy}px;width:60px;height:60px;display:flex;align-items:center;justify-content:center;background:rgba(33,61,119,0.2);border:1px solid rgba(251,121,43,0.3);border-radius:12px;font-size:24px;z-index:9990;cursor:pointer;`;
        el.textContent = '⚡';
        document.body.appendChild(el);
        break;
    }

    selectElement(el);
    markUnsaved();
    showToast(`${type} created (SAVE TO DISK to keep permanently)`);
  }

  // ══════════════════════════════════════════════════════════════
  // DRAG & RESIZE LOGIC
  // ══════════════════════════════════════════════════════════════
  function startDrag(e) {
    if (!selectedEl || !adminActive) return;
    pushUndo();
    isDragging = true;

    const rect = selectedEl.getBoundingClientRect();
    dragOffset.x = e.clientX - rect.left;
    dragOffset.y = e.clientY - rect.top;

    const cs = window.getComputedStyle(selectedEl);
    if (cs.position === 'static') selectedEl.style.position = 'relative';
    if (cs.position !== 'absolute' && cs.position !== 'fixed') {
      selectedEl.style.position = 'absolute';
      selectedEl.style.left = rect.left + window.scrollX + 'px';
      selectedEl.style.top = rect.top + window.scrollY + 'px';
    }

    e.preventDefault();
  }

  function doDrag(e) {
    if (!isDragging || !selectedEl) return;
    const x = e.clientX - dragOffset.x + window.scrollX;
    const y = e.clientY - dragOffset.y + window.scrollY;
    selectedEl.style.left = x + 'px';
    selectedEl.style.top = y + 'px';
    document.getElementById('prop-x').value = Math.round(x);
    document.getElementById('prop-y').value = Math.round(y);
    e.preventDefault();
  }

  function endDrag() {
    if (isDragging && selectedEl) {
      markUnsaved();
    }
    isDragging = false;
  }

  function startResize(e) {
    if (!selectedEl || !adminActive) return;
    pushUndo();
    isResizing = true;
    resizeDir = e.target.dataset.dir;
    const rect = selectedEl.getBoundingClientRect();
    resizeStart = {
      x: e.clientX, y: e.clientY,
      w: rect.width, h: rect.height,
      l: parseFloat(selectedEl.style.left) || rect.left + window.scrollX,
      t: parseFloat(selectedEl.style.top) || rect.top + window.scrollY
    };
    e.preventDefault();
    e.stopPropagation();
  }

  function doResize(e) {
    if (!isResizing || !selectedEl) return;
    const dx = e.clientX - resizeStart.x;
    const dy = e.clientY - resizeStart.y;

    let newW = resizeStart.w, newH = resizeStart.h;
    let newL = resizeStart.l, newT = resizeStart.t;

    if (resizeDir.includes('e')) newW = Math.max(20, resizeStart.w + dx);
    if (resizeDir.includes('w')) { newW = Math.max(20, resizeStart.w - dx); newL = resizeStart.l + dx; }
    if (resizeDir.includes('s')) newH = Math.max(20, resizeStart.h + dy);
    if (resizeDir.includes('n')) { newH = Math.max(20, resizeStart.h - dy); newT = resizeStart.t + dy; }

    selectedEl.style.width = newW + 'px';
    selectedEl.style.height = newH + 'px';
    selectedEl.style.left = newL + 'px';
    selectedEl.style.top = newT + 'px';

    document.getElementById('prop-w').value = Math.round(newW) + 'px';
    document.getElementById('prop-h').value = Math.round(newH) + 'px';
    e.preventDefault();
  }

  function endResize() {
    if (isResizing && selectedEl) markUnsaved();
    isResizing = false;
  }

  // ══════════════════════════════════════════════════════════════
  // EVENT HANDLERS
  // ══════════════════════════════════════════════════════════════

  function onPageClick(e) {
    if (!adminActive) return;

    // Ignore admin panel clicks
    if (e.target.closest('.admin-panel-sidebar') || e.target.closest('.admin-toggle-fab') || e.target.closest('.admin-toast')) return;
    if (e.target.classList.contains('admin-resize-handle')) return;

    if (['text', 'box', 'image'].includes(currentTool)) {
      createElement(currentTool, e.clientX, e.clientY);
      e.preventDefault();
      e.stopPropagation();
      return;
    }

    if (currentTool === 'edit') {
      const target = e.target;
      if (target.closest('.admin-panel-sidebar')) return;
      pushUndo();
      target._adminSetEditable = true;
      target.contentEditable = 'true';
      target.classList.add('admin-inline-editor');
      target.focus();
      target.addEventListener('blur', function onBlur() {
        target.contentEditable = 'false';
        target.removeAttribute('contenteditable');
        target.classList.remove('admin-inline-editor');
        target.removeEventListener('blur', onBlur);
        delete target._adminSetEditable;
        markUnsaved();
        showToast('Text updated (SAVE TO DISK to keep)');
      }, { once: true });
      e.preventDefault();
      return;
    }

    // Select / Move / Color tool
    const target = e.target.closest('[id], div, section, header, nav, span, p, h1, h2, h3, h4, h5, h6, button, a, img, table, td, th, tr, ul, li, form, input, label, footer, aside, article, main, figure, figcaption, details, summary');
    if (!target || target === document.body || target === document.documentElement) {
      clearSelection();
      return;
    }

    selectElement(target);

    if (currentTool === 'move') {
      startDrag(e);
    }

    if (currentTool === 'color') {
      pushUndo();
      const newColor = prompt('Enter background color (hex or CSS):', window.getComputedStyle(target).backgroundColor);
      if (newColor) {
        target.style.backgroundColor = newColor;
        markUnsaved();
        showToast('Color applied');
      }
    }

    e.preventDefault();
    e.stopPropagation();
  }

  function onPageMouseMove(e) {
    if (!adminActive || isDragging || isResizing) return;
    if (e.target.closest('.admin-panel-sidebar') || e.target.closest('.admin-toggle-fab')) return;

    // Remove previous hover highlights
    document.querySelectorAll('.admin-highlight').forEach(el => {
      if (!el.classList.contains('admin-selected')) el.classList.remove('admin-highlight');
    });

    if (['select', 'move', 'resize', 'edit', 'color'].includes(currentTool)) {
      const target = e.target.closest('[id], div, section, header, nav, span, p, h1, h2, h3, h4, h5, h6, button, a, img, table');
      if (target && target !== document.body && target !== document.documentElement && !target.closest('.admin-panel-sidebar')) {
        target.classList.add('admin-highlight');
      }
    }
  }

  // Global mouse events
  document.addEventListener('mousemove', (e) => {
    if (isDragging) doDrag(e);
    if (isResizing) doResize(e);
    onPageMouseMove(e);
  });
  document.addEventListener('mouseup', () => {
    endDrag();
    endResize();
  });

  // ── Keyboard Shortcuts ──
  document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+A — toggle admin
    if (e.ctrlKey && e.shiftKey && e.key.toUpperCase() === 'A') {
      e.preventDefault();
      toggleAdmin();
    }

    // Ctrl+S — save to disk
    if (adminActive && e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 's') {
      e.preventDefault();
      saveToDisk();
    }

    // Ctrl+Z — undo
    if (adminActive && e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 'z') {
      if (document.activeElement && document.activeElement.contentEditable === 'true') return;
      e.preventDefault();
      undo();
    }

    // Ctrl+Y or Ctrl+Shift+Z — redo
    if (adminActive && e.ctrlKey && (e.key.toLowerCase() === 'y' || (e.shiftKey && e.key.toLowerCase() === 'z'))) {
      if (document.activeElement && document.activeElement.contentEditable === 'true') return;
      e.preventDefault();
      redo();
    }

    // Delete key
    if (adminActive && selectedEl && (e.key === 'Delete')) {
      if (document.activeElement && document.activeElement.contentEditable === 'true') return;
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
      deleteSelected();
      e.preventDefault();
    }

    // Ctrl+D — duplicate
    if (adminActive && selectedEl && e.ctrlKey && e.key.toLowerCase() === 'd') {
      e.preventDefault();
      duplicateSelected();
    }

    // Arrow keys for nudging
    if (adminActive && selectedEl && ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) {
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
      if (document.activeElement && document.activeElement.contentEditable === 'true') return;
      e.preventDefault();
      pushUndo();
      const step = e.shiftKey ? 10 : 1;
      const cs = window.getComputedStyle(selectedEl);
      if (cs.position === 'static') selectedEl.style.position = 'relative';

      let l = parseFloat(selectedEl.style.left) || 0;
      let t = parseFloat(selectedEl.style.top) || 0;

      if (e.key === 'ArrowLeft') l -= step;
      if (e.key === 'ArrowRight') l += step;
      if (e.key === 'ArrowUp') t -= step;
      if (e.key === 'ArrowDown') t += step;

      selectedEl.style.left = l + 'px';
      selectedEl.style.top = t + 'px';
      document.getElementById('prop-x').value = Math.round(l);
      document.getElementById('prop-y').value = Math.round(t);
      markUnsaved();
    }
  });

  // Page click listener
  document.addEventListener('click', onPageClick, true);

  // ── RGB to Hex ──
  function rgbToHex(rgb) {
    if (!rgb || rgb === 'transparent' || rgb === 'rgba(0, 0, 0, 0)') return '#111827';
    const m = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    if (!m) return '#111827';
    return '#' + [m[1], m[2], m[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
  }

  // ── Before Unload Warning ──
  window.addEventListener('beforeunload', (e) => {
    if (hasUnsavedChanges) {
      e.preventDefault();
      e.returnValue = 'You have unsaved changes. Save to disk first?';
    }
  });

  // ── Initialize ──
  function init() {
    buildPanel();
    console.log('%c VESPER Admin Panel loaded. Press Ctrl+Shift+A to toggle.', 
      'background:#213d77;color:#fb792b;padding:8px 16px;border-radius:4px;font-weight:bold');
    console.log('%c Changes are saved PERMANENTLY to index.html on disk.', 
      'background:#10b981;color:#fff;padding:4px 12px;border-radius:4px');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
