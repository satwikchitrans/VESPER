"""
Inject CSS styles and JavaScript logic for the Executive Dashboard
into style.css and app.js.
"""
import re

# =========================================================================
# 1. APPEND CSS TO style.css
# =========================================================================
DASHBOARD_CSS = """
/* ============================================================
   EXECUTIVE TRAFFIC DASHBOARD & ARTERIAL FLOW ANALYTICS
   ============================================================ */

.dashboard-layout {
  padding: 16px 20px 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  height: calc(100% - 42px);
  box-sizing: border-box;
}

.dash-hero-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px 20px;
  background: linear-gradient(135deg, rgba(13, 22, 42, 0.95), rgba(8, 14, 28, 0.98));
  border: 1px solid rgba(0, 240, 255, 0.25);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.dhb-left h2 {
  font-size: 17px;
  font-weight: 800;
  color: #f8fafc;
  margin: 0 0 4px 0;
  letter-spacing: 0.3px;
}

.dhb-left p {
  font-size: 11.5px;
  color: #94a3b8;
  margin: 0;
  max-width: 680px;
  line-height: 1.45;
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
  color: #64748b;
  letter-spacing: 0.5px;
}

.dash-select {
  background: #0d1527;
  border: 1px solid rgba(0, 240, 255, 0.35);
  color: #38bdf8;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  outline: none;
  cursor: pointer;
}

.dhb-actions {
  display: flex;
  gap: 8px;
}

.dash-btn {
  padding: 6px 12px;
  font-size: 10.5px;
  font-weight: 800;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.green-wave-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #ffffff;
  border: 1px solid #34d399;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.35);
}

.green-wave-btn:hover {
  background: linear-gradient(135deg, #059669, #047857);
  box-shadow: 0 0 16px rgba(16, 185, 129, 0.55);
}

.export-btn {
  background: rgba(30, 41, 59, 0.85);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
}

.export-btn:hover {
  background: rgba(30, 41, 59, 1);
  border-color: #38bdf8;
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
  background: rgba(13, 21, 39, 0.88);
  border: 1px solid rgba(0, 240, 255, 0.18);
  border-radius: 8px;
  padding: 12px 14px;
  box-sizing: border-box;
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.dash-kpi-card:hover {
  border-color: rgba(0, 240, 255, 0.45);
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

.dkc-badge.green { background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid #10b981; }
.dkc-badge.cyan  { background: rgba(6, 182, 212, 0.18); color: #22d3ee; border: 1px solid #06b6d4; }
.dkc-badge.purple{ background: rgba(168, 85, 247, 0.18); color: #c084fc; border: 1px solid #a855f7; }
.dkc-badge.amber { background: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid #f59e0b; }

.dkc-value {
  font-size: 22px;
  font-weight: 900;
  color: #f8fafc;
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
.dkc-progress-fill.cyan  { background: #06b6d4; }
.dkc-progress-fill.purple{ background: #a855f7; }
.dkc-progress-fill.amber { background: #f59e0b; }

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
  background: rgba(11, 18, 34, 0.92);
  border: 1px solid rgba(0, 240, 255, 0.18);
  border-radius: 8px;
  padding: 14px 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.dcard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
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
  color: #f8fafc;
  margin: 0;
}

.dcard-sub {
  font-size: 9.5px;
  color: #64748b;
  display: block;
}

.dcard-tag {
  font-size: 9px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 3px;
}
.dcard-tag.cyan { background: rgba(0, 240, 255, 0.12); color: #00f0ff; border: 1px solid rgba(0, 240, 255, 0.3); }

/* --- CORRIDOR LIST --- */
.corridor-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.corridor-item {
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 9px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.corridor-item:hover {
  background: rgba(15, 23, 42, 0.95);
  border-color: rgba(0, 240, 255, 0.4);
}

.corridor-item.active {
  background: rgba(0, 240, 255, 0.06);
  border-color: #00f0ff;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.12);
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
  padding: 1px 5px;
  border-radius: 3px;
  background: #1e293b;
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.ci-name {
  font-size: 11px;
  font-weight: 700;
  color: #e2e8f0;
}

.ci-los-badge {
  font-size: 9px;
  font-weight: 900;
  padding: 1px 6px;
  border-radius: 3px;
}

.los-a { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
.los-b { background: rgba(6, 182, 212, 0.2); color: #22d3ee; border: 1px solid #06b6d4; }
.los-c { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
.los-d { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }

.ci-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
  font-size: 10px;
  margin-bottom: 6px;
}

.ci-stat-col span { color: #64748b; margin-right: 3px; }
.ci-stat-col strong { color: #f1f5f9; }

.ci-bottleneck {
  font-size: 9.5px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
  padding-top: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.ci-bn-icon { font-size: 10px; }

/* --- SELECTED CORRIDOR CARD --- */
.selected-corridor-card {
  background: rgba(13, 22, 42, 0.95);
  border: 1px solid rgba(0, 240, 255, 0.3);
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
  color: #00f0ff;
  letter-spacing: 0.4px;
}

.scc-badge.online {
  font-size: 8.5px;
  font-weight: 800;
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
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
.scc-lbl { color: #64748b; font-size: 9px; font-weight: 700; }
.scc-item strong { color: #e2e8f0; }

/* --- TRAFFIC VELOCITY CHART --- */
.chart-horizon-group {
  display: flex;
  gap: 4px;
}

.ch-btn {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  font-size: 9.5px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 3px;
  cursor: pointer;
}

.ch-btn.active {
  background: #00f0ff;
  color: #0b111e;
  border-color: #00f0ff;
}

.dash-chart-wrapper {
  background: #080c16;
  border: 1px solid rgba(0, 240, 255, 0.12);
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
.dcl-color.blue  { background: #3b82f6; }
.dcl-color.cyan  { background: #00f0ff; }
.dcl-color.amber { background: #f59e0b; }

/* --- MODAL SPLIT BARS --- */
.dash-modal-split-box {
  background: rgba(13, 21, 39, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 6px;
  padding: 10px 12px;
}

.dms-title {
  font-size: 9.5px;
  font-weight: 800;
  color: #94a3b8;
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
.dms-bar-fill.blue   { background: #3b82f6; }
.dms-bar-fill.green  { background: #10b981; }
.dms-bar-fill.amber  { background: #f59e0b; }
.dms-bar-fill.purple { background: #a855f7; }

.dms-pct { color: #f8fafc; font-weight: 700; text-align: right; }

/* --- SIGNALS & PREDICTION --- */
.mini-action-btn {
  background: #1e293b;
  border: 1px solid rgba(0, 240, 255, 0.3);
  color: #00f0ff;
  font-size: 9.5px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 3px;
  cursor: pointer;
}

.mini-action-btn:hover {
  background: #00f0ff;
  color: #0b111e;
}

.dash-signals-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ds-item {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.06);
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
  color: #e2e8f0;
}

.ds-badge {
  font-size: 9px;
  font-weight: 900;
  padding: 1px 6px;
  border-radius: 3px;
}

.ds-badge.green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
.ds-badge.amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }

.ds-meta {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: #64748b;
}

.ds-meta span.green { color: #34d399; }
.ds-meta span.amber { color: #fbbf24; }

/* --- PREDICTIVE HORIZON BOX --- */
.dash-predictive-box {
  background: rgba(13, 22, 42, 0.95);
  border: 1px solid rgba(168, 85, 247, 0.3);
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
  color: #c084fc;
  letter-spacing: 0.5px;
}

.dpb-horizon-toggles {
  display: flex;
  gap: 3px;
}

.dh-btn {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  font-size: 9px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 3px;
  cursor: pointer;
}

.dh-btn.active {
  background: #a855f7;
  color: #ffffff;
  border-color: #a855f7;
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

.dpb-stat-row strong.green { color: #34d399; }
.dpb-stat-row strong.cyan  { color: #38bdf8; }
.dpb-stat-row strong.amber { color: #fbbf24; }

.dpb-advisory {
  background: rgba(15, 23, 42, 0.8);
  border-left: 2px solid #a855f7;
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
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(126, 34, 206, 0.3));
  border: 1px solid rgba(168, 85, 247, 0.5);
  color: #e9d5ff;
  font-size: 10px;
  font-weight: 800;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dpb-btn-broadcast:hover {
  background: rgba(168, 85, 247, 0.4);
  color: #ffffff;
}
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.dashboard-layout' not in css:
    css += '\n' + DASHBOARD_CSS
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended Dashboard CSS to style.css.")
else:
    print("Dashboard CSS already present in style.css.")


# =========================================================================
# 2. APPEND DASHBOARD JS ENGINE TO app.js
# =========================================================================
DASHBOARD_JS = """
// ============================================================
// EXECUTIVE TRAFFIC DASHBOARD & ARTERIAL FLOW ENGINE
// ============================================================

