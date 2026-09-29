"""
Refine Executive Dashboard with the authentic Project VESPER Blue & White palette.
Replaces any generic/AI neon or purple tints with clean Royal Navy Blue, crisp high-contrast white text,
and official Indian Government / Tactical accents (Cobalt Blue, Emerald Green, Saffron Amber, Emergency Red).
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace purple badges in index.html with crisp blue / slate
html = html.replace('<span class="dkc-badge purple">16 SENSORS ACTIVE</span>', '<span class="dkc-badge blue">16 SENSORS ACTIVE</span>')
html = html.replace('<div class="dkc-progress-fill purple" style="width: 88%;"></div>', '<div class="dkc-progress-fill blue" style="width: 88%;"></div>')
html = html.replace('<div class="dms-bar-fill purple" style="width: 7.6%;"></div>', '<div class="dms-bar-fill slate" style="width: 7.6%;"></div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html badges.")

# 2. Refine style.css for Dashboard
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the Dashboard CSS block with the clean, authentic Blue & White palette
OLD_MARKER = "/* ============================================================\n   EXECUTIVE TRAFFIC DASHBOARD & ARTERIAL FLOW ANALYTICS\n   ============================================================ */"

REFINED_DASHBOARD_CSS = """/* ============================================================
   EXECUTIVE TRAFFIC DASHBOARD & ARTERIAL FLOW ANALYTICS
   (Authentic Project VESPER Blue & White Command Palette)
   ============================================================ */

.dashboard-layout {
  padding: 16px 22px 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  height: calc(100% - 42px);
  box-sizing: border-box;
  background: #080e1a;
}

/* Hero Operational Header */
.dash-hero-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px 22px;
  background: #0e1a32;
  border: 1px solid #1e3a8a;
  border-left: 4px solid #38bdf8;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}

.dhb-left h2 {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 4px 0;
  letter-spacing: 0.2px;
}

.dhb-left p {
  font-size: 12px;
  color: #94a3b8;
  margin: 0;
  max-width: 700px;
  line-height: 1.5;
}

.dhb-ctrls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.dhb-time-filter {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dhb-label {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.dash-select {
  background: #091122;
  border: 1px solid #1e3a8a;
  color: #38bdf8;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s;
}

.dash-select:hover,
.dash-select:focus {
  border-color: #38bdf8;
}

.dhb-actions {
  display: flex;
  gap: 8px;
}

.dash-btn {
  padding: 7px 14px;
  font-size: 11px;
  font-weight: 800;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.green-wave-btn {
  background: #059669;
  color: #ffffff;
  border: 1px solid #10b981;
}

.green-wave-btn:hover {
  background: #047857;
  border-color: #34d399;
}

.export-btn {
  background: #1e3a8a;
  color: #ffffff;
  border: 1px solid #3b82f6;
}

.export-btn:hover {
  background: #2563eb;
  border-color: #60a5fa;
}

/* --- KPI GRID --- */
.dash-kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
}

@media (max-width: 1200px) {
  .dash-kpi-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .dash-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}

.dash-kpi-card {
  background: #0c1527;
  border: 1px solid #1e293b;
  border-radius: 8px;
  padding: 12px 14px;
  box-sizing: border-box;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.dash-kpi-card:hover {
  border-color: #38bdf8;
  transform: translateY(-2px);
}

.dkc-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dkc-title {
  font-size: 9.5px;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.dkc-badge {
  font-size: 8.5px;
  font-weight: 800;
  padding: 2px 5px;
  border-radius: 3px;
}

.dkc-badge.green { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); }
.dkc-badge.cyan  { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
.dkc-badge.blue  { background: rgba(37, 99, 235, 0.15); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.4); }
.dkc-badge.amber { background: rgba(249, 115, 22, 0.15); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.4); }

.dkc-value {
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
  margin: 6px 0 2px;
  font-family: 'Inter', -apple-system, sans-serif;
}

.dkc-unit {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
}

.dkc-sub {
  font-size: 9.5px;
  color: #64748b;
  margin-bottom: 8px;
}

.dkc-progress-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
}

.dkc-progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease;
}

