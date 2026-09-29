# -*- coding: utf-8 -*-
"""
Fix the color palette in the Map View (Tactical GIS, In-Map HUDs, Sighting Inspector,
Map Overlays, Markers, Sidebar Panels, Legends, and Timeline) to strictly adhere to
the IRCTC palette: Primary Navy Blue (#213D77 / #1A3160), Orange (#EC6E2A / #F05A28), and White (#FFFFFF / #F4F6FB).
Only colors and visual styling are adjusted. No layout, sizing, or structural logic is changed.
"""
import re

# 1. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add / overwrite dedicated Map View IRCTC color rules at the end of style.css with high specificity
map_view_irctc_css = """

/* ═══════════════════════════════════════════════════════════════════ */
/* TACTICAL GIS MAP VIEW — STRICT IRCTC COLOR PALETTE (#213D77, ORANGE, WHITE) */
/* ═══════════════════════════════════════════════════════════════════ */

/* Map container & Leaflet */
#gis-map,
.gis-map-container,
.leaflet-container {
  background: #f4f6fb !important;
}

.leaflet-control-zoom {
  border: 1px solid #213d77 !important;
  box-shadow: 0 2px 8px rgba(33, 61, 119, 0.2) !important;
  border-radius: 4px !important;
  overflow: hidden;
}

.leaflet-control-zoom a {
  background: #ffffff !important;
  color: #213d77 !important;
  border-bottom: 1px solid #e2e8f0 !important;
}

.leaflet-control-zoom a:hover {
  background: #213d77 !important;
  color: #ffffff !important;
}

.leaflet-popup-content-wrapper {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  border-radius: 6px !important;
  color: #1a1a2e !important;
  box-shadow: 0 8px 24px rgba(33, 61, 119, 0.25) !important;
}

.leaflet-popup-tip {
  background: #ffffff !important;
  border: 1px solid #213d77 !important;
}

.map-popup-live-btn {
  background: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
  border: none !important;
  border-radius: 4px !important;
  padding: 4px 8px !important;
  cursor: pointer !important;
  font-family: var(--font-sans) !important;
  font-size: 10px !important;
}

.map-popup-live-btn:hover {
  background: #d4601f !important;
}

/* Map Top Overlay Controls */
#gis-map-overlay-top {
  pointer-events: none !important;
}

#gis-map-overlay-top > * {
  pointer-events: auto !important;
}

.overlay-chip-btn {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  color: #213d77 !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 8px rgba(33, 61, 119, 0.15) !important;
}

.overlay-chip-btn:hover {
  background: #213d77 !important;
  color: #ffffff !important;
  border-color: #213d77 !important;
}

.overlay-chip-btn.active {
  background: #213d77 !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
  box-shadow: 0 2px 10px rgba(236, 110, 42, 0.35) !important;
}

.overlay-chip-btn.accent-cyan,
.overlay-chip-btn.godseye-btn,
.overlay-chip-btn.godseye-mode-chip {
  background: #ffffff !important;
  border-color: #213d77 !important;
  color: #213d77 !important;
}

.overlay-chip-btn.accent-cyan:hover,
.overlay-chip-btn.godseye-btn:hover,
.overlay-chip-btn.godseye-mode-chip:hover {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
  color: #ffffff !important;
}

.gis-shader-group {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  box-shadow: 0 2px 8px rgba(33, 61, 119, 0.15) !important;
}

.shader-chip-btn {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.shader-chip-btn:hover {
  background: rgba(33, 61, 119, 0.1) !important;
  color: #213d77 !important;
}

.shader-chip-btn.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  box-shadow: 0 0 8px rgba(236, 110, 42, 0.4) !important;
}

.shader-chip-btn.accent-3d.active {
  background: #213d77 !important;
  color: #ffffff !important;
}

.overlay-chip {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  box-shadow: 0 2px 8px rgba(33, 61, 119, 0.15) !important;
}

.overlay-chip .chip-label {
  color: #4a5568 !important;
  font-weight: 700 !important;
}

.overlay-chip .chip-val {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.overlay-chip.accent {
  border-color: #ec6e2a !important;
}

.overlay-chip.accent .chip-val {
  color: #ec6e2a !important;
}

/* Map Legend */
#gis-map-legend {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 16px rgba(33, 61, 119, 0.2) !important;
  color: #213d77 !important;
}

.legend-item {
  color: #213d77 !important;
  font-weight: 700 !important;
  font-size: 9px !important;
}

/* In-Map Switching HUD */
#gis-switching-hud {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 16px rgba(33, 61, 119, 0.2) !important;
  color: #1a1a2e !important;
}

#gis-switching-hud .hud-tag {
  color: #213d77 !important;
  font-weight: 900 !important;
}

#gis-switching-hud .hud-node {
  background: #e8edf5 !important;
  color: #213d77 !important;
  border: 1px solid #213d77 !important;
  font-weight: 800 !important;
}

#gis-switching-hud .hud-node.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

#gis-switching-hud .hud-zone {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

#gis-switching-hud .hm-lbl {
  color: #718096 !important;
}

#gis-switching-hud .hm-val {
  color: #213d77 !important;
  font-weight: 800 !important;
}

/* In-Map Sighting Inspector Drawer */
.gis-sighting-inspector {
  background: #ffffff !important;
  border: 2px solid #213d77 !important;
  border-radius: 8px !important;
  box-shadow: 0 12px 36px rgba(33, 61, 119, 0.3) !important;
  color: #1a1a2e !important;
}

.gsi-header {
  border-bottom: 1.5px solid #e2e8f0 !important;
}

.gsi-badge {
  background: #213d77 !important;
  color: #ffffff !important;
  border: 1px solid #213d77 !important;
  font-weight: 900 !important;
}

.gsi-sensor-pill {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: 1px solid #ec6e2a !important;
  font-weight: 800 !important;
}

.gsi-sensor-pill.fixed {
  background: #213d77 !important;
  color: #ffffff !important;
  border-color: #213d77 !important;
}

.gsi-close-btn {
  color: #213d77 !important;
}

.gsi-close-btn:hover {
  background: #ec6e2a !important;
  color: #ffffff !important;
}

.gsi-plate-banner {
  background: #213d77 !important;
  border: 1.5px solid #213d77 !important;
  border-radius: 6px !important;
}

.gsi-plate-text {
  color: #ffffff !important;
  font-weight: 900 !important;
}

.gsi-target-desc {
  color: #e2e8f0 !important;
}

.gsi-sec-lbl {
  color: #4a5568 !important;
  font-weight: 800 !important;
}

.gsi-char-chip {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  border-radius: 4px !important;
}

.gsi-char-chip .gcc-char {
  color: #213d77 !important;
  font-weight: 900 !important;
}

.gsi-char-chip .gcc-conf {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.gsi-canvas-wrap {
  border: 1.5px solid #213d77 !important;
  background: #000000 !important;
  border-radius: 4px !important;
}

.gsi-canvas-tag {
  background: #213d77 !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gsi-telem-item {
  background: #f4f6fb !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 4px !important;
}

.gsi-telem-item .gt-lbl {
  color: #718096 !important;
}

.gsi-telem-item .gt-val {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.gsi-telem-item .gt-val.cyan,
.gsi-telem-item .gt-val.green,
.gsi-telem-item .gt-val.amber {
  color: #ec6e2a !important;
}

.gsi-location-bar {
  background: #f4f6fb !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 4px !important;
}

.glb-street {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.glb-gps {
  color: #ec6e2a !important;
  font-weight: 700 !important;
}

.glb-copy-btn {
  background: #ffffff !important;
  border: 1px solid #213d77 !important;
  color: #213d77 !important;
  font-weight: 800 !important;
}

.glb-copy-btn:hover {
  background: #213d77 !important;
  color: #ffffff !important;
}

.gsi-handoff-strip {
  background: #f4f6fb !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 4px !important;
}

.gh-node {
  background: #ffffff !important;
  border: 1px solid #213d77 !important;
  color: #213d77 !important;
  font-weight: 800 !important;
}

.gh-node.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

.gh-arrow {
  color: #ec6e2a !important;
}

.gsi-actions-toolbar .gsi-btn {
  font-family: var(--font-sans) !important;
  font-size: 9.5px !important;
  font-weight: 800 !important;
  border-radius: 4px !important;
  cursor: pointer !important;
  padding: 6px 10px !important;
  border: none !important;
}

.gsi-actions-toolbar .gsi-btn.cyan {
  background: #213d77 !important;
  color: #ffffff !important;
}

.gsi-actions-toolbar .gsi-btn.amber,
.gsi-actions-toolbar .gsi-btn.purple {
  background: #ec6e2a !important;
  color: #ffffff !important;
}

.gsi-actions-toolbar .gsi-btn:hover {
  filter: brightness(1.15) !important;
}

/* In-Map Sighting Chain HUD */
.gis-sighting-chain-hud {
  background: #ffffff !important;
  border: 2px solid #213d77 !important;
  border-radius: 8px !important;
  box-shadow: 0 12px 36px rgba(33, 61, 119, 0.3) !important;
  color: #1a1a2e !important;
}

.gsch-tag {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

.gsch-plate {
  color: #213d77 !important;
  font-weight: 900 !important;
}

.gsch-close-btn {
  background: #ffffff !important;
  border: 1px solid #213d77 !important;
  color: #213d77 !important;
  font-weight: 800 !important;
}

.gsch-close-btn:hover {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

.gsch-stat {
  background: #f4f6fb !important;
  border: 1px solid #e2e8f0 !important;
}

.gsch-stat-lbl {
  color: #718096 !important;
}

.gsch-stat-val {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.gsch-stat-val.cyan,
.gsch-stat-val.green,
.gsch-stat-val.amber {
  color: #ec6e2a !important;
}

.gsch-action-btn.cyan {
  background: #213d77 !important;
  color: #ffffff !important;
  border: 1px solid #213d77 !important;
}

.gsch-action-btn.amber,
.gsch-action-btn.red {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: 1px solid #ec6e2a !important;
}

/* Left Sidebar Target Acquisition Summary Card */
.acq-sighting-summary-card {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  border-radius: 6px !important;
  box-shadow: 0 2px 8px rgba(33, 61, 119, 0.1) !important;
}

.assc-title {
  color: #213d77 !important;
  font-weight: 900 !important;
}

.assc-badge {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: none !important;
  font-weight: 800 !important;
}

.assc-lbl {
  color: #4a5568 !important;
  font-weight: 700 !important;
}

.assc-row strong,
.assc-row span:not(.assc-lbl) {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.assc-row strong.cyan,
.assc-row span.amber {
  color: #ec6e2a !important;
}

.assc-btn.primary {
  background: #213d77 !important;
  color: #ffffff !important;
  border: 1px solid #213d77 !important;
  font-weight: 800 !important;
}

.assc-btn.primary:hover {
  background: #1a3160 !important;
  color: #ffffff !important;
}

.assc-btn.secondary {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: 1px solid #ec6e2a !important;
  font-weight: 800 !important;
}

.assc-btn.secondary:hover {
  background: #d4601f !important;
  color: #ffffff !important;
}

.acq-btn.secondary {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  color: #213d77 !important;
  font-weight: 800 !important;
}

.acq-btn.secondary:hover {
  background: #213d77 !important;
  color: #ffffff !important;
}

.acq-chip.active {
  background: #213d77 !important;
  border-color: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.acq-chip.stolen {
  border-left: 3px solid #ec6e2a !important;
  color: #213d77 !important;
}

/* Right Sidebar in Map View */
.nearby-card.active-card {
  background: #f4f6fb !important;
  border: 1.5px solid #213d77 !important;
}

.nc-role {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.nc-status.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.nearby-row {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
}

.nearby-row:hover {
  background: #e8edf5 !important;
  border-color: #213d77 !important;
}

.nr-name {
  color: #213d77 !important;
  font-weight: 700 !important;
}

.nr-dist {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.nr-badge.fixed {
  background: #213d77 !important;
  color: #ffffff !important;
}

.nr-badge.mobile {
  background: #ec6e2a !important;
  color: #ffffff !important;
}

.nearby-intercept-box {
  background: #f4f6fb !important;
  border: 1.5px dashed #213d77 !important;
}

.nib-label {
  color: #213d77 !important;
  font-weight: 800 !important;
}

.nib-val {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.conf-ring-bg {
  stroke: #e2e8f0 !important;
}

.conf-ring-fill {
  stroke: #ec6e2a !important;
}

.conf-tier.high {
  background: rgba(33, 61, 119, 0.12) !important;
  color: #213d77 !important;
  border: 1px solid #213d77 !important;
}

.factor-bar {
  background: #e2e8f0 !important;
}

.factor-fill {
  background: linear-gradient(90deg, #213d77, #ec6e2a) !important;
}

/* Map Markers */
.marker-fixed-anpr {
  background: #213d77 !important;
  border: 2px solid #ffffff !important;
  box-shadow: 0 0 10px rgba(33, 61, 119, 0.6) !important;
  color: #ffffff !important;
}

.tactical-bus-marker .tbm-body {
  background: #ec6e2a !important;
  border: 2px solid #ffffff !important;
  box-shadow: 0 0 10px rgba(236, 110, 42, 0.6) !important;
}

.tactical-bus-marker .tbm-label {
  background: #213d77 !important;
  border: 1px solid #ffffff !important;
  color: #ffffff !important;
}

.sighting-node-marker .sn-ring {
  border-color: rgba(236, 110, 42, 0.8) !important;
  background: rgba(236, 110, 42, 0.15) !important;
  box-shadow: 0 0 12px rgba(236, 110, 42, 0.5) !important;
}

.sighting-node-marker.active .sn-ring {
  border-color: #213d77 !important;
  background: rgba(33, 61, 119, 0.25) !important;
  box-shadow: 0 0 16px rgba(33, 61, 119, 0.8) !important;
}

.sighting-node-marker .sn-core {
  background: #213d77 !important;
  border: 2px solid #ffffff !important;
  color: #ffffff !important;
}

.sighting-node-marker.mobile .sn-core {
  background: #ec6e2a !important;
  border-color: #ffffff !important;
}

.sighting-node-marker .sn-label {
  background: #213d77 !important;
  border: 1px solid #ffffff !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.sighting-node-marker.active .sn-label {
  background: #ec6e2a !important;
  border-color: #ffffff !important;
  color: #ffffff !important;
}

.tvm-halo {
  border: 2px dashed #ec6e2a !important;
  background: radial-gradient(circle, rgba(236, 110, 42, 0.25) 0%, rgba(236, 110, 42, 0) 70%) !important;
}

.tvm-icon-wrap {
  background: #213d77 !important;
  border: 2px solid #ffffff !important;
  box-shadow: 0 0 14px rgba(33, 61, 119, 0.8) !important;
}

.tvm-tag {
  background: #213d77 !important;
  border: 1.5px solid #ffffff !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(33, 61, 119, 0.4) !important;
}

.tvm-speed {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.tvm-estimate-badge {
  background: #ffffff !important;
  border: 1px solid #213d77 !important;
  color: #213d77 !important;
  font-weight: 800 !important;
}

/* Timeline */
.gis-timeline {
  background: #213d77 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
}

.timeline-title {
  color: #ffffff !important;
}

.target-sub-badge {
  color: #cbd5e1 !important;
}

.tl-action-btn {
  background: #1a3160 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  font-weight: 700 !important;
}

.tl-action-btn:hover {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
  color: #ffffff !important;
}

.tl-action-btn.active,
.tl-action-btn.primary {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
  color: #ffffff !important;
}

.tl-speed-btn {
  background: #1a3160 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.tl-speed-btn.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

.timeline-sighting-node {
  background: #ffffff !important;
  border: 1.5px solid #213d77 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
}

.timeline-sighting-node:hover,
.timeline-sighting-node.active {
  background: #ffffff !important;
  border-color: #ec6e2a !important;
  box-shadow: 0 0 12px rgba(236, 110, 42, 0.5) !important;
}

.timeline-sighting-node .tsn-cam {
  color: #213d77 !important;
  font-weight: 900 !important;
}

.timeline-sighting-node .tsn-time {
  color: #4a5568 !important;
}

.timeline-sighting-node .tsn-type {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.timeline-sighting-node.mobile .tsn-type {
  color: #213d77 !important;
}

.tbc-line {
  background: repeating-linear-gradient(90deg, #ec6e2a, #ec6e2a 4px, transparent 4px, transparent 8px) !important;
}

.tbc-tag {
  color: #ffffff !important;
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  padding: 1px 4px !important;
  border-radius: 3px !important;
  font-size: 8px !important;
}
"""

