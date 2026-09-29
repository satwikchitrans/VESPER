"""
Update Project VESPER so that:
1. The Executive Traffic Dashboard is the HERO / LANDING window (primary default page & first tab).
2. The Dashboard and entire interface adopt the official IRCTC color palette:
   - Deep Royal Navy (#213d77 / #1b3569)
   - Saffron Orange (#fb792b / #ea580c)
   - Clean Off-White & Crisp Slate (#f4f6f9 / #ffffff / #172b4d)
3. Canvas chart renders dynamically with IRCTC theme colors.
"""
import re

# =========================================================================
# 1. UPDATE index.html
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make nav-dashboard the first tab and active
html = re.sub(r'<button class="nav-tab[^>]*id="nav-dashboard"[^>]*>[\s\S]*?</button>', '', html)
html = re.sub(r'<button class="nav-tab active" data-window="gis" id="nav-gis">', '<button class="nav-tab" data-window="gis" id="nav-gis">', html)

first_nav_tab = '''      <button class="nav-tab active" data-window="dashboard" id="nav-dashboard">
        <span class="nav-icon">📈</span>
        <span class="nav-label">Executive Dashboard</span>
      </button>'''

html = re.sub(r'(<div class="nav-tabs-group">\s*)', r'\1' + first_nav_tab + '\n', html)

# Ensure window-gis is not active and window-dashboard is active
html = re.sub(r'<section class="window-panel active" id="window-gis"', '<section class="window-panel" id="window-gis"', html)
html = re.sub(r'<section class="window-panel" id="window-dashboard"', '<section class="window-panel active" id="window-dashboard"', html)