const DASHBOARD_DATA = {
  currentRegime: 'normal',
  selectedCorridor: 'c1',
  chartMode: '24h',
  predictHorizon: 15,
  corridors: {
    c1: {
      name: 'Karol Bagh ↔ CP ↔ ITO ↔ Pragati Maidan',
      vol: '4,120 veh/h',
      speed: '34 km/h',
      los: 'LOS B',
      losClass: 'los-b',
      cong: '22%',
      sync: '94%',
      capacity: '5,200 veh/hr (V/C: 0.79)',
      density: '38.4 vehicles / km',
      travelTime: '14.2 min (Baseline: 12.0 min)',
      transitTSP: 'Route 419 Bus TSP Active (14.6 FPS)',
      bottleneck: 'ITO Junction Westbound · Delay: +2.1m'
    },
    c2: {
      name: 'AIIMS Flyover ↔ Ring Road ↔ Moolchand ↔ Nehru Place',
      vol: '5,680 veh/h',
      speed: '42 km/h',
      los: 'LOS C',
      losClass: 'los-c',
      cong: '36%',
      sync: '91%',
      capacity: '6,400 veh/hr (V/C: 0.88)',
      density: '48.2 vehicles / km',
      travelTime: '18.5 min (Baseline: 14.5 min)',
      transitTSP: 'Route 522 Bus TSP Active (14.8 FPS)',
      bottleneck: 'Lajpat Nagar Ring Road Merge · Delay: +3.8m'
    },
    c3: {
      name: 'Dhaula Kuan ↔ Sardar Patel Marg ↔ India Gate',
      vol: '3,450 veh/h',
      speed: '48 km/h',
      los: 'LOS A',
      losClass: 'los-a',
      cong: '14%',
      sync: '98%',
      capacity: '5,000 veh/hr (V/C: 0.69)',
      density: '24.1 vehicles / km',
      travelTime: '11.0 min (Baseline: 10.5 min)',
      transitTSP: 'Route 764 Bus TSP Active (15.0 FPS)',
      bottleneck: 'Express Flow · Optimal Transit Green Wave'
    },
    c4: {
      name: 'Connaught Place ↔ India Gate ↔ AIIMS ↔ Saket',
      vol: '4,890 veh/h',
      speed: '31 km/h',
      los: 'LOS C',
      losClass: 'los-c',
      cong: '41%',
      sync: '88%',
      capacity: '5,500 veh/hr (V/C: 0.89)',
      density: '52.6 vehicles / km',
      travelTime: '21.4 min (Baseline: 16.0 min)',
      transitTSP: 'Route 335 Express TSP Active (14.2 FPS)',
      bottleneck: 'Aurobindo Marg Influx · Delay: +4.5m'
    }
  },
  predictions: {
    15: {
      speed: '38.6 km/h (▲ +1.2 km/h)',
      prob: '18% (Low Risk)',
      choke: 'Lajpat Nagar Merge (34%)',
      advisory: 'Maintain current green wave on C-01 & C-03. Route 522 bus mobile ANPR units will monitor Ring Road inflow.'
    },
    30: {
      speed: '36.2 km/h (▼ -1.2 km/h)',
      prob: '28% (Moderate Influx)',
      choke: 'ITO Junction / Vikas Marg (46%)',
      advisory: 'Prepare 8s cycle extension on North-South signal corridor at 16:30. DTC Bus headway normal.'
    },
    60: {
      speed: '32.8 km/h (▼ -4.6 km/h)',
      prob: '54% (Peak Hour Build-up)',
      choke: 'Connaught Place Outer Circle (62%)',
      advisory: 'Recommend automated detour advisory for commercial logistics to Ring Road Expressway.'
    }
  }
};