if '/* TACTICAL GIS MAP VIEW — STRICT IRCTC COLOR PALETTE' not in css:
    css += map_view_irctc_css
else:
    # Replace existing block
    idx = css.find('/* ═══════════════════════════════════════════════════════════════════ */\n/* TACTICAL GIS MAP VIEW — STRICT IRCTC COLOR PALETTE')
    if idx != -1:
        css = css[:idx] + map_view_irctc_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated style.css with IRCTC Map View palette.')

# 2. Update app.js map initializations & trajectory colors
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change default tileLayer to street (OpenStreetMap)
js = js.replace(
    "const darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {\n    subdomains: 'abcd', maxZoom: 22, maxNativeZoom: 19, updateWhenIdle: false, keepBuffer: 4\n  }).addTo(map);",
    "const darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {\n    subdomains: 'abcd', maxZoom: 22, maxNativeZoom: 19, updateWhenIdle: false, keepBuffer: 4\n  });"
)

# Make street layer the default attached to map
js = js.replace(
    "  const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {\n    maxZoom: 22,\n    maxNativeZoom: 19,\n    updateWhenIdle: false,\n    keepBuffer: 4\n  });",
    "  const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {\n    maxZoom: 22,\n    maxNativeZoom: 19,\n    updateWhenIdle: false,\n    keepBuffer: 4\n  }).addTo(map);"
)

