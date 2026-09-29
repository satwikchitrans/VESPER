import re
import json

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

with open('style.css', 'r', encoding='utf-8', errors='ignore') as f:
    style_css = f.read()

# 1. Update initBuses in app.js
new_init_buses = """function initBuses(map) {
  BUS_ROUTES.forEach(bus => {
    STATE.busWaypointIndex[bus.id] = 0;
    const startPt = (bus.roadPath && bus.roadPath.length) ? (Array.isArray(bus.roadPath[0]) ? bus.roadPath[0] : [bus.roadPath[0].lat, bus.roadPath[0].lng]) : [bus.waypoints[0].lat, bus.waypoints[0].lng];
    STATE.busPositions[bus.id] = { lat: startPt[0], lng: startPt[1] };
    
    const html = `
      <div class="tactical-bus-marker" id="tbm-wrap-${bus.id}">
        <div class="tbm-body">
          <span class="tbm-icon">🚌</span>
        </div>
        <div class="tbm-label">${bus.id}</div>
      </div>
    `;
    const icon = L.divIcon({ className: 'marker-bus-wrapper', html: html, iconSize: [28, 28], iconAnchor: [14, 14] });
    const marker = L.marker(startPt, { icon, zIndexOffset: 2000 }).addTo(map);
    marker.bindPopup(`<div style="padding:4px"><div style="font-weight:700;color:#fbbf24;font-size:11px">${bus.id}</div><div style="font-size:10px;color:#94a3b8">${bus.name}</div><div style="font-size:9px;color:#fbbf24;margin:3px 0 6px">Hailo-8 NPU · Active Mobile ANPR</div><button class="map-popup-live-btn" onclick="openLiveCameraModal('${bus.id}')"> Watch Live Feed</button></div>`);
    STATE.markers.buses[bus.id] = marker;
  });
}"""

app_js = re.sub(r'function initBuses\(map\)\s*\{[\s\S]*?STATE\.markers\.buses\[bus\.id\] = marker;\s*\}\);?\s*\}', new_init_buses, app_js, count=1)
print("Updated initBuses")