function initDashboard() {
  renderDashboardTrafficChart();
  updateDashboardMetrics();
}

function selectDashboardCorridor(corridorId) {
  DASHBOARD_DATA.selectedCorridor = corridorId;
  playSound('click');

  document.querySelectorAll('.corridor-item').forEach(el => el.classList.remove('active'));
  const activeEl = document.getElementById(`ci-${corridorId}`);
  if (activeEl) activeEl.classList.add('active');

  const c = DASHBOARD_DATA.corridors[corridorId];
  if (!c) return;

  const sccTitle = document.getElementById('scc-title');
  if (sccTitle) sccTitle.textContent = `${corridorId.toUpperCase()}: ${c.name.toUpperCase()}`;

  const sccCap = document.getElementById('scc-capacity');
  if (sccCap) sccCap.textContent = c.capacity;

  const sccDens = document.getElementById('scc-density');
  if (sccDens) sccDens.textContent = c.density;

  const sccTT = document.getElementById('scc-tt');
  if (sccTT) sccTT.textContent = c.travelTime;

  const sccTransit = document.getElementById('scc-transit');
  if (sccTransit) sccTransit.textContent = c.transitTSP;
}

function onDashboardRegimeChange(regimeKey) {
  DASHBOARD_DATA.currentRegime = regimeKey;
  playSound('click');

  const flowEl = document.getElementById('dash-kpi-flow');
  const speedEl = document.getElementById('dash-kpi-speed');
  const congEl = document.getElementById('dash-kpi-congestion');
  const badgeEl = document.getElementById('dash-flow-badge');

  if (regimeKey === 'am_peak') {
    if (flowEl) flowEl.textContent = '178,400';
    if (speedEl) speedEl.innerHTML = '29.2 <span class="dkc-unit">km/h</span>';
    if (congEl) congEl.textContent = '44.6%';
    if (badgeEl) { badgeEl.textContent = '▲ PEAK AM INFLUX'; badgeEl.className = 'dkc-badge amber'; }
  } else if (regimeKey === 'pm_peak') {
    if (flowEl) flowEl.textContent = '192,650';
    if (speedEl) speedEl.innerHTML = '27.4 <span class="dkc-unit">km/h</span>';
    if (congEl) congEl.textContent = '52.1%';
    if (badgeEl) { badgeEl.textContent = '▲ PEAK PM COMMUTE'; badgeEl.className = 'dkc-badge amber'; }
  } else if (regimeKey === 'night') {
    if (flowEl) flowEl.textContent = '42,100';
    if (speedEl) speedEl.innerHTML = '54.8 <span class="dkc-unit">km/h</span>';
    if (congEl) congEl.textContent = '8.2%';
    if (badgeEl) { badgeEl.textContent = '▼ FREE FLOW'; badgeEl.className = 'dkc-badge green'; }
  } else {
    if (flowEl) flowEl.textContent = '142,850';
    if (speedEl) speedEl.innerHTML = '37.4 <span class="dkc-unit">km/h</span>';
    if (congEl) congEl.textContent = '24.8%';
    if (badgeEl) { badgeEl.textContent = '+4.8% NORMAL'; badgeEl.className = 'dkc-badge green'; }
  }

  renderDashboardTrafficChart();
  showToast('TRAFFIC REGIME UPDATED', `Flow models recalibrated for ${regimeKey.toUpperCase().replace('_', ' ')}.`, 'cyan');
}

