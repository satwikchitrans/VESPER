# -*- coding: utf-8 -*-
"""
Style the boxes in Map View with Blue surfaces (#213D77 / #1A3160),
and text in White (#FFFFFF) or Orange (#EC6E2A) according to importance.
Change nothing else (no layout, sizing, or structure changes).
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Overwrite the Tactical GIS Map View block at the end of style.css
map_view_blue_boxes_css = """/* ═══════════════════════════════════════════════════════════════════ */
/* TACTICAL GIS MAP VIEW — BLUE BOXES WITH WHITE & ORANGE TEXT        */
/* ═══════════════════════════════════════════════════════════════════ */

/* Map View Sidebar Panels (Blue Box Surfaces) */
.gis-sidebar,
.gis-right-sidebar {
  background: #142447 !important;
}

.gis-sidebar .panel-section,
.gis-right-sidebar .panel-section {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  border-radius: var(--radius-md) !important;
  box-shadow: 0 4px 16px rgba(10, 20, 45, 0.4) !important;
  color: #ffffff !important;
}

.gis-sidebar .panel-title,
.gis-right-sidebar .panel-title {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gis-sidebar .badge-mini,
.gis-right-sidebar .badge-mini {
  background: #1a3160 !important;
  border: 1px solid #ec6e2a !important;
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

/* Left Sidebar: Target Acquisition */
.gis-sidebar .acq-tabs {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
}

.gis-sidebar .acq-tab {
  color: #cbd5e1 !important;
  font-weight: 700 !important;
}

.gis-sidebar .acq-tab:hover {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.1) !important;
}

.gis-sidebar .acq-tab.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
  box-shadow: 0 2px 8px rgba(236, 110, 42, 0.4) !important;
}

.gis-sidebar .acq-input,
.gis-sidebar .acq-select {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
}

.gis-sidebar .acq-input:focus,
.gis-sidebar .acq-select:focus {
  border-color: #ec6e2a !important;
  box-shadow: 0 0 8px rgba(236, 110, 42, 0.4) !important;
}

.gis-sidebar .acq-input::placeholder {
  color: #94a3b8 !important;
}

.gis-sidebar .acq-btn.primary {
  background: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
  border: none !important;
}

.gis-sidebar .acq-btn.primary:hover {
  background: #d4601f !important;
}

.gis-sidebar .acq-btn.secondary {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gis-sidebar .acq-btn.secondary:hover {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
  color: #ffffff !important;
}

/* Sighting Chain Summary Card */
.acq-sighting-summary-card {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-left: 3px solid #ec6e2a !important;
  border-radius: 6px !important;
  color: #ffffff !important;
}

.assc-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
}

.assc-title {
  color: #ffffff !important;
  font-weight: 900 !important;
}

.assc-badge {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: none !important;
  font-weight: 800 !important;
}

.assc-lbl {
  color: #cbd5e1 !important;
  font-weight: 600 !important;
}