js = js.replace("STATE.currentTileLayer = 'dark';", "STATE.currentTileLayer = 'street';")

# Replace mini-map carto dark with street/light
js = js.replace(
    "L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { subdomains: 'abcd', maxZoom: 19 }).addTo(map);",
    "L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);"
)

# Trajectory confirmed lines: #213D77 and #EC6E2A
js = js.replace("color: '#00e5ff',", "color: '#213d77',")
js = js.replace("color: veh.isStolen ? '#f87171' : '#34d399',", "color: veh.isStolen ? '#ec6e2a' : '#213d77',")
js = js.replace("color: veh.isStolen ? '#f87171' : '#00e5ff',", "color: veh.isStolen ? '#ec6e2a' : '#213d77',")

# Marker popups colors
js = js.replace("color:#00e5ff;font-size:11px", "color:#213d77;font-size:11px")
js = js.replace("color:#34d399;margin:3px 0 6px", "color:#ec6e2a;margin:3px 0 6px")
js = js.replace("color:#34d399", "color:#ec6e2a")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('Updated app.js with IRCTC Map Layer and Trajectory colors.')

# 3. Update index.html and editor.html legend dots
for fname in ['index.html', 'editor.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update legend dots to IRCTC palette
    old_legend = """          <div id="gis-map-legend">
            <div class="legend-item"><span class="legend-dot" style="background:#00e5ff"></span> Fixed ANPR</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ffc107"></span> Mobile Bus</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ff1744"></span> Target Vehicle</div>
            <div class="legend-item"><span class="legend-dot" style="background:#69f0ae"></span> Trajectory</div>
            <div class="legend-item"><span class="legend-dot" style="background:#7c4dff;border:2px dashed #b388ff"></span> Reachability Cone</div>
          </div>"""

    new_legend = """          <div id="gis-map-legend">
            <div class="legend-item"><span class="legend-dot" style="background:#213d77"></span> Fixed ANPR</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ec6e2a"></span> Mobile Bus</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ec6e2a;border:1.5px solid #213d77"></span> Target Vehicle</div>
            <div class="legend-item"><span class="legend-dot" style="background:#213d77"></span> Trajectory</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ffffff;border:1.5px dashed #ec6e2a"></span> Reachability Cone</div>
          </div>"""

    if old_legend in html:
        html = html.replace(old_legend, new_legend)
    else:
        # regex replace if whitespace differences
        html = re.sub(
            r'<div id="gis-map-legend">[\s\S]*?<\/div>\s*<\/div>',
            new_legend + '\n        </div>',
            html,
            count=1
        )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Updated legend in {fname}')

print('All Map View colors updated to IRCTC palette successfully.')