function setDashboardChartMode(mode) {
  DASHBOARD_DATA.chartMode = mode;
  playSound('click');

  document.querySelectorAll('.ch-btn').forEach(b => b.classList.remove('active'));
  const activeBtn = document.getElementById(`btn-horizon-${mode}`);
  if (activeBtn) activeBtn.classList.add('active');

  renderDashboardTrafficChart();
}

function setDashboardPredictHorizon(mins) {
  DASHBOARD_DATA.predictHorizon = mins;
  playSound('click');

  document.querySelectorAll('.dpb-horizon-toggles .dh-btn').forEach(b => b.classList.remove('active'));
  const activeBtn = document.getElementById(`btn-pred-${mins}`);
  if (activeBtn) activeBtn.classList.add('active');

  const p = DASHBOARD_DATA.predictions[mins];
  if (!p) return;

  const spdEl = document.getElementById('pred-speed');
  if (spdEl) spdEl.textContent = p.speed;

  const probEl = document.getElementById('pred-prob');
  if (probEl) probEl.textContent = p.prob;

  const chokeEl = document.getElementById('pred-choke');
  if (chokeEl) chokeEl.textContent = p.choke;

  const advEl = document.getElementById('dpb-advisory');
  if (advEl) advEl.innerHTML = `<span>💡 Advisory: <strong>${p.advisory}</strong></span>`;
}