.assc-row strong,
.assc-row span:not(.assc-lbl) {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.assc-row strong.cyan,
.assc-row span.amber {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

.assc-btn.primary {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: none !important;
  font-weight: 800 !important;
}

.assc-btn.primary:hover {
  background: #d4601f !important;
}

.assc-btn.secondary {
  background: #213d77 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  font-weight: 800 !important;
}

.assc-btn.secondary:hover {
  background: #1a3160 !important;
  border-color: #ec6e2a !important;
}

.acq-hint {
  color: #cbd5e1 !important;
}

.acq-chip {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #ffffff !important;
}

.acq-chip:hover {
  background: #213d77 !important;
  border-color: #ec6e2a !important;
}

.acq-chip.active {
  background: #1a3160 !important;
  border: 1.5px solid #ec6e2a !important;
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.acq-chip.stolen {
  border-left: 3px solid #ec6e2a !important;
  color: #ffffff !important;
}

/* Vehicle List Cards (Left Sidebar) */
.gis-sidebar .vehicle-card {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #ffffff !important;
}

.gis-sidebar .vehicle-card.active {
  border-color: #ec6e2a !important;
  box-shadow: 0 0 10px rgba(236, 110, 42, 0.4) !important;
}

.gis-sidebar .vc-plate {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gis-sidebar .vc-tag {
  background: #213d77 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
}

.gis-sidebar .vc-tag.stolen {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

/* Right Sidebar: Active Feed & Nearby ANPR */
.gis-right-sidebar .nearby-card.active-card {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-left: 3px solid #ec6e2a !important;
}

.gis-right-sidebar .nc-role {
  color: #cbd5e1 !important;
  font-weight: 700 !important;
}

.gis-right-sidebar .nc-status.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gis-right-sidebar .nc-main .nc-name {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gis-right-sidebar .nc-main .nc-detail {
  color: #cbd5e1 !important;
}

.gis-right-sidebar .subgroup-label {
  color: #cbd5e1 !important;
  font-weight: 800 !important;
}

.gis-right-sidebar .nearby-row {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #ffffff !important;
}

.gis-right-sidebar .nearby-row:hover {
  background: #213d77 !important;
  border-color: #ec6e2a !important;
}

.gis-right-sidebar .nr-name {
  color: #ffffff !important;
  font-weight: 700 !important;
}

.gis-right-sidebar .nr-dist {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.gis-right-sidebar .nr-badge.fixed {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: #ffffff !important;
}

.gis-right-sidebar .nr-badge.mobile {
  background: #ec6e2a !important;
  color: #ffffff !important;
}

.gis-right-sidebar .nearby-intercept-box {
  background: #1a3160 !important;
  border: 1.5px dashed #ec6e2a !important;
  color: #ffffff !important;
}

.gis-right-sidebar .nib-label {
  color: #cbd5e1 !important;
  font-weight: 700 !important;
}

.gis-right-sidebar .nib-val {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

.gis-right-sidebar .conf-tier.high {
  background: #1a3160 !important;
  color: #ec6e2a !important;
  border: 1px solid #ec6e2a !important;
}

.gis-right-sidebar .conf-desc,
.gis-right-sidebar .factor-label {
  color: #cbd5e1 !important;
}

.gis-right-sidebar .factor-bar {
  background: #1a3160 !important;
}

.gis-right-sidebar .factor-fill {
  background: #ec6e2a !important;
}

.gis-right-sidebar .factor-val {
  color: #ffffff !important;
  font-weight: 700 !important;
}

.gis-right-sidebar .conf-ring-val {
  color: #ffffff !important;
  font-weight: 900 !important;
}

/* In-Map Sighting Inspector Drawer (Blue Box) */
.gis-sighting-inspector {
  background: #213d77 !important;
  border: 2px solid #ec6e2a !important;
  border-radius: 8px !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(33, 61, 119, 0.5) !important;
  color: #ffffff !important;
}

.gsi-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.18) !important;
}

.gsi-badge {
  background: #1a3160 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  font-weight: 900 !important;
}

.gsi-sensor-pill {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: 1px solid #ec6e2a !important;
  font-weight: 800 !important;
}

.gsi-sensor-pill.fixed {
  background: #1a3160 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
}

.gsi-close-btn {
  color: #ffffff !important;
}

.gsi-close-btn:hover {
  background: #ec6e2a !important;
  color: #ffffff !important;
}

.gsi-plate-banner {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 6px !important;
}

.gsi-plate-text {
  color: #ffffff !important;
  font-weight: 900 !important;
}

.gsi-target-desc {
  color: #cbd5e1 !important;
}

.gsi-sec-lbl {
  color: #cbd5e1 !important;
  font-weight: 800 !important;
}

.gsi-char-chip {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 4px !important;
}

.gsi-char-chip .gcc-char {
  color: #ffffff !important;
  font-weight: 900 !important;
}

.gsi-char-chip .gcc-conf {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.gsi-canvas-wrap {
  border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
  background: #000000 !important;
  border-radius: 4px !important;
}

.gsi-canvas-tag {
  background: #ec6e2a !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gsi-telem-item {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 4px !important;
}

.gsi-telem-item .gt-lbl {
  color: #cbd5e1 !important;
}

.gsi-telem-item .gt-val {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gsi-telem-item .gt-val.cyan,
.gsi-telem-item .gt-val.green,
.gsi-telem-item .gt-val.amber {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

.gsi-location-bar {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 4px !important;
}

.glb-street {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.glb-gps {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.glb-copy-btn {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.glb-copy-btn:hover {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
}

.gsi-handoff-strip {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 4px !important;
}

.gh-node {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gh-node.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
  font-weight: 900 !important;
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
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
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

/* In-Map Sighting Chain HUD (Blue Box) */
.gis-sighting-chain-hud {
  background: #213d77 !important;
  border: 2px solid #ec6e2a !important;
  border-radius: 8px !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6) !important;
  color: #ffffff !important;
}

.gsch-tag {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

.gsch-plate {
  color: #ffffff !important;
  font-weight: 900 !important;
}

.gsch-close-btn {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gsch-close-btn:hover {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
}

.gsch-stat {
  background: #1a3160 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.gsch-stat-lbl {
  color: #cbd5e1 !important;
}

.gsch-stat-val {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.gsch-stat-val.cyan,
.gsch-stat-val.green,
.gsch-stat-val.amber {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

.gsch-action-btn.cyan {
  background: #1a3160 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

.gsch-action-btn.amber,
.gsch-action-btn.red {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border: 1px solid #ec6e2a !important;
}

/* In-Map Switching HUD (Blue Box) */
#gis-switching-hud {
  background: #213d77 !important;
  border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
  border-left: 4px solid #ec6e2a !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
  color: #ffffff !important;
}

#gis-switching-hud .hud-tag {
  color: #ec6e2a !important;
  font-weight: 900 !important;
}

#gis-switching-hud .hud-node {
  background: #1a3160 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
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
  color: #cbd5e1 !important;
}

#gis-switching-hud .hm-val {
  color: #ffffff !important;
  font-weight: 800 !important;
}

/* Map Legend (Blue Box) */
#gis-map-legend {
  background: #213d77 !important;
  border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
  color: #ffffff !important;
}

.legend-item {
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 9px !important;
}

/* Map Top Overlay Controls (Blue Boxes) */
.overlay-chip-btn {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

.overlay-chip-btn:hover {
  background: #1a3160 !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

.overlay-chip-btn.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
  box-shadow: 0 2px 10px rgba(236, 110, 42, 0.45) !important;
}

.overlay-chip-btn.accent-cyan,
.overlay-chip-btn.godseye-btn,
.overlay-chip-btn.godseye-mode-chip {
  background: #213d77 !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
}

.overlay-chip-btn.accent-cyan:hover,
.overlay-chip-btn.godseye-btn:hover,
.overlay-chip-btn.godseye-mode-chip:hover {
  background: #ec6e2a !important;
  border-color: #ec6e2a !important;
  color: #ffffff !important;
}

.gis-shader-group {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

.shader-chip-btn {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.shader-chip-btn:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  color: #ffffff !important;
}

.shader-chip-btn.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  box-shadow: 0 0 8px rgba(236, 110, 42, 0.5) !important;
}

.shader-chip-btn.accent-3d.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
}

.overlay-chip {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

.overlay-chip .chip-label {
  color: #cbd5e1 !important;
  font-weight: 700 !important;
}

.overlay-chip .chip-val {
  color: #ffffff !important;
  font-weight: 800 !important;
}

.overlay-chip.accent {
  border-color: #ec6e2a !important;
}

.overlay-chip.accent .chip-val {
  color: #ec6e2a !important;
}

/* Timeline (Blue Box) */
.gis-timeline {
  background: #142447 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
}

.timeline-title {
  color: #ffffff !important;
}

.target-sub-badge {
  color: #cbd5e1 !important;
}

.tl-action-btn {
  background: #213d77 !important;
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
  background: #213d77 !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.tl-speed-btn.active {
  background: #ec6e2a !important;
  color: #ffffff !important;
  border-color: #ec6e2a !important;
}

.timeline-sighting-node {
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

.timeline-sighting-node:hover,
.timeline-sighting-node.active {
  background: #1a3160 !important;
  border-color: #ec6e2a !important;
  box-shadow: 0 0 12px rgba(236, 110, 42, 0.6) !important;
}

.timeline-sighting-node .tsn-cam {
  color: #ffffff !important;
  font-weight: 900 !important;
}

.timeline-sighting-node .tsn-time {
  color: #cbd5e1 !important;
}

.timeline-sighting-node .tsn-type {
  color: #ec6e2a !important;
  font-weight: 800 !important;
}

.timeline-sighting-node.mobile .tsn-type {
  color: #ffffff !important;
}

.tbc-line {
  background: repeating-linear-gradient(90deg, #ec6e2a, #ec6e2a 4px, transparent 4px, transparent 8px) !important;
}

.tbc-tag {
  color: #ffffff !important;
  background: #213d77 !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  padding: 1px 4px !important;
  border-radius: 3px !important;
  font-size: 8px !important;
}
"""

# Replace the block
target_idx = css.find('/* ═══════════════════════════════════════════════════════════════════ */\n/* TACTICAL GIS MAP VIEW')
if target_idx != -1:
    css = css[:target_idx] + map_view_blue_boxes_css
else:
    css += '\n\n' + map_view_blue_boxes_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Successfully applied Blue boxes with White & Orange text in Map View.')
