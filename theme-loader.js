/**
 * VESPER Dynamic Theme Engine & Visual Inspector Bridge
 * 1. Automatically loads saved custom box backgrounds, surface colors, text colors,
 *    font scaling, and element-specific overrides from localStorage.
 * 2. Provides visual click-to-select inspector support when commanded by theme-admin.html.
 */
(function() {
  'use strict';

  var THEME_STYLE_ID = 'vesper-live-custom-theme';
  var ELEMENT_OVERRIDES_STYLE_ID = 'vesper-element-overrides-style';
  var STORAGE_KEY = 'vesper_custom_theme_css';
  var OVERRIDES_KEY = 'vesper_element_overrides';

  function applyCustomTheme(cssText) {
    if (!cssText) return;
    var styleEl = document.getElementById(THEME_STYLE_ID);
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = THEME_STYLE_ID;
      document.head.appendChild(styleEl);
    }
    styleEl.textContent = cssText;
  }

  function applyElementOverrides(overridesCss) {
    var styleEl = document.getElementById(ELEMENT_OVERRIDES_STYLE_ID);
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = ELEMENT_OVERRIDES_STYLE_ID;
      document.head.appendChild(styleEl);
    }
    styleEl.textContent = overridesCss || '';
  }

  // 1. Initial Load from LocalStorage
  function loadSavedTheme() {
    try {
      var savedCss = localStorage.getItem(STORAGE_KEY);
      if (savedCss) applyCustomTheme(savedCss);

      var savedOverrides = localStorage.getItem(OVERRIDES_KEY);
      if (savedOverrides) applyElementOverrides(savedOverrides);
    } catch (e) {
      console.warn('[ThemeLoader] LocalStorage access error:', e);
    }
  }

  loadSavedTheme();
  // Ensure styles are also applied once DOM is fully ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadSavedTheme);
  }

  // 2. Cross-tab & BroadcastChannel Synchronization
  try {
    if (typeof BroadcastChannel !== 'undefined') {
      var channel = new BroadcastChannel('vesper_theme_sync_channel');
      channel.onmessage = function(event) {
        if (!event.data) return;
        if (event.data.type === 'APPLY_THEME') {
          applyCustomTheme(event.data.css);
          if (typeof event.data.overrides === 'string') {
            applyElementOverrides(event.data.overrides);
          }
        } else if (event.data.type === 'RESET_THEME') {
          var styleEl1 = document.getElementById(THEME_STYLE_ID);
          if (styleEl1) styleEl1.textContent = '';
          var styleEl2 = document.getElementById(ELEMENT_OVERRIDES_STYLE_ID);
          if (styleEl2) styleEl2.textContent = '';
        }
      };
    }
  } catch (e) {}

  // 3. Visual Element Inspector Overlay State
  var inspectorActive = false;
  var hoverOverlay = null;
  var selectedOverlay = null;
  var currentHoveredEl = null;

  function createOverlay(className, borderColor, bgColor) {
    var el = document.createElement('div');
    el.className = className;
    el.style.position = 'fixed';
    el.style.pointerEvents = 'none';
    el.style.zIndex = '999999';
    el.style.border = '2px solid ' + borderColor;
    el.style.background = bgColor;
    el.style.borderRadius = '4px';
    el.style.transition = 'all 0.08s ease';
    el.style.display = 'none';

    var label = document.createElement('div');
    label.className = 'inspector-label';
    label.style.position = 'absolute';
    label.style.top = '-22px';
    label.style.left = '0';
    label.style.background = borderColor;
    label.style.color = '#ffffff';
    label.style.fontFamily = 'monospace';
    label.style.fontSize = '10px';
    label.style.fontWeight = 'bold';
    label.style.padding = '2px 6px';
    label.style.borderRadius = '3px';
    label.style.whiteSpace = 'nowrap';
    el.appendChild(label);

    document.body.appendChild(el);
    return el;
  }

  function getUniqueSelector(el) {
    if (!el || el === document.body || el === document.documentElement) return 'body';
    if (el.id) return '#' + el.id;

    var path = [];
    while (el && el.nodeType === Node.ELEMENT_NODE && el !== document.body) {
      var selector = el.nodeName.toLowerCase();
      if (el.id) {
        selector = '#' + el.id;
        path.unshift(selector);
        break;
      } else {
        var cleanClasses = Array.from(el.classList).filter(function(c) {
          return !c.startsWith('inspector-');
        });
        if (cleanClasses.length > 0) {
          selector += '.' + cleanClasses.slice(0, 2).join('.');
        }
        var sibling = el;
        var nth = 1;
        while (sibling = sibling.previousElementSibling) {
          if (sibling.nodeName.toLowerCase() === el.nodeName.toLowerCase()) nth++;
        }
        if (nth > 1) selector += ':nth-of-type(' + nth + ')';
      }
      path.unshift(selector);
      el = el.parentElement;
    }
    return path.join(' > ');
  }

  function rgbToHex(rgbStr) {
    if (!rgbStr || rgbStr === 'transparent' || rgbStr === 'rgba(0, 0, 0, 0)') return '';
    var match = rgbStr.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    if (!match) return rgbStr;
    function hex(x) {
      return ('0' + parseInt(x, 10).toString(16)).slice(-2);
    }
    return '#' + hex(match[1]) + hex(match[2]) + hex(match[3]);
  }

  function positionOverlay(overlay, targetEl, text) {
    if (!targetEl || !overlay) return;
    var rect = targetEl.getBoundingClientRect();
    overlay.style.top = rect.top + 'px';
    overlay.style.left = rect.left + 'px';
    overlay.style.width = rect.width + 'px';
    overlay.style.height = rect.height + 'px';
    overlay.style.display = 'block';
    var label = overlay.querySelector('.inspector-label');
    if (label && text) label.textContent = text;
  }

  function onMouseMove(e) {
    if (!inspectorActive) return;
    var target = document.elementFromPoint(e.clientX, e.clientY);
    if (!target || target === document.body || target === document.documentElement || target.classList.contains('inspector-overlay')) {
      if (hoverOverlay) hoverOverlay.style.display = 'none';
      return;
    }
    currentHoveredEl = target;
    if (!hoverOverlay) {
      hoverOverlay = createOverlay('inspector-overlay hover', '#38bdf8', 'rgba(56, 189, 248, 0.15)');
    }
    var tag = target.tagName.toLowerCase();
    var idStr = target.id ? '#' + target.id : '';
    var classStr = target.classList.length > 0 ? '.' + Array.from(target.classList).slice(0, 2).join('.') : '';
    positionOverlay(hoverOverlay, target, tag + idStr + classStr);
  }

  function onClick(e) {
    if (!inspectorActive) return;
    e.preventDefault();
    e.stopPropagation();

    var target = document.elementFromPoint(e.clientX, e.clientY);
    if (!target || target === document.body || target.classList.contains('inspector-overlay')) return;

    if (!selectedOverlay) {
      selectedOverlay = createOverlay('inspector-overlay selected', '#fb792b', 'rgba(251, 121, 43, 0.25)');
    }
    var tag = target.tagName.toLowerCase();
    var idStr = target.id ? '#' + target.id : '';
    var classStr = target.classList.length > 0 ? '.' + Array.from(target.classList).slice(0, 2).join('.') : '';
    positionOverlay(selectedOverlay, target, 'SELECTED: ' + tag + idStr + classStr);

    var computed = window.getComputedStyle(target);
    var selector = getUniqueSelector(target);
    var primaryClass = target.classList.length > 0 ? Array.from(target.classList)[0] : '';
    var snippet = (target.innerText || target.textContent || '').trim().substring(0, 40);

    var fontSize = computed.fontSize ? parseInt(computed.fontSize, 10) : 14;
    var fontWeight = computed.fontWeight || '400';

    var payload = {
      type: 'ELEMENT_SELECTED',
      selector: selector,
      tagName: tag,
      id: target.id || '',
      classes: Array.from(target.classList),
      primaryClass: primaryClass,
      textSnippet: snippet,
      currentBg: rgbToHex(computed.backgroundColor) || '#ffffff',
      currentColor: rgbToHex(computed.color) || '#0f172a',
      currentBorder: rgbToHex(computed.borderColor) || '#cbd5e1',
      currentFontSize: fontSize,
      currentFontWeight: fontWeight
    };

    if (window.parent && window.parent !== window) {
      window.parent.postMessage(payload, '*');
    }
  }

  function setInspectorMode(enable) {
    inspectorActive = enable;
    if (enable) {
      document.addEventListener('mousemove', onMouseMove, true);
      document.addEventListener('click', onClick, true);
      document.body.style.cursor = 'crosshair';
    } else {
      document.removeEventListener('mousemove', onMouseMove, true);
      document.removeEventListener('click', onClick, true);
      document.body.style.cursor = 'default';
      if (hoverOverlay) hoverOverlay.style.display = 'none';
      if (selectedOverlay) selectedOverlay.style.display = 'none';
    }
  }

  // 4. Window Message Listener
  window.addEventListener('message', function(event) {
    if (!event.data) return;
    if (event.data.type === 'VESPER_THEME_UPDATE') {
      applyCustomTheme(event.data.css);
      if (typeof event.data.overrides === 'string') {
        applyElementOverrides(event.data.overrides);
      }
    } else if (event.data.type === 'VESPER_THEME_RESET') {
      var styleEl1 = document.getElementById(THEME_STYLE_ID);
      if (styleEl1) styleEl1.textContent = '';
      var styleEl2 = document.getElementById(ELEMENT_OVERRIDES_STYLE_ID);
      if (styleEl2) styleEl2.textContent = '';
    } else if (event.data.type === 'TOGGLE_INSPECTOR') {
      setInspectorMode(!!event.data.enabled);
    }
  });

  // 5. Storage Event Listener
  window.addEventListener('storage', function(event) {
    if (event.key === STORAGE_KEY) {
      applyCustomTheme(event.newValue || '');
    } else if (event.key === OVERRIDES_KEY) {
      applyElementOverrides(event.newValue || '');
    }
  });
})();