function triggerGreenCorridorWave() {
  playSound('beep');
  showToast('GREEN WAVE SYNCHRONIZED', 'Corridor 1 (Karol Bagh - CP - ITO) & Corridor 3 signals aligned for 90s priority pulse.', 'green');

  const sigIto = document.getElementById('sig-ito');
  if (sigIto) {
    sigIto.textContent = 'GREEN: 85s (WAVE)';
    sigIto.className = 'ds-badge green';
  }
  const sigCp = document.getElementById('sig-cp');
  if (sigCp) {
    sigCp.textContent = 'GREEN: 65s (WAVE)';
    sigCp.className = 'ds-badge green';
  }
}

function recalculateSignalSplits() {
  playSound('click');
  showToast('AI ADAPTIVE SIGNAL OPTIMIZER', 'Induction loops & bus NPU density recalculated. Cycle efficiency: 98.4%.', 'cyan');
}

function broadcastCongestionAdvisory() {
  playSound('alert');
  showToast('BROADCAST DISPATCHED', 'Arterial speed advisory published to Delhi Police Traffic & DTC Transit Mesh.', 'amber');
}

function resetDashboardView() {
  selectDashboardCorridor('c1');
  const sel = document.getElementById('dash-time-regime');
  if (sel) { sel.value = 'normal'; onDashboardRegimeChange('normal'); }
  setDashboardPredictHorizon(15);
}

function exportDashboardTrafficJson() {
  playSound('click');
  const payload = {
    timestamp: new Date().toISOString(),
    system: "Project VESPER Executive Traffic Engine",
    jurisdiction: "Delhi Police Traffic Management & DTC Mobile Mesh",
    metrics: {
      totalFleetFlowVehHr: 142850,
      avgCorridorVelocityKmh: 37.4,
      citywideCongestionPct: 24.8,
      levelOfService: "LOS B",
      anprScansPerMin: 3840,
      adaptiveSignalInterventionsPerHour: 128,
      dailyCarbonOffsetTonnes: 2.42
    },
    corridors: DASHBOARD_DATA.corridors,
    predictions: DASHBOARD_DATA.predictions
  };

  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(payload, null, 2));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", `VESPER_Traffic_Analysis_${Date.now()}.json`);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();

  showToast('TRAFFIC AUDIT EXPORTED', 'Municipal Traffic Analysis JSON downloaded successfully.', 'green');
}

