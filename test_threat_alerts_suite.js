const fs = require('fs');

console.log('=== VERIFYING AUTOMATED THREAT ALERTS & BUS CAMERA MESH ===\n');

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');

// 1. Check DOM IDs in index.html
const requiredIds = [
  'nav-alerts',
  'nav-alerts-badge',
  'window-alerts',
  'btn-alerts-close',
  'asr-wanted-count',
  'asr-hits-today',
  'btn-alert-filter-all',
  'btn-alert-filter-stolen',
  'btn-alert-filter-wanted',
  'btn-alert-filter-cloned',
  'btn-alert-filter-bus',
  'btn-trigger-test-wanted',
  'btn-simulate-bus-capture',
  'btn-clear-alerts',
  'threat-alerts-stream',
  'as-bus-list'
];

let missing = [];
requiredIds.forEach(id => {
  if (!html.includes(`id="${id}"`)) missing.push(id);
});

if (missing.length > 0) {
  console.error('FAIL: Missing DOM IDs:', missing);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredIds.length} Threat Alerts & Bus Mesh DOM IDs present in index.html`);
}

// 2. Check JavaScript Methods in app.js
const requiredFns = [
  'initThreatAlertsSystem',
  'registerAutomatedThreatAlert',
  'renderThreatAlertsStream',
  'updateAlertStats',
  'triggerTestWantedVehicle',
  'simulateBusNPUSighting',
  'traceThreatVehicleOnMap'
];

let missingFns = [];
requiredFns.forEach(fn => {
  if (!js.includes(fn)) missingFns.push(fn);
});

if (missingFns.length > 0) {
  console.error('FAIL: Missing JS functions:', missingFns);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredFns.length} Threat Alerts JS methods present in app.js`);
}

// 3. Check CSS rules in style.css
const requiredClasses = [
  '.alerts-panel-layout',
  '.alerts-stats-ribbon',
  '.alerts-toolbar',
  '.threat-alerts-stream',
  '.threat-alert-card',
  '.tac-bad-past-box',
  '.tac-sensor-tag.bus',
  '.as-bus-item'
];

let missingClasses = [];
requiredClasses.forEach(cls => {
  if (!css.includes(cls)) missingClasses.push(cls);
});

if (missingClasses.length > 0) {
  console.error('FAIL: Missing CSS classes:', missingClasses);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredClasses.length} Threat Alerts CSS classes present in style.css`);
}

console.log('\n=== ALL AUTOMATED THREAT ALERTS & BUS CAMERA MESH TESTS PASSED (100%) ===');
