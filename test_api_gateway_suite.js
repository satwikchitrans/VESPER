const fs = require('fs');
const http = require('http');

console.log('=== VERIFYING API GATEWAY & MICROSERVICES INTEGRATION ===\n');

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');

// 1. Check API DOM elements in index.html
const requiredIds = [
  'btn-api-modal',
  'nav-api-label',
  'nav-api-lat',
  'modal-api-gateway',
  'btn-close-api',
  'btn-close-api-bottom',
  'gw-stat-apis',
  'gw-stat-lat',
  'gw-stat-stream',
  'btn-ping-all-apis',
  'api-console-endpoint',
  'api-console-status',
  'api-console-time',
  'btn-copy-api-json',
  'api-console-output'
];

let missing = [];
requiredIds.forEach(id => {
  if (!html.includes(`id="${id}"`)) missing.push(id);
});

if (missing.length > 0) {
  console.error('FAIL: Missing DOM IDs:', missing);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredIds.length} API Gateway DOM elements present in index.html`);
}

// 2. Check JavaScript Functions in app.js
const requiredFns = [
  'pingAllAPIServices',
  'executeAPICall',
  'displayAPIConsoleOutput',
  'copyAPIResponse',
  'pollLiveAirspaceAndFleet'
];

let missingFns = [];
requiredFns.forEach(fn => {
  if (!js.includes(fn)) missingFns.push(fn);
});

if (missingFns.length > 0) {
  console.error('FAIL: Missing JS functions:', missingFns);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredFns.length} API Gateway JS methods present in app.js`);
}

// 3. Check CSS classes in style.css
const requiredClasses = [
  '.api-modal-card',
  '.api-stats-bar',
  '.api-services-grid',
  '.api-service-card',
  '.api-console-section',
  '.api-console-output'
];

let missingClasses = [];
requiredClasses.forEach(cls => {
  if (!css.includes(cls)) missingClasses.push(cls);
});

if (missingClasses.length > 0) {
  console.error('FAIL: Missing CSS classes:', missingClasses);
  process.exit(1);
} else {
  console.log(`✓ All ${requiredClasses.length} API Gateway CSS classes present in style.css`);
}

// 4. Test Live Endpoints on Server
const endpoints = [
  '/api/gateway/health',
  '/api/vahan/lookup?plate=DL1CAE4921',
  '/api/cctns/stolen-check?plate=HR51AW4091',
  '/api/traffic/osrm-route',
  '/api/weather/delhi-aqi',
  '/api/flights/opensky-adsb',
  '/api/transit/dtc-fleet',
  '/api/toll/fastag-ledger?plate=DL1CAE4921',
  '/api/forensic/bsa63-verify?plate=DL1CAE4921'
];

let passed = 0;
endpoints.forEach(ep => {
  http.get('http://127.0.0.1:8080' + ep, res => {
    let raw = '';
    res.on('data', chunk => raw += chunk);
    res.on('end', () => {
      if (res.statusCode === 200) {
        console.log(`✓ Endpoint ${ep} => 200 OK (${raw.length} bytes)`);
        passed++;
        if (passed === endpoints.length) {
          console.log('\n=== ALL 8 MICROSERVICE ENDPOINTS & API GATEWAY CHECKS PASSED (100%) ===');
        }
      } else {
        console.error(`FAIL: ${ep} returned ${res.statusCode}`);
        process.exit(1);
      }
    });
  }).on('error', err => {
    console.error(`FAIL: ${ep} request failed: ${err.message}`);
    process.exit(1);
  });
});