# Move window-dashboard to top of <main id="windows-container"> (after gutters)
# Extract window-dashboard section
dash_match = re.search(r'(<!-- ═══════════════════════════════════════════════════════════════════ -->\s*<!-- WINDOW: EXECUTIVE TRAFFIC DASHBOARD[\s\S]*?</section>)', html)
if dash_match:
    dash_content = dash_match.group(1)
    # Remove it from current location
    html = html.replace(dash_content, '')
    # Insert right after split-gutter-h
    gutter_target = '<div id="split-gutter-h" class="split-gutter horizontal" title="Drag vertically to resize Surveillance / PS124 window height"></div>'
    html = html.replace(gutter_target, gutter_target + '\n\n  ' + dash_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html: Executive Dashboard is now the primary Hero landing page & first tab.")


# =========================================================================
# 2. UPDATE style.css WITH IRCTC THEME OVERRIDES FOR DASHBOARD
# =========================================================================
IRCTC_DASHBOARD_CSS = """
/* ============================================================
   IRCTC PALETTE OVERRIDES FOR EXECUTIVE TRAFFIC DASHBOARD
   Official Indian Railways Royal Navy (#213d77) & Saffron (#fb792b)
   ============================================================ */

.theme-gov .dashboard-layout {
  background: #f4f6f9;
  color: #172b4d;
}

.theme-gov .dash-hero-banner {
  background: linear-gradient(135deg, #213d77 0%, #182e57 100%);
  border: 2px solid #fb792b;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(33, 61, 119, 0.22);
}

.theme-gov .dhb-left h2 {
  color: #ffffff;
  font-weight: 900;
  letter-spacing: 0.4px;
}

.theme-gov .dhb-left p {
  color: #e2e8f0;
}

.theme-gov .dhb-label {
  color: #cbd5e1;
}

.theme-gov .dash-select {
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  color: #213d77;
  font-weight: 800;
}

.theme-gov .green-wave-btn {
  background: linear-gradient(135deg, #fb792b 0%, #ea580c 100%);
  border: 1px solid #f97316;
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(251, 121, 43, 0.35);
}

.theme-gov .green-wave-btn:hover {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  box-shadow: 0 4px 14px rgba(251, 121, 43, 0.5);
}

.theme-gov .export-btn {
  background: #ffffff;
  border: 1.5px solid #213d77;
  color: #213d77;
  font-weight: 800;
}

.theme-gov .export-btn:hover {
  background: #e8f0fe;
  color: #1b3569;
}

/* --- KPI CARDS (IRCTC WHITE ELEVATED WITH NAVY & SAFFRON ACCENTS) --- */
.theme-gov .dash-kpi-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-top: 3px solid #213d77;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(33, 61, 119, 0.08);
}

.theme-gov .dash-kpi-card:hover {
  border-top-color: #fb792b;
  box-shadow: 0 4px 14px rgba(33, 61, 119, 0.16);
}

.theme-gov .dkc-title {
  color: #5e6e82;
  font-weight: 800;
}

.theme-gov .dkc-value {
  color: #213d77;
  font-weight: 900;
}

.theme-gov .dkc-unit {
  color: #64748b;
}

.theme-gov .dkc-sub {
  color: #64748b;
}

.theme-gov .dkc-progress-bar {
  background: #e2e8f0;
}

.theme-gov .dkc-badge.green  { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.theme-gov .dkc-badge.cyan   { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
.theme-gov .dkc-badge.purple { background: #f5f3ff; color: #5b21b6; border: 1px solid #ddd6fe; }
.theme-gov .dkc-badge.amber  { background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; }

/* --- MAIN DASHBOARD CARDS --- */
.theme-gov .dash-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 3px 12px rgba(33, 61, 119, 0.08);
}

.theme-gov .dcard-header {
  border-bottom: 1.5px solid #edf2f7;
}

.theme-gov .dcard-title {
  color: #213d77;
  font-weight: 800;
}

.theme-gov .dcard-sub {
  color: #64748b;
}

.theme-gov .dcard-tag.cyan {
  background: #eff6ff;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}

/* --- CORRIDOR LIST --- */
.theme-gov .corridor-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.theme-gov .corridor-item:hover {
  background: #f1f5f9;
  border-color: #213d77;
}

.theme-gov .corridor-item.active {
  background: #f0f7ff;
  border: 2px solid #213d77;
  box-shadow: 0 2px 10px rgba(33, 61, 119, 0.12);
}

.theme-gov .ci-id-tag {
  background: #213d77;
  color: #ffffff;
  border: none;
}

.theme-gov .ci-name {
  color: #172b4d;
  font-weight: 800;
}

.theme-gov .ci-stat-col span {
  color: #64748b;
}

.theme-gov .ci-stat-col strong {
  color: #213d77;
  font-weight: 800;
}

.theme-gov .ci-bottleneck {
  color: #475569;
  border-top: 1px solid #edf2f7;
}

.theme-gov .selected-corridor-card {
  background: #f0f7ff;
  border: 1.5px solid #213d77;
}

.theme-gov .scc-title {
  color: #213d77;
  font-weight: 900;
}

.theme-gov .scc-lbl {
  color: #5e6e82;
}

.theme-gov .scc-item strong {
  color: #172b4d;
}

/* --- CANVAS CHART IN IRCTC THEME --- */
.theme-gov .ch-btn {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #475569;
}

.theme-gov .ch-btn.active {
  background: #213d77;
  color: #ffffff;
  border-color: #213d77;
}

.theme-gov .dash-chart-wrapper {
  background: #ffffff;
  border: 1px solid #e2e8f0;
}

.theme-gov .dash-chart-legend {
  color: #475569;
}

.theme-gov .dcl-color.blue  { background: #213d77; }
.theme-gov .dcl-color.cyan  { background: #fb792b; }
.theme-gov .dcl-color.amber { background: #dc2626; }

.theme-gov .dash-modal-split-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.theme-gov .dms-title {
  color: #213d77;
  font-weight: 800;
}

.theme-gov .dms-label {
  color: #334155;
  font-weight: 700;
}

.theme-gov .dms-bar-track {
  background: #e2e8f0;
}

.theme-gov .dms-pct {
  color: #213d77;
  font-weight: 800;
}

.theme-gov .dms-bar-fill.blue   { background: #213d77; }
.theme-gov .dms-bar-fill.green  { background: #10b981; }
.theme-gov .dms-bar-fill.amber  { background: #fb792b; }
.theme-gov .dms-bar-fill.purple { background: #8b5cf6; }

/* --- SIGNALS & PREDICTION IN IRCTC THEME --- */
.theme-gov .mini-action-btn {
  background: #eff6ff;
  border: 1px solid #213d77;
  color: #213d77;
}

.theme-gov .mini-action-btn:hover {
  background: #213d77;
  color: #ffffff;
}

.theme-gov .ds-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.theme-gov .ds-junction {
  color: #172b4d;
  font-weight: 800;
}

.theme-gov .ds-meta {
  color: #64748b;
}

.theme-gov .dash-predictive-box {
  background: #fffaf5;
  border: 1.5px solid #fb792b;
}

.theme-gov .dpb-title {
  color: #c2410c;
  font-weight: 900;
}

.theme-gov .dh-btn {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #475569;
}

.theme-gov .dh-btn.active {
  background: #fb792b;
  color: #ffffff;
  border-color: #fb792b;
}

.theme-gov .dpb-stat-row {
  color: #475569;
}

.theme-gov .dpb-stat-row strong.green { color: #059669; }
.theme-gov .dpb-stat-row strong.cyan  { color: #213d77; }
.theme-gov .dpb-stat-row strong.amber { color: #c2410c; }

.theme-gov .dpb-advisory {
  background: #ffffff;
  border-left: 3px solid #fb792b;
  border: 1px solid #fed7aa;
  border-left-width: 3px;
  color: #334155;
}

.theme-gov .dpb-btn-broadcast {
  background: linear-gradient(135deg, #213d77 0%, #182e57 100%);
  color: #ffffff;
  border: 1px solid #213d77;
}

.theme-gov .dpb-btn-broadcast:hover {
  background: linear-gradient(135deg, #182e57 0%, #0f172a 100%);
}
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'IRCTC PALETTE OVERRIDES FOR EXECUTIVE TRAFFIC DASHBOARD' not in css:
    css += '\n' + IRCTC_DASHBOARD_CSS
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended IRCTC theme overrides to style.css.")


# =========================================================================
# 3. UPDATE app.js FOR DEFAULT HERO DASHBOARD & IRCTC CANVAS DRAWING
# =========================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Make STATE.activeWindow default to 'dashboard'
app_js = re.sub(r"activeWindow:\s*'[^']+'", "activeWindow: 'dashboard'", app_js)

# Update renderDashboardTrafficChart to support IRCTC theme
NEW_CHART_FUNC = """function renderDashboardTrafficChart() {
  const canvas = document.getElementById('dash-traffic-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const isGov = document.body.classList.contains('theme-gov');

  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  // Background Fill for Theme
  if (isGov) {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, w, h);
  }

  // Background Grid Lines
  ctx.strokeStyle = isGov ? 'rgba(33, 61, 119, 0.1)' : 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 1;
  const rows = 5;
  for (let r = 0; r <= rows; r++) {
    const y = 20 + (r / rows) * (h - 50);
    ctx.beginPath();
    ctx.moveTo(35, y);
    ctx.lineTo(w - 15, y);
    ctx.stroke();

    // Axis Labels (Speed km/h)
    ctx.fillStyle = isGov ? '#5e6e82' : '#64748b';
    ctx.font = 'bold 9px Inter, sans-serif';
    ctx.textAlign = 'right';
    const val = 60 - r * 10;
    ctx.fillText(val + 'k', 30, y + 3);
  }

  // Hours Labels
  const hours = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'];
  const colW = (w - 50) / (hours.length - 1);
  for (let i = 0; i < hours.length; i++) {
    const x = 35 + i * colW;
    ctx.fillStyle = isGov ? '#5e6e82' : '#64748b';
    ctx.font = 'bold 9px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(hours[i], x, h - 8);
  }

  // Volume Bar Chart (Royal Navy Bars in Gov mode, Blue in Tactical mode)
  const volumeData = [32, 24, 78, 54, 88, 65, 36];
  const barW = 18;
  for (let i = 0; i < volumeData.length; i++) {
    const x = 35 + i * colW - barW / 2;
    const barH = (volumeData[i] / 100) * (h - 60);
    const y = h - 25 - barH;

    const grad = ctx.createLinearGradient(0, y, 0, h - 25);
    if (isGov) {
      grad.addColorStop(0, 'rgba(33, 61, 119, 0.85)');
      grad.addColorStop(1, 'rgba(33, 61, 119, 0.25)');
    } else {
      grad.addColorStop(0, 'rgba(59, 130, 246, 0.6)');
      grad.addColorStop(1, 'rgba(59, 130, 246, 0.1)');
    }

    ctx.fillStyle = grad;
    ctx.fillRect(x, y, barW, barH);
    ctx.strokeStyle = isGov ? '#213d77' : 'rgba(59, 130, 246, 0.8)';
    ctx.strokeRect(x, y, barW, barH);
  }

  // Average Velocity Curve (IRCTC Saffron #fb792b in Gov mode, Cyan #00f0ff in Tactical mode)
  const speedData = [52, 54, 28, 38, 26, 34, 48];
  ctx.beginPath();
  for (let i = 0; i < speedData.length; i++) {
    const x = 35 + i * colW;
    const y = 20 + ((60 - speedData[i]) / 50) * (h - 50);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = isGov ? '#fb792b' : '#00f0ff';
  ctx.lineWidth = isGov ? 3 : 2.5;
  ctx.shadowColor = isGov ? 'rgba(251, 121, 43, 0.4)' : 'rgba(0, 240, 255, 0.6)';
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.shadowBlur = 0; // reset

  // Dots on Speed Curve
  for (let i = 0; i < speedData.length; i++) {
    const x = 35 + i * colW;
    const y = 20 + ((60 - speedData[i]) / 50) * (h - 50);
    ctx.fillStyle = isGov ? '#ffffff' : '#0b111e';
    ctx.beginPath();
    ctx.arc(x, y, 4.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = isGov ? '#fb792b' : '#00f0ff';
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  // Congestion Threshold Line (Crimson Dashed)
  const threshY = 20 + ((60 - 30) / 50) * (h - 50);
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = isGov ? 'rgba(220, 38, 38, 0.7)' : 'rgba(245, 158, 11, 0.6)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(35, threshY);
  ctx.lineTo(w - 15, threshY);
  ctx.stroke();
  ctx.setLineDash([]); // reset
}"""

# Replace old renderDashboardTrafficChart
app_js = re.sub(r'function renderDashboardTrafficChart\(\)\s*\{[\s\S]*?ctx\.setLineDash\(\[\]\);\s*// reset\s*\}', NEW_CHART_FUNC, app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print("Updated app.js with IRCTC canvas chart renderer & default hero state.")
"""
"""