.dkc-progress-fill.green { background: #10b981; }
.dkc-progress-fill.cyan  { background: #38bdf8; }
.dkc-progress-fill.blue  { background: #2563eb; }
.dkc-progress-fill.amber { background: #f97316; }

/* --- MAIN DASHBOARD GRID --- */
.dash-main-grid {
  display: grid;
  grid-template-columns: 1.15fr 1.25fr 1fr;
  gap: 16px;
}

@media (max-width: 1100px) {
  .dash-main-grid { grid-template-columns: 1fr; }
}

.dash-card {
  background: #0c1527;
  border: 1px solid #1e293b;
  border-radius: 8px;
  padding: 14px 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.dcard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #1e293b;
  padding-bottom: 10px;
}

.dcard-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dcard-icon {
  font-size: 16px;
}

.dcard-title {
  font-size: 13px;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
}

.dcard-sub {
  font-size: 10px;
  color: #94a3b8;
  display: block;
}

.dcard-tag {
  font-size: 9px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 3px;
}
.dcard-tag.cyan { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); }

/* --- CORRIDOR LIST --- */
.corridor-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.corridor-item {
  background: #091122;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.corridor-item:hover {
  background: #0f1c36;
  border-color: #38bdf8;
}

.corridor-item.active {
  background: #0e1e3d;
  border-color: #38bdf8;
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
}

.ci-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.ci-title-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ci-id-tag {
  font-size: 9px;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 3px;
  background: #1e3a8a;
  color: #ffffff;
  border: 1px solid #3b82f6;
}

.ci-name {
  font-size: 11px;
  font-weight: 700;
  color: #ffffff;
}

.ci-los-badge {
  font-size: 9px;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 3px;
}

.los-a { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
.los-b { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #38bdf8; }
.los-c { background: rgba(249, 115, 22, 0.2); color: #f97316; border: 1px solid #f97316; }
.los-d { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }

.ci-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
  font-size: 10px;
  margin-bottom: 6px;
}

.ci-stat-col span { color: #94a3b8; margin-right: 3px; }
.ci-stat-col strong { color: #ffffff; }

.ci-bottleneck {
  font-size: 9.5px;
  color: #cbd5e1;
  display: flex;
  align-items: center;
  gap: 4px;
  padding-top: 4px;
  border-top: 1px solid #1e293b;
}

.ci-bn-icon { font-size: 10px; }

/* --- SELECTED CORRIDOR CARD --- */
.selected-corridor-card {
  background: #091122;
  border: 1px solid #1e3a8a;
  border-radius: 6px;
  padding: 10px 12px;
}

.scc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.scc-title {
  font-size: 10.5px;
  font-weight: 800;
  color: #38bdf8;
  letter-spacing: 0.3px;
}

.scc-badge.online {
  font-size: 8.5px;
  font-weight: 800;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  padding: 1px 5px;
  border-radius: 3px;
  border: 1px solid #10b981;
}

.scc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  font-size: 10px;
}

.scc-item { display: flex; flex-direction: column; gap: 2px; }
.scc-lbl { color: #94a3b8; font-size: 9px; font-weight: 700; }
.scc-item strong { color: #ffffff; }

/* --- TRAFFIC VELOCITY CHART --- */
.chart-horizon-group {
  display: flex;
  gap: 4px;
}

.ch-btn {
  background: #091122;
  border: 1px solid #1e293b;
  color: #94a3b8;
  font-size: 9.5px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s;
}

.ch-btn:hover {
  border-color: #38bdf8;
  color: #ffffff;
}

.ch-btn.active {
  background: #1e3a8a;
  color: #ffffff;
  border-color: #3b82f6;
}

.dash-chart-wrapper {
  background: #080e1a;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 8px;
  position: relative;
  display: flex;
  justify-content: center;
}

.dash-chart-wrapper canvas {
  width: 100%;
  height: 200px;
  display: block;
}

.dash-chart-legend {
  display: flex;
  justify-content: center;
  gap: 16px;
  font-size: 9.5px;
  color: #94a3b8;
  flex-wrap: wrap;
}

.dcl-item { display: flex; align-items: center; gap: 5px; }
.dcl-color { width: 8px; height: 8px; border-radius: 2px; display: inline-block; }
.dcl-color.blue  { background: #2563eb; }
.dcl-color.cyan  { background: #38bdf8; }
.dcl-color.amber { background: #f97316; }

/* --- MODAL SPLIT BARS --- */
.dash-modal-split-box {
  background: #091122;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 10px 12px;
}

.dms-title {
  font-size: 9.5px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 0.4px;
  margin-bottom: 8px;
}

.dms-bars {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dms-bar-row {
  display: grid;
  grid-template-columns: 200px 1fr 45px;
  align-items: center;
  gap: 8px;
  font-size: 9.5px;
}

.dms-label { color: #cbd5e1; }

.dms-bar-track {
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  overflow: hidden;
}

.dms-bar-fill { height: 100%; border-radius: 3px; }
.dms-bar-fill.blue   { background: #2563eb; }
.dms-bar-fill.green  { background: #10b981; }
.dms-bar-fill.amber  { background: #f97316; }
.dms-bar-fill.slate  { background: #64748b; }

.dms-pct { color: #ffffff; font-weight: 700; text-align: right; }

/* --- SIGNALS & PREDICTION --- */
.mini-action-btn {
  background: #091122;
  border: 1px solid #1e3a8a;
  color: #38bdf8;
  font-size: 9.5px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
}

.mini-action-btn:hover {
  background: #1e3a8a;
  color: #ffffff;
  border-color: #38bdf8;
}

.dash-signals-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ds-item {
  background: #091122;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 8px 10px;
}

.ds-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.ds-junction {
  font-size: 10.5px;
  font-weight: 700;
  color: #ffffff;
}

.ds-badge {
  font-size: 9px;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 3px;
}

.ds-badge.green { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
.ds-badge.amber { background: rgba(249, 115, 22, 0.2); color: #f97316; border: 1px solid #f97316; }

.ds-meta {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: #94a3b8;
}

.ds-meta span.green { color: #10b981; }
.ds-meta span.amber { color: #f97316; }

/* --- PREDICTIVE HORIZON BOX --- */
.dash-predictive-box {
  background: #091122;
  border: 1px solid #1e3a8a;
  border-left: 3px solid #38bdf8;
  border-radius: 6px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dpb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dpb-title {
  font-size: 10px;
  font-weight: 900;
  color: #38bdf8;
  letter-spacing: 0.5px;
}

.dpb-horizon-toggles {
  display: flex;
  gap: 3px;
}

.dh-btn {
  background: #0c1527;
  border: 1px solid #1e293b;
  color: #94a3b8;
  font-size: 9px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s;
}

.dh-btn:hover {
  color: #ffffff;
  border-color: #38bdf8;
}

.dh-btn.active {
  background: #1e3a8a;
  color: #ffffff;
  border-color: #3b82f6;
}

.dpb-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 10px;
}

.dpb-stat-row {
  display: flex;
  justify-content: space-between;
  color: #94a3b8;
}

.dpb-stat-row strong.green { color: #10b981; }
.dpb-stat-row strong.cyan  { color: #38bdf8; }
.dpb-stat-row strong.amber { color: #f97316; }

.dpb-advisory {
  background: #0c1527;
  border-left: 2px solid #38bdf8;
  padding: 6px 8px;
  border-radius: 0 4px 4px 0;
  font-size: 9.5px;
  color: #cbd5e1;
  line-height: 1.4;
  margin-top: 4px;
}

.dpb-actions {
  margin-top: 4px;
}

.dpb-btn-broadcast {
  width: 100%;
  background: #1e3a8a;
  border: 1px solid #3b82f6;
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dpb-btn-broadcast:hover {
  background: #2563eb;
  border-color: #60a5fa;
}
"""

if OLD_MARKER in css:
    css_parts = css.split(OLD_MARKER)
    new_css = css_parts[0] + REFINED_DASHBOARD_CSS
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(new_css)
    print("Replaced style.css dashboard block with refined Blue & White palette.")
else:
    css += '\n' + REFINED_DASHBOARD_CSS
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended refined Blue & White dashboard styles to style.css.")

# 3. Refine canvas drawing in app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Make canvas lines clean Royal / Sky Blue and Saffron instead of generic colors
app_js = app_js.replace("grad.addColorStop(0, 'rgba(59, 130, 246, 0.6)');", "grad.addColorStop(0, 'rgba(37, 99, 235, 0.7)');")
app_js = app_js.replace("ctx.strokeStyle = '#00f0ff';", "ctx.strokeStyle = '#38bdf8';")
app_js = app_js.replace("ctx.shadowColor = 'rgba(0, 240, 255, 0.6)';", "ctx.shadowColor = 'rgba(56, 189, 248, 0.4)';")
app_js = app_js.replace("ctx.fillStyle = '#00f0ff';", "ctx.fillStyle = '#38bdf8';")
app_js = app_js.replace("ctx.strokeStyle = 'rgba(245, 158, 11, 0.6)';", "ctx.strokeStyle = 'rgba(249, 115, 22, 0.7)';")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Updated app.js canvas styling.")
print("DONE: Color palette refinement complete.")
