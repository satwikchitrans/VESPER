const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'index.html');
const jsPath = path.join(__dirname, 'app.js');

const htmlContent = fs.readFileSync(htmlPath, 'utf8');
const jsContent = fs.readFileSync(jsPath, 'utf8');

console.log('Testing GodsEye View components...');

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
  'btn-godseye',
  'btn-godseye-close',
  'ge-alt-leo',
  'ge-alt-tactical',
  'ge-alt-lock',
  'ge-toggle-los',
  'ge-toggle-flir',
  'ge-toggle-interceptions'
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
  console.log(`✓ All ${requiredIds.length} GodsEye DOM IDs exist in index.html!`);
} else {
  console.error(`Total missing: ${missing}`);
  process.exit(1);
}

if (jsContent.includes('buildStaticRadarBuffer') &&
    jsContent.includes('onVehicleGlide') &&
    jsContent.includes('updateInterceptionMatrix') &&
    jsContent.includes('renderTargetChips') &&
    jsContent.includes('setAltitudeMode')) {
  console.log('✓ All high-efficiency GodsEye methods present in app.js!');
} else {
  console.error('Some methods missing in app.js');
  process.exit(1);
}

console.log('ALL GODSEYE VERIFICATION CHECKS PASSED!');
