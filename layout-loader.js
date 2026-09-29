/* ═══════════════════════════════════════════════════════════════
   VESPER LIVE LAYOUT RENDERER
   Loads layout customizations from VESPER Studio permanently
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  async function applySavedLayout() {
    try {
      const res = await fetch('/api/layout');
      if (!res.ok) return;
      const data = await res.json();
      
      // If Studio saved modifications exist
      if (data.modifications) {
        Object.entries(data.modifications).forEach(([selector, styles]) => {
          try {
            const el = document.querySelector(selector);
            if (!el) return;
            Object.entries(styles).forEach(([prop, val]) => {
              if (prop === '_innerHTML') el.innerHTML = val;
              else if (prop === '_innerText') el.innerText = val;
              else if (!prop.startsWith('_')) el.style[prop] = val;
            });
          } catch (e) {}
        });
      }
    } catch (err) {
      console.log('Layout loader:', err.message);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applySavedLayout);
  } else {
    applySavedLayout();
  }
})();
