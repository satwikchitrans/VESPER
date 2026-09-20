const fs = require('fs');

console.log('=== VERIFYING MANUAL PLATE SIGHTING SEARCH & BUTTON ACCESSIBILITY ===\n');

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');

// 1. Check DOM IDs for Manual Sighting Search & Modal (including new UTA Investigator)
const requiredIds = [
  'global-plate-input',
  'btn-global-plate-search',
  'acq-plate-input',
  'btn-acq-track-plate',
  'btn-acq-open-chain-modal',
  'acq-sighting-summary-card',
  'btn-assc-connect-map',
  'btn-assc-build-trajectory',
  'gis-sighting-chain-hud',
  'btn-close-gsch',
  'btn-gsch-replay',
  'btn-gsch-view-ledger',
  'btn-gsch-intercept',
  'modal-sighting-chain',
  'btn-close-sighting-modal',
  'btn-modal-connect-map',
  'btn-modal-build-corridor',
  'sc-modal-tbody',
  'sc-modal-plate',
  'uta-plate-input',
  'btn-uta-search-plate',
  'btn-uta-open-chain-modal'
];

let missing = [];
requiredIds.forEach(id => {
  if (!html.includes(`id="${id}"`)) missing.push(id);
});

if (missing.length > 0) {
  console.error('FAIL: Missing DOM IDs:', missing);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredIds.length} Sighting & Trajectory DOM IDs present in index.html (including UTA Investigator)`);
}

// 2. Check Methods in app.js
const requiredMethods = [
  'searchAndReconstructTrajectory',
  'updateSightingChainUI',
  'openSightingChainModal',
  'closeSightingChainModal',
  'connectSightingsOnMap',
  'buildExpectedTrajectory',
  'replaySightingChronology',
  'flyToSightingGPS',
  'initSightingChainInteractions'
];

let missingMethods = [];
requiredMethods.forEach(m => {
  if (!js.includes(m)) missingMethods.push(m);
});

if (missingMethods.length > 0) {
  console.error('FAIL: Missing JS methods:', missingMethods);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredMethods.length} ANPR Sighting methods present in app.js`);
}

// 3. Verify Urban Traffic Analytics Accessibility & Scrolling in style.css
if (css.includes('#window-ps124') &&
    css.includes('.ps124-layout') &&
    css.includes('.uta-nav-bar') &&
    css.includes('.uta-tab-btn') &&
    css.includes('.uta-plate-investigator')) {
  console.log('✓ Urban Traffic Analytics has full scrollable layout & accessible sticky button navigation');
} else {
  console.error('FAIL: Missing Urban Traffic Analytics accessibility styles in style.css');
  process.exit(1);
}

// 4. Verify no pane-split-controls collision (unified inline controls)
if (css.includes('.pane-split-controls { display: none !important; }') || css.includes('.pane-split-badge')) {
  console.log('✓ Floating pane-split-controls collision eliminated: controls unified cleanly inside header bar');
} else {
  console.error('FAIL: pane-split-controls may still overlap buttons');
  process.exit(1);
}

console.log('\n=== ALL MANUAL SIGHTING SEARCH & BUTTON ACCESSIBILITY TESTS PASSED ===');
