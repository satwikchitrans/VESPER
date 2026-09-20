const fs = require('fs');
const http = require('http');

console.log('=== TEST: GIS CLOSE BUTTON & MAIN PAGE ALIGNMENT SUITE ===\n');

const html = fs.readFileSync('index.html', 'utf8');
const app = fs.readFileSync('app.js', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');

let failed = 0;

function assert(condition, desc) {
  if (condition) {
    console.log(`✓ ${desc}`);
  } else {
    console.error(`✗ FAIL: ${desc}`);
    failed++;
  }
}

// 1. Close buttons check
assert(html.includes('id="btn-gis-close"'), 'btn-gis-close button exists in index.html');
assert(html.includes('id="btn-surv-close"'), 'btn-surv-close button exists in index.html');
assert(html.includes('id="btn-ps124-close"'), 'btn-ps124-close button exists in index.html');
assert(html.includes('id="btn-dossier-close"'), 'btn-dossier-close button exists in index.html');
assert(html.includes('id="btn-grid-close"'), 'btn-grid-close button exists in index.html');

// 2. JS Handlers check
assert(app.includes('function closeOrCollapseWindow(panel)'), 'closeOrCollapseWindow function defined in app.js');
assert(app.includes('btn-gis-close'), 'btn-gis-close event handler wired in app.js');
assert(app.includes('switchWindow(\'home\')'), 'closeOrCollapseWindow switches to home window');

// 3. Main page contrast & alignment
assert(css.includes('.section-title-large') && css.includes('color: #213d77 !important;'), 'section-title-large styled with IRCTC Navy #213d77 (not white)');
assert(css.includes('.pc-list strong') && css.includes('color: #172b4d !important;'), 'pc-list strong styled with dark color #172b4d (not white)');
assert(css.includes('margin: 20px 32px 0 32px !important;'), 'home-hero aligned with 32px margins');
assert(css.includes('margin: 18px 32px 0 32px !important;'), 'hero-api-banner aligned with 32px margins');
assert(css.includes('padding: 24px 32px 0 32px !important;'), 'home-guide-section aligned with 32px padding');
assert(css.includes('padding: 20px 32px 36px 32px !important;'), 'home-problem-section aligned with 32px padding');

// 4. Hero buttons IRCTC theme
assert(css.includes('#btn-launch-ops') && css.includes('#fb792b'), 'btn-launch-ops has IRCTC Orange');
assert(css.includes('#btn-hero-split-launch') && css.includes('#213d77'), 'btn-hero-split-launch has IRCTC Navy');
assert(css.includes('#btn-demo-stolen-alert') && css.includes('#dc2626'), 'btn-demo-stolen-alert has Emergency Crimson');

// 5. Check no "TO" remaining in guide steps
assert(!html.includes('color:var(--accent-orange)">TO</div>'), '"TO" text removed from guide steps');
assert(html.includes('<span class="gs-action-badge">VIEW</span>'), 'Guide steps have clean VIEW badges');

// 6. Test server status
http.get('http://127.0.0.1:8080/', (res) => {
  assert(res.statusCode === 200, `Local dev server HTTP 200 OK (got ${res.statusCode})`);
  console.log('\n=== ALL ' + (failed === 0 ? 'TESTS PASSED' : failed + ' TESTS FAILED') + ' ===');
  process.exit(failed > 0 ? 1 : 0);
}).on('error', (err) => {
  console.error('✗ FAIL: Server error:', err.message);
  process.exit(1);
});
