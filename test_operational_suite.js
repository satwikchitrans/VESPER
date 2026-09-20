const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');

console.log('=== OPERATIONAL SUITE VERIFICATION ===\n');

// 1. Presentation / Pitch artifact audit
const matchesHtml = html.match(/(?:problem[\s_-]*statement|jury|presentation|slide[\s_-]*\d|faq|defense|ps127|feasib)/gi) || [];
const matchesJs = js.match(/(?:problem[\s_-]*statement|jury|presentation|slide[\s_-]*\d|faq|defense|ps127|feasib)/gi) || [];
const matchesCss = css.match(/(?:problem[\s_-]*statement|jury|presentation|slide[\s_-]*\d|faq|defense|ps127|feasib)/gi) || [];

console.log('1. Presentation / Pitch Artifacts:');
console.log(`   - index.html: ${matchesHtml.length} matches`);
console.log(`   - app.js: ${matchesJs.length} matches`);
console.log(`   - style.css: ${matchesCss.length} matches`);

if (matchesHtml.length + matchesJs.length + matchesCss.length > 0) {
  console.error('FAIL: Found lingering presentation artifacts!');
  process.exit(1);
} else {
  console.log('   ✓ 100% PURGED of presentation / PPT / FAQ artifacts\n');
}

// 2. Critical DOM IDs
const criticalIds = [
  'btn-godseye',
  'godseye-overlay',
  'godseye-map',
  'btn-ge-dispatch-intercept',
  'ge-sensor-pip',
  'ge-pip-canvas',
  'btn-ge-pip-close',
  'btn-ge-pip-switch',
  'ge-primary-choke',
  'ge-choke-eta',
  'ge-choke-unit',
  'ge-choke-prob',
  'ge-choke-action',
  'ge-intercept-list',
  'ge-radar-canvas',
  'ge-target-chips',
  'ge-target-plate',
  'ge-target-make',
  'ge-target-color',
  'ge-target-reid',
  'ge-status-text'
];

console.log('2. Tactical DOM IDs Check:');
let missing = [];
criticalIds.forEach(id => {
  if (!html.includes(`id="${id}"`)) {
    missing.push(id);
  }
});

if (missing.length > 0) {
  console.error('FAIL: Missing IDs in index.html:', missing);
  process.exit(1);
} else {
  console.log(`   ✓ All ${criticalIds.length} tactical DOM elements confirmed present\n`);
}

// 3. Operational Logic Methods
const requiredMethods = [
  'authorizeInterception',
  'openSensorPiP',
  'updateInterceptionMatrix',
  'openGodsEye',
  'closeGodsEye',
  'renderTargetChips',
  'startRadarSweep'
];

console.log('3. Operational Logic Methods Check:');
let missingMethods = [];
requiredMethods.forEach(m => {
  if (!js.includes(m)) {
    missingMethods.push(m);
  }
});

if (missingMethods.length > 0) {
  console.error('FAIL: Missing methods in app.js:', missingMethods);
  process.exit(1);
} else {
  console.log(`   ✓ All ${requiredMethods.length} tactical engine methods confirmed present\n`);
}

// 4. Interactivity Check
console.log('4. Interactive Chokepoint Selection Check:');
if (js.includes('GODSEYE.primaryChokePoint = cp') && js.includes('btn-ge-dispatch-intercept')) {
  console.log('   ✓ Interactive chokepoint switching & roadblock dispatch enabled\n');
} else {
  console.error('FAIL: Chokepoint switching logic missing');
  process.exit(1);
}

console.log('=== ALL SUITE CHECKS PASSED SUCCESSFULLY ===');