# 2. Update advanceEntityAlongRoad and startVehicleRoadGlide
unified_physics_engine = """// ========================= PHYSICS-BASED UNIFIED ENTITY SIMULATION =========================
function advanceEntityAlongRoad(entity, deltaMeters) {
  const path = entity.roadPath;
  if (!path || path.length < 2) return null;

  // Initialize and compute cumulative distances if needed
  if (!entity._cumDist || entity._cumDist.length !== path.length) {
    entity._cumDist = [0];
    let total = 0;
    for (let i = 0; i < path.length - 1; i++) {
      const p1 = Array.isArray(path[i]) ? path[i] : [path[i].lat, path[i].lng];
      const p2 = Array.isArray(path[i+1]) ? path[i+1] : [path[i+1].lat, path[i+1].lng];
      total += haversine(p1[0], p1[1], p2[0], p2[1]) * 1000;
      entity._cumDist.push(total);
    }
    entity._totalRoadDist = Math.max(1, total);
  }

  if (entity._roadDist === undefined) {
    entity._roadDist = (entity._roadIndex || 0) * 15;
  }

  const total = entity._totalRoadDist;
  entity._roadDist = (entity._roadDist + deltaMeters) % total;
  if (entity._roadDist < 0) entity._roadDist += total;
  const targetDist = entity._roadDist;

  // Binary search for exact segment
  let low = 0, high = entity._cumDist.length - 1;
  while (low <= high) {
    const mid = (low + high) >> 1;
    if (entity._cumDist[mid] <= targetDist) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  const idx = Math.max(0, Math.min(path.length - 2, high));
  entity._roadIndex = idx;

  const segStartDist = entity._cumDist[idx];
  const segEndDist = entity._cumDist[idx + 1] || total;
  const segLen = Math.max(0.001, segEndDist - segStartDist);
  const segFraction = Math.max(0, Math.min(1, (targetDist - segStartDist) / segLen));

  const p1 = Array.isArray(path[idx]) ? path[idx] : [path[idx].lat, path[idx].lng];
  const p2 = Array.isArray(path[idx+1]) ? path[idx+1] : [path[idx+1].lat, path[idx+1].lng];

  const lat = p1[0] + (p2[0] - p1[0]) * segFraction;
  const lng = p1[1] + (p2[1] - p1[1]) * segFraction;

  const dLng = p2[1] - p1[1];
  const dLat = p2[0] - p1[0];
  const rawBearing = (Math.atan2(dLng, dLat) * 180 / Math.PI + 360) % 360;

  if (entity._heading === undefined) entity._heading = rawBearing;
  else {
    let diff = (rawBearing - entity._heading + 540) % 360 - 180;
    entity._heading = (entity._heading + diff * 0.15 + 360) % 360;
  }

  entity.currentPos = { lat, lng, heading: entity._heading, roadIndex: idx };
  return entity.currentPos;
}

function startVehicleRoadGlide() {
  if (STATE.timers.vehicleGlide) clearInterval(STATE.timers.vehicleGlide);
  if (STATE.timers.bus) clearInterval(STATE.timers.bus);

  const TICK_MS = 50;
  const dt = TICK_MS / 1000; // 0.05 seconds

  STATE.timers.vehicleGlide = setInterval(() => {
    if (STATE.isSimPaused) return;

    // 1. Update all DTC Transit Buses
    if (!STATE.busScannerCones) STATE.busScannerCones = {};
    BUS_ROUTES.forEach(bus => {
      const speedKmh = bus.speedKmh || 35;
      const deltaM = (speedKmh * 1000 / 3600) * dt;
      const pos = advanceEntityAlongRoad(bus, deltaM);
      if (!pos) return;

      STATE.busPositions[bus.id] = { lat: pos.lat, lng: pos.lng };
      const marker = STATE.markers.buses[bus.id];
      if (marker) {
        marker.setLatLng([pos.lat, pos.lng]);
        const wrapEl = document.getElementById(`tbm-wrap-${bus.id}`);
        if (wrapEl) {
          const bodyEl = wrapEl.querySelector('.tbm-body');
          if (bodyEl) bodyEl.style.transform = `rotate(${pos.heading.toFixed(1)}deg)`;
        }
      }

      // Mobile ANPR scanner cone 50m ahead of bus
      if (STATE.maps.gis) {
        const fovDist = 0.00045; // ~50m in lat/lng
        const rad = pos.heading * Math.PI / 180;
        const fovLat = pos.lat + Math.cos(rad) * fovDist;
        const fovLng = pos.lng + Math.sin(rad) * fovDist;

        if (!STATE.busScannerCones[bus.id]) {
          STATE.busScannerCones[bus.id] = L.circle([fovLat, fovLng], {
            radius: 55,
            color: '#fbbf24',
            fillColor: '#fbbf24',
            fillOpacity: 0.12,
            weight: 1,
            dashArray: '4 4'
          }).addTo(STATE.maps.gis);
          STATE.busScannerCones[bus.id].bindTooltip(`🚌 ${bus.id} Mobile ANPR Scanning Zone`, { sticky: true });
        } else {
          STATE.busScannerCones[bus.id].setLatLng([fovLat, fovLng]);
        }
      }
    });

    // 2. Update all Vehicles (Target + Ambient Traffic)
    VEHICLES.forEach(veh => {
      const isSelected = (veh.id === STATE.selectedVehicle);
      const speedKmh = veh.speedKmh || (veh.isStolen ? 56 : 44);
      const deltaM = (speedKmh * 1000 / 3600) * dt;
      const pos = advanceEntityAlongRoad(veh, deltaM);
      if (!pos) return;

      if (isSelected) {
        // Active selected vehicle markers across maps
        if (STATE.markers.vehicles.gis) STATE.markers.vehicles.gis.setLatLng([pos.lat, pos.lng]);
        if (STATE.markers.vehicles.surv) STATE.markers.vehicles.surv.setLatLng([pos.lat, pos.lng]);
        if (STATE.markers.vehicles.grid) STATE.markers.vehicles.grid.setLatLng([pos.lat, pos.lng]);

        // Rotate vehicle icon along road
        document.querySelectorAll(`[id^="tvm-wrap-"]`).forEach(el => {
          el.style.transform = `rotate(${pos.heading.toFixed(1)}deg)`;
        });

        // Synchronize GodsEye satellite view
        if (GODSEYE.active) {
          GODSEYE.onVehicleGlide(pos.lat, pos.lng, pos.heading, veh);
        }

        // Auto-follow on Tactical GIS Map (smooth throttled pan)
        if (STATE.autoFollow && STATE.maps.gis) {
          try {
            const bounds = STATE.maps.gis.getBounds();
            const innerBounds = bounds.pad(-0.25);
            if (!innerBounds.contains([pos.lat, pos.lng])) {
              const nowMs = Date.now();
              if (!STATE._lastGisPan || nowMs - STATE._lastGisPan > 2500) {
                STATE._lastGisPan = nowMs;
                STATE.maps.gis.panTo([pos.lat, pos.lng], { animate: true, duration: 1.2 });
              }
            }
          } catch (e) {}
        }

        // Check ANPR camera interception points
        checkCameraTrigger(veh, pos.lat, pos.lng);
      }
    });

  }, TICK_MS);
}

function moveBuses() {
  // Retained for compatibility; unified engine in startVehicleRoadGlide handles all motion
}"""

app_js = re.sub(r'function startVehicleRoadGlide\(\)\s*\{[\s\S]*?function getCardinal', unified_physics_engine + "\n\nfunction getCardinal", app_js, count=1)
print("Updated startVehicleRoadGlide & moveBuses")

# 3. Add CSS for tactical bus marker
bus_css = """
/* Tactical Bus Markers */
.marker-bus-wrapper {
  background: transparent !important;
  border: none !important;
}
.tactical-bus-marker {
  position: relative;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.tbm-body {
  width: 22px;
  height: 22px;
  border-radius: 5px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border: 1.5px solid #fde68a;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  transition: transform 0.08s linear;
}
.tbm-label {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid #fbbf24;
  color: #fbbf24;
  font-family: var(--font-mono, monospace);
  font-size: 7.5px;
  font-weight: 700;
  padding: 1px 4px;
  border-radius: 3px;
  white-space: nowrap;
  pointer-events: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.5);
}
"""

if '.tactical-bus-marker' not in style_css:
    style_css += "\n" + bus_css
    print("Added bus marker CSS")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(style_css)

print("Saved app.js and style.css successfully!")
