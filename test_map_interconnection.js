const fs = require('fs');

console.log('=== TEST: MAP & DETAILS INTERCONNECTION SUITE ===\n');

const html = fs.readFileSync('index.html', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');

function assert(condition, message) {
  if (condition) {
    console.log(`✓ ${message}`);
  } else {
    console.error(`✗ FAIL: ${message}`);
    process.exitCode = 1;
  }
}

// 1. Check HTML Elements for Sighting Inspector
assert(html.includes('id="gis-sighting-inspector"'), 'gis-sighting-inspector exists in index.html');
assert(html.includes('id="gsi-sighting-badge"'), 'gsi-sighting-badge exists in index.html');
assert(html.includes('id="gsi-sensor-pill"'), 'gsi-sensor-pill exists in index.html');
assert(html.includes('id="gsi-plate-text"'), 'gsi-plate-text exists in index.html');
assert(html.includes('id="gsi-char-chips"'), 'gsi-char-chips exists in index.html');
assert(html.includes('id="gsi-snapshot-canvas"'), 'gsi-snapshot-canvas exists in index.html');
assert(html.includes('id="btn-close-gsi"'), 'btn-close-gsi exists in index.html');
assert(html.includes('id="btn-gsi-copy-gps"'), 'btn-gsi-copy-gps exists in index.html');
assert(html.includes('id="btn-gsi-focus-feed"'), 'btn-gsi-focus-feed exists in index.html');
assert(html.includes('id="btn-gsi-pcr-intercept"'), 'btn-gsi-pcr-intercept exists in index.html');
assert(html.includes('id="btn-gsi-dossier"'), 'btn-gsi-dossier exists in index.html');

// 2. Check CSS classes
assert(css.includes('.gis-sighting-inspector'), '.gis-sighting-inspector defined in style.css');
assert(css.includes('.gsi-char-chip'), '.gsi-char-chip defined in style.css');
assert(css.includes('.gsi-preview-telemetry-row'), '.gsi-preview-telemetry-row defined in style.css');
assert(css.includes('.gsi-handoff-strip'), '.gsi-handoff-strip defined in style.css');

// 3. Check JavaScript Functions and Handlers
assert(js.includes('function openSightingInspector('), 'openSightingInspector function defined in app.js');
assert(js.includes('function renderSightingSnapshot('), 'renderSightingSnapshot function defined in app.js');
assert(js.includes('function closeSightingInspector('), 'closeSightingInspector function defined in app.js');
assert(js.includes('function simulatePCRIntercept('), 'simulatePCRIntercept function defined in app.js');
assert(js.includes("document.getElementById('btn-close-gsi')"), 'btn-close-gsi handler registered in app.js');
assert(js.includes("document.getElementById('btn-gsi-pcr-intercept')"), 'btn-gsi-pcr-intercept handler registered in app.js');
assert(js.includes('openSightingInspector(veh, stepIndex);'), 'openSightingInspector called in activateTimelineStep');

console.log('\n=== ALL INTERCONNECTION TESTS PASSED ===');
