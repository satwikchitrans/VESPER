const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'index.html');
const jsPath = path.join(__dirname, 'app.js');

const htmlContent = fs.readFileSync(htmlPath, 'utf8');
const jsContent = fs.readFileSync(jsPath, 'utf8');

console.log('Testing GodsEye 1.0 OSINT View components...');

const requiredIds = [
  'ge-clock',
  'ge-target-plate',
  'ge-target-make',
  'ge-target-color',
  'ge-target-reid',
  'ge-target-status',
  'ge-target-threat',
  'ge-target-corridor',
  'ge-target-mapmatch',
  'ge-primary-choke',
  'ge-choke-eta',
  'ge-choke-unit',
  'ge-choke-prob',
  'ge-choke-action',
  'ge-altitude',
  'ge-swath',
  'ge-gsd',
  'ge-render-fps',
  'ge-fixed-count',
  'ge-mobile-count',
  'ge-coverage',
  'ge-active-node',
  'ge-los-status',
  'ge-intercept-list',
  'ge-mini-feed',
  'ge-speed',
  'ge-heading',
  'ge-lat',
  'ge-lng',
  'ge-road-name',
  'ge-eta',
  'ge-dist',
  'ge-sightings',
  'ge-conf',
  'ge-los-node',
  'ge-reticle-label',
  'ge-status-text',
  'ge-target-chips',
  'ge-radar-canvas',
  'ge-map-container',
  'godseye-overlay',
  'btn-topbar-godseye',
  'btn-godseye-close',
  'ge-alt-leo',
  'ge-alt-tactical',
  'ge-alt-lock',
  'ge-toggle-adsb',
  'ge-toggle-satellites',
  'ge-toggle-airspace',
  'ge-toggle-los',
  'ge-toggle-interceptions',
  'ge-toggle-aqi',
  'ge-vm-default',
  'ge-vm-nvg',
  'ge-vm-flir',
  'ge-vm-crt',
  'ge-vm-god',
  'ge-osint-inspector',
  'ge-oi-type',
  'ge-oi-id',
  'btn-ge-oi-close',
  'ge-oi-desc',
  'ge-oi-alt',
  'ge-oi-speed',
  'ge-oi-hdg',
  'ge-oi-squawk',
  'ge-oi-lat',
  'ge-oi-lng',
  'ge-oi-payload',
  'ge-oi-status',
  'btn-ge-oi-focus',
  'btn-ge-oi-stream'
];

let missing = 0;
requiredIds.forEach(id => {
  const regex = new RegExp(`id=["']${id}["']`);
  if (!regex.test(htmlContent)) {
    console.error(`MISSING ID in index.html: ${id}`);
    missing++;
  }
});

if (missing === 0) {
  console.log(`✓ All ${requiredIds.length} GodsEye OSINT DOM IDs exist in index.html!`);
} else {
  console.error(`Total missing: ${missing}`);
  process.exit(1);
}

const requiredMethods = [
  'buildStaticRadarBuffer',
  'onVehicleGlide',
  'updateInterceptionMatrix',
  'renderTargetChips',
  'setAltitudeMode',
  'setVisualMode',
  'openInspector'
];

let methodsMissing = 0;
requiredMethods.forEach(method => {
  if (!jsContent.includes(method)) {
    console.error(`MISSING METHOD in app.js: ${method}`);
    methodsMissing++;
  }
});

if (methodsMissing === 0) {
  console.log(`✓ All ${requiredMethods.length} GodsEye OSINT methods present in app.js!`);
} else {
  console.error('Some methods missing in app.js');
  process.exit(1);
}

// Check OSINT datasets
if (jsContent.includes('OSINT_AIRCRAFT') &&
    jsContent.includes('OSINT_SATELLITES') &&
    jsContent.includes('OSINT_AIRSPACE') &&
    jsContent.includes('OSINT_AQI')) {
  console.log('✓ All 4 Godseye 1.0 OSINT datasets defined in app.js!');
} else {
  console.error('OSINT datasets missing in app.js');
  process.exit(1);
}

console.log('ALL GODSEYE 1.0 OSINT INTEGRATION CHECKS PASSED!');

