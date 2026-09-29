"""
Inject Executive Traffic Dashboard & Deep Traffic Analysis Suite
into Project VESPER (index.html, style.css, app.js).
"""
import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add nav tab if not present
if 'id="nav-dashboard"' not in html:
    nav_tab_html = '''      <button class="nav-tab" data-window="dashboard" id="nav-dashboard">
        <span class="nav-icon">📈</span>
        <span class="nav-label">Executive Dashboard</span>
      </button>'''
    # Insert after nav-gis
    html = re.sub(r'(<button class="nav-tab[^>]*id="nav-gis"[^>]*>[\s\S]*?</button>)', r'\1\n' + nav_tab_html, html)

# Add window-dashboard section
if 'id="window-dashboard"' not in html:
    dashboard_section = '''
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- WINDOW: EXECUTIVE TRAFFIC DASHBOARD & DEEP ARTERIAL ANALYTICS     -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <section class="window-panel" id="window-dashboard" data-pane="dashboard">
      <div class="window-folder-header">
        <div class="wfh-title-group">
          <span class="wfh-title">VESPER // EXECUTIVE COMMAND DASHBOARD &amp; DEEP TRAFFIC ANALYSIS</span>
          <span class="wfh-tag green">LIVE SENSING MESH ONLINE</span>
        </div>
        <div class="wfh-controls">
          <button class="wfh-btn btn-win-reset" onclick="resetDashboardView()" title="Reset Dashboard Telemetry">Reset</button>
          <button class="wfh-btn btn-win-maximize" title="Maximize Window">MAX</button>
          <button class="wfh-btn btn-win-close" id="btn-dashboard-close" onclick="closeOrCollapseWindow('dashboard')" title="Close Window (Esc)">CLOSE</button>
        </div>
      </div>

      <div class="dashboard-layout">
        <!-- Hero Header & Global Operational Filter Bar -->
        <div class="dash-hero-banner">
          <div class="dhb-left">
            <h2>Metropolitan Traffic Flow &amp; Real-Time Arterial Analytics</h2>
            <p>Unified telemetry stream fusing <strong>12 Fixed ANPR Junctions</strong>, <strong>4 DTC Mobile Edge NPU Buses</strong>, and <strong>Municipal Induction Sensors</strong> for automated corridor optimization.</p>
          </div>
          <div class="dhb-ctrls">
            <div class="dhb-time-filter">
              <span class="dhb-label">FLOW REGIME:</span>
              <select id="dash-time-regime" class="dash-select" onchange="onDashboardRegimeChange(this.value)">
                <option value="am_peak">Morning Peak (08:00 - 11:00)</option>
                <option value="normal" selected>Normal Midday (11:00 - 16:00)</option>
                <option value="pm_peak">Evening Peak (16:00 - 21:00)</option>
                <option value="night">Night Clearance (21:00 - 06:00)</option>
              </select>
            </div>
            <div class="dhb-actions">
              <button class="dash-btn green-wave-btn" id="btn-dash-greenwave" onclick="triggerGreenCorridorWave()">
                <span>⚡ TRIGGER GREEN WAVE</span>
              </button>
              <button class="dash-btn export-btn" id="btn-dash-export-json" onclick="exportDashboardTrafficJson()">
                <span>📥 EXPORT AUDIT JSON</span>
              </button>
            </div>
          </div>
        </div>

        <!-- KPI Strip: 6 Strategic Municipal Metrics -->
        <div class="dash-kpi-grid">
          <div class="dash-kpi-card" id="kpi-card-flow">
            <div class="dkc-top">
              <span class="dkc-title">TOTAL FLEET FLOW</span>
              <span class="dkc-badge green" id="dash-flow-badge">+4.8% NORMAL</span>
            </div>
            <div class="dkc-value" id="dash-kpi-flow">142,850</div>
            <div class="dkc-sub">Vehicles / Hour · Urban Perimeter</div>
            <div class="dkc-progress-bar"><div class="dkc-progress-fill green" style="width: 78%;"></div></div>
          </div>

          <div class="dash-kpi-card" id="kpi-card-speed">
            <div class="dkc-top">
              <span class="dkc-title">AVG CORRIDOR SPEED</span>
              <span class="dkc-badge cyan" id="dash-speed-badge">TARGET: 35 KM/H</span>
            </div>
            <div class="dkc-value" id="dash-kpi-speed">37.4 <span class="dkc-unit">km/h</span></div>
            <div class="dkc-sub">Range: 28 - 54 km/h across corridors</div>
            <div class="dkc-progress-bar"><div class="dkc-progress-fill cyan" style="width: 74%;"></div></div>
          </div>

          <div class="dash-kpi-card" id="kpi-card-congestion">
            <div class="dkc-top">
              <span class="dkc-title">CONGESTION INDEX</span>
              <span class="dkc-badge green" id="dash-cong-badge">LOS B · OPTIMAL</span>
            </div>
            <div class="dkc-value" id="dash-kpi-congestion">24.8%</div>
            <div class="dkc-sub">Citywide Delay Factor: 1.18x free-flow</div>
            <div class="dkc-progress-bar"><div class="dkc-progress-fill green" style="width: 25%;"></div></div>
          </div>

          <div class="dash-kpi-card" id="kpi-card-anpr">
            <div class="dkc-top">
              <span class="dkc-title">ANPR SCAN RATE</span>
              <span class="dkc-badge purple">16 SENSORS ACTIVE</span>
            </div>
            <div class="dkc-value" id="dash-kpi-anpr">3,840 <span class="dkc-unit">/min</span></div>
            <div class="dkc-sub">99.4% OCR Confidence · NTP Synced</div>
            <div class="dkc-progress-bar"><div class="dkc-progress-fill purple" style="width: 88%;"></div></div>
          </div>

          <div class="dash-kpi-card" id="kpi-card-signals">
            <div class="dkc-top">
              <span class="dkc-title">AI SIGNAL SPLITS</span>
              <span class="dkc-badge amber">ADAPTIVE SYNC</span>
            </div>
            <div class="dkc-value" id="dash-kpi-signals">128 <span class="dkc-unit">/ hr</span></div>
            <div class="dkc-sub">Dynamic Green-Wave Interventions</div>
            <div class="dkc-progress-bar"><div class="dkc-progress-fill amber" style="width: 65%;"></div></div>
          </div>

          <div class="dash-kpi-card" id="kpi-card-carbon">
            <div class="dkc-top">
              <span class="dkc-title">EMISSION OFFSET</span>
              <span class="dkc-badge green">-18.4% CO₂</span>
            </div>
            <div class="dkc-value" id="dash-kpi-carbon">2.42 <span class="dkc-unit">t/day</span></div>
            <div class="dkc-sub">Anti-Idling Signal Synchronization</div>
            <div class="dkc-progress-bar"><div class="dkc-progress-fill green" style="width: 82%;"></div></div>
          </div>
        </div>

        <!-- Main Dashboard Content Grid: 3 Analytical Columns -->
        <div class="dash-main-grid">
          <!-- Column 1: Corridor-by-Corridor Deep Flow Matrix -->
          <div class="dash-card corridor-matrix-card">
            <div class="dcard-header">
              <div class="dcard-title-group">
                <span class="dcard-icon">🛣️</span>
                <div>
                  <h3 class="dcard-title">Arterial Corridor Flow &amp; Level-of-Service</h3>
                  <span class="dcard-sub">Click any corridor to inspect real-time capacity and bottlenecks</span>
                </div>
              </div>
              <span class="dcard-tag cyan">4 ARTERIES</span>
            </div>
            
            <div class="corridor-list" id="dash-corridor-list">
              <!-- Corridor 1 -->
              <div class="corridor-item active" id="ci-c1" onclick="selectDashboardCorridor('c1')">
                <div class="ci-header">
                  <div class="ci-title-wrap">
                    <span class="ci-id-tag c1">C-01</span>
                    <span class="ci-name">Karol Bagh ↔ CP ↔ ITO ↔ Pragati Maidan</span>
                  </div>
                  <span class="ci-los-badge los-b" id="c1-los">LOS B</span>
                </div>
                <div class="ci-stats">
                  <div class="ci-stat-col"><span>Flow:</span><strong id="c1-vol">4,120 veh/h</strong></div>
                  <div class="ci-stat-col"><span>Avg Speed:</span><strong id="c1-spd">34 km/h</strong></div>
                  <div class="ci-stat-col"><span>Congestion:</span><strong id="c1-cong">22%</strong></div>
                  <div class="ci-stat-col"><span>Sync:</span><strong class="green" id="c1-sync">94%</strong></div>
                </div>
                <div class="ci-bottleneck">
                  <span class="ci-bn-icon">⚠️</span>
                  <span>Bottleneck: <strong>ITO Junction Westbound</strong> · Delay: +2.1m</span>
                </div>
              </div>

              <!-- Corridor 2 -->
              <div class="corridor-item" id="ci-c2" onclick="selectDashboardCorridor('c2')">
                <div class="ci-header">
                  <div class="ci-title-wrap">
                    <span class="ci-id-tag c2">C-02</span>
                    <span class="ci-name">AIIMS Flyover ↔ Ring Road ↔ Moolchand ↔ Nehru Place</span>
                  </div>
                  <span class="ci-los-badge los-c" id="c2-los">LOS C</span>
                </div>
                <div class="ci-stats">
                  <div class="ci-stat-col"><span>Flow:</span><strong id="c2-vol">5,680 veh/h</strong></div>
                  <div class="ci-stat-col"><span>Avg Speed:</span><strong id="c2-spd">42 km/h</strong></div>
                  <div class="ci-stat-col"><span>Congestion:</span><strong id="c2-cong">36%</strong></div>
                  <div class="ci-stat-col"><span>Sync:</span><strong class="green" id="c2-sync">91%</strong></div>
                </div>
                <div class="ci-bottleneck">
                  <span class="ci-bn-icon">⚠️</span>
                  <span>Bottleneck: <strong>Lajpat Nagar Ring Road Merge</strong> · Delay: +3.8m</span>
                </div>
              </div>

              <!-- Corridor 3 -->
              <div class="corridor-item" id="ci-c3" onclick="selectDashboardCorridor('c3')">
                <div class="ci-header">
                  <div class="ci-title-wrap">
                    <span class="ci-id-tag c3">C-03</span>
                    <span class="ci-name">Dhaula Kuan ↔ Sardar Patel Marg ↔ India Gate</span>
                  </div>
                  <span class="ci-los-badge los-a" id="c3-los">LOS A</span>
                </div>
                <div class="ci-stats">
                  <div class="ci-stat-col"><span>Flow:</span><strong id="c3-vol">3,450 veh/h</strong></div>
                  <div class="ci-stat-col"><span>Avg Speed:</span><strong id="c3-spd">48 km/h</strong></div>
                  <div class="ci-stat-col"><span>Congestion:</span><strong id="c3-cong">14%</strong></div>
                  <div class="ci-stat-col"><span>Sync:</span><strong class="green" id="c3-sync">98%</strong></div>
                </div>
                <div class="ci-bottleneck">
                  <span class="ci-bn-icon green">✓</span>
                  <span>Express Flow · Optimal Transit Green Wave</span>
                </div>
              </div>

              <!-- Corridor 4 -->
              <div class="corridor-item" id="ci-c4" onclick="selectDashboardCorridor('c4')">
                <div class="ci-header">
                  <div class="ci-title-wrap">
                    <span class="ci-id-tag c4">C-04</span>
                    <span class="ci-name">Connaught Place ↔ India Gate ↔ AIIMS ↔ Saket</span>
                  </div>
                  <span class="ci-los-badge los-c" id="c4-los">LOS C</span>
                </div>
                <div class="ci-stats">
                  <div class="ci-stat-col"><span>Flow:</span><strong id="c4-vol">4,890 veh/h</strong></div>
                  <div class="ci-stat-col"><span>Avg Speed:</span><strong id="c4-spd">31 km/h</strong></div>
                  <div class="ci-stat-col"><span>Congestion:</span><strong id="c4-cong">41%</strong></div>
                  <div class="ci-stat-col"><span>Sync:</span><strong class="amber" id="c4-sync">88%</strong></div>
                </div>
                <div class="ci-bottleneck">
                  <span class="ci-bn-icon">⚠️</span>
                  <span>Bottleneck: <strong>Aurobindo Marg Influx</strong> · Delay: +4.5m</span>
                </div>
              </div>
            </div>

            <!-- Selected Corridor Deep-Inspection Card -->
            <div class="selected-corridor-card" id="selected-corridor-card">
              <div class="scc-header">
                <span class="scc-title" id="scc-title">CORRIDOR 1: KAROL BAGH - ITO DEEP PROFILE</span>
                <span class="scc-badge online" id="scc-status">ACTIVE CO-ORDINATION</span>
              </div>
              <div class="scc-grid">
                <div class="scc-item">
                  <span class="scc-lbl">ROADWAY CAPACITY:</span>
                  <strong id="scc-capacity">5,200 veh/hr (V/C: 0.79)</strong>
                </div>
                <div class="scc-item">
                  <span class="scc-lbl">MEDIAN DENSITY:</span>
                  <strong id="scc-density">38.4 vehicles / km</strong>
                </div>
                <div class="scc-item">
                  <span class="scc-lbl">END-TO-END TIME:</span>
                  <strong id="scc-tt">14.2 min (Baseline: 12.0 min)</strong>
                </div>
                <div class="scc-item">
                  <span class="scc-lbl">TRANSIT PRIORITY:</span>
                  <strong class="cyan" id="scc-transit">Route 419 Bus TSP Active</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- Column 2: Live Velocity & Volume Trend Visualizer + Modal Split -->
          <div class="dash-card traffic-chart-card">
            <div class="dcard-header">
              <div class="dcard-title-group">
                <span class="dcard-icon">📊</span>
                <div>
                  <h3 class="dcard-title">Hourly Traffic Velocity &amp; Density Profile</h3>
                  <span class="dcard-sub">24-hour continuous sensor fusion &amp; velocity curves</span>
                </div>
              </div>
              <div class="chart-horizon-group">
                <button class="ch-btn active" id="btn-horizon-24h" onclick="setDashboardChartMode('24h')">24H CYCLE</button>
                <button class="ch-btn" id="btn-horizon-live" onclick="setDashboardChartMode('live')">REAL-TIME</button>
              </div>
            </div>

            <!-- Canvas Chart Container -->
            <div class="dash-chart-wrapper">
              <canvas id="dash-traffic-canvas" width="560" height="220"></canvas>
            </div>

            <div class="dash-chart-legend">
              <span class="dcl-item"><span class="dcl-color blue"></span> Traffic Volume (veh/hr ×100)</span>
              <span class="dcl-item"><span class="dcl-color cyan"></span> Average Velocity (km/h)</span>
              <span class="dcl-item"><span class="dcl-color amber"></span> Congestion Threshold (30 km/h)</span>
            </div>

            <!-- Modal Fleet Composition Matrix -->
            <div class="dash-modal-split-box">
              <div class="dms-title">MUNICIPAL FLEET MODAL SPLIT &amp; EMISSION PROFILE</div>
              <div class="dms-bars">
                <div class="dms-bar-row">
                  <span class="dms-label">Public Transit (DTC Electric Buses)</span>
                  <div class="dms-bar-track"><div class="dms-bar-fill blue" style="width: 28.4%;"></div></div>
                  <span class="dms-pct">28.4%</span>
                </div>
                <div class="dms-bar-row">
                  <span class="dms-label">Commercial Cabs &amp; Shared EV Mobility</span>
                  <div class="dms-bar-track"><div class="dms-bar-fill green" style="width: 34.2%;"></div></div>
                  <span class="dms-pct">34.2%</span>
                </div>
                <div class="dms-bar-row">
                  <span class="dms-label">Private Sedans &amp; Passenger SUVs</span>
                  <div class="dms-bar-track"><div class="dms-bar-fill amber" style="width: 29.8%;"></div></div>
                  <span class="dms-pct">29.8%</span>
                </div>
                <div class="dms-bar-row">
                  <span class="dms-label">Two-Wheelers &amp; Last-Mile Auto-Rickshaws</span>
                  <div class="dms-bar-track"><div class="dms-bar-fill purple" style="width: 7.6%;"></div></div>
                  <span class="dms-pct">7.6%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Column 3: AI Adaptive Signals & Predictive Congestion Horizon -->
          <div class="dash-card signal-predict-card">
            <!-- Part 1: AI Adaptive Signal Synchronization -->
            <div class="dcard-header">
              <div class="dcard-title-group">
                <span class="dcard-icon">🚦</span>
                <div>
                  <h3 class="dcard-title">Adaptive Signal Mesh &amp; Split Control</h3>
                  <span class="dcard-sub">Edge AI junction timing &amp; green-wave coordination</span>
                </div>
              </div>
              <button class="mini-action-btn" onclick="recalculateSignalSplits()">Auto-Tune</button>
            </div>

            <div class="dash-signals-list">
              <div class="ds-item">
                <div class="ds-top">
                  <span class="ds-junction">ITO Flyover Junction (CAM-02)</span>
                  <span class="ds-badge green" id="sig-ito">GREEN: 62s</span>
                </div>
                <div class="ds-meta">
                  <span>Phase: Eastbound Wave</span>
                  <span>Queue: 18 veh</span>
                  <span class="green">Synced (96%)</span>
                </div>
              </div>

              <div class="ds-item">
                <div class="ds-top">
                  <span class="ds-junction">Connaught Place Outer Circle (CAM-01)</span>
                  <span class="ds-badge green" id="sig-cp">GREEN: 45s</span>
                </div>
                <div class="ds-meta">
                  <span>Phase: Radial Circulatory</span>
                  <span>Queue: 12 veh</span>
                  <span class="green">Synced (92%)</span>
                </div>
              </div>

              <div class="ds-item">
                <div class="ds-top">
                  <span class="ds-junction">AIIMS Flyover Underpass (CAM-05)</span>
                  <span class="ds-badge amber" id="sig-aiims">SPLIT: 54s</span>
                </div>
                <div class="ds-meta">
                  <span>Phase: Ring Road Priority</span>
                  <span>Queue: 24 veh</span>
                  <span class="amber">Dense (88%)</span>
                </div>
              </div>

              <div class="ds-item">
                <div class="ds-top">
                  <span class="ds-junction">Moolchand Metro Crossing (CAM-06)</span>
                  <span class="ds-badge green" id="sig-moolchand">GREEN: 40s</span>
                </div>
                <div class="ds-meta">
                  <span>Phase: BRTS Bus Priority</span>
                  <span>Queue: 15 veh</span>
                  <span class="green">Synced (95%)</span>
                </div>
              </div>
            </div>

            <!-- Part 2: Predictive Congestion Forecaster -->
            <div class="dash-predictive-box">
              <div class="dpb-header">
                <span class="dpb-title">🔮 PREDICTIVE CONGESTION HORIZON</span>
                <div class="dpb-horizon-toggles">
                  <button class="dh-btn active" id="btn-pred-15" onclick="setDashboardPredictHorizon(15)">+15m</button>
                  <button class="dh-btn" id="btn-pred-30" onclick="setDashboardPredictHorizon(30)">+30m</button>
                  <button class="dh-btn" id="btn-pred-60" onclick="setDashboardPredictHorizon(60)">+60m</button>
                </div>
              </div>

              <div class="dpb-content" id="dpb-content">
                <div class="dpb-stat-row">
                  <span>Predicted City Speed:</span>
                  <strong class="green" id="pred-speed">38.6 km/h (▲ +1.2 km/h)</strong>
                </div>
                <div class="dpb-stat-row">
                  <span>Congestion Probability:</span>
                  <strong class="cyan" id="pred-prob">18% (Low Risk)</strong>
                </div>
                <div class="dpb-stat-row">
                  <span>Primary Chokepoint Risk:</span>
                  <strong class="amber" id="pred-choke">Lajpat Nagar Merge (34%)</strong>
                </div>
                <div class="dpb-advisory" id="dpb-advisory">
                  <span>💡 Advisory: <strong>Maintain current green wave on C-01 &amp; C-03.</strong> Route 522 bus mobile ANPR units will monitor Ring Road inflow.</span>
                </div>
              </div>

              <div class="dpb-actions">
                <button class="dpb-btn-broadcast" onclick="broadcastCongestionAdvisory()">📢 Broadcast Advisory to Navigation Mesh</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
'''
    # Insert right before </main>
    html = html.replace('</main>', dashboard_section + '\n  </main>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html with Executive Dashboard.")