function renderDashboardTrafficChart() {
  const canvas = document.getElementById('dash-traffic-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  // Background Grid Lines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 1;
  const rows = 5;
  for (let r = 0; r <= rows; r++) {
    const y = 20 + (r / rows) * (h - 50);
    ctx.beginPath();
    ctx.moveTo(35, y);
    ctx.lineTo(w - 15, y);
    ctx.stroke();

    // Axis Labels (Speed km/h)
    ctx.fillStyle = '#64748b';
    ctx.font = '9px Inter, monospace';
    ctx.textAlign = 'right';
    const val = 60 - r * 10;
    ctx.fillText(val + 'k', 30, y + 3);
  }

  // Hours Labels
  const hours = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'];
  const colW = (w - 50) / (hours.length - 1);
  for (let i = 0; i < hours.length; i++) {
    const x = 35 + i * colW;
    ctx.fillStyle = '#64748b';
    ctx.font = '9px Inter, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(hours[i], x, h - 8);
  }

  // Volume Bar Chart (Blue Bars)
  const volumeData = [32, 24, 78, 54, 88, 65, 36];
  const barW = 18;
  for (let i = 0; i < volumeData.length; i++) {
    const x = 35 + i * colW - barW / 2;
    const barH = (volumeData[i] / 100) * (h - 60);
    const y = h - 25 - barH;

    const grad = ctx.createLinearGradient(0, y, 0, h - 25);
    grad.addColorStop(0, 'rgba(59, 130, 246, 0.6)');
    grad.addColorStop(1, 'rgba(59, 130, 246, 0.1)');

    ctx.fillStyle = grad;
    ctx.fillRect(x, y, barW, barH);
    ctx.strokeStyle = 'rgba(59, 130, 246, 0.8)';
    ctx.strokeRect(x, y, barW, barH);
  }

  // Average Velocity Curve (Cyan Line)
  const speedData = [52, 54, 28, 38, 26, 34, 48];
  ctx.beginPath();
  for (let i = 0; i < speedData.length; i++) {
    const x = 35 + i * colW;
    const y = 20 + ((60 - speedData[i]) / 50) * (h - 50);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = '#00f0ff';
  ctx.lineWidth = 2.5;
  ctx.shadowColor = 'rgba(0, 240, 255, 0.6)';
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.shadowBlur = 0; // reset

  // Dots on Speed Curve
  for (let i = 0; i < speedData.length; i++) {
    const x = 35 + i * colW;
    const y = 20 + ((60 - speedData[i]) / 50) * (h - 50);
    ctx.fillStyle = '#0b111e';
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#00f0ff';
    ctx.beginPath();
    ctx.arc(x, y, 2.5, 0, Math.PI * 2);
    ctx.fill();
  }

  // Congestion Threshold Line (Amber Dashed)
  const threshY = 20 + ((60 - 30) / 50) * (h - 50);
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.6)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(35, threshY);
  ctx.lineTo(w - 15, threshY);
  ctx.stroke();
  ctx.setLineDash([]); // reset
}

function updateDashboardMetrics() {
  // Live subtle fluctuation simulator for realism
  const flowEl = document.getElementById('dash-kpi-flow');
  if (flowEl && DASHBOARD_DATA.currentRegime === 'normal') {
    const base = 142850;
    const noise = Math.floor(Math.sin(Date.now() / 3000) * 120);
    flowEl.textContent = (base + noise).toLocaleString();
  }
}
"""

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Hook into switchWindow
if 'windowId === "dashboard"' not in app_js and "windowId === 'dashboard'" not in app_js:
    app_js = app_js.replace("if (windowId === 'surveillance' && !STATE.mapsInitialized.surv)",
                            "if (windowId === 'dashboard') { initDashboard(); }\n    if (windowId === 'surveillance' && !STATE.mapsInitialized.surv)")

# Hook into init
if 'initDashboard();' not in app_js:
    app_js = app_js.replace("window.addEventListener('DOMContentLoaded', () => {",
                            "window.addEventListener('DOMContentLoaded', () => {\n  initDashboard();")

if 'const DASHBOARD_DATA' not in app_js:
    app_js += '\n' + DASHBOARD_JS
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    print("Appended Dashboard JS to app.js.")
else:
    print("Dashboard JS already present in app.js.")

print("DONE: Dashboard integration complete.")
