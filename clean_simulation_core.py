import re

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# 1. Clean startVehicleRoadGlide (Remove busScannerCones circles completely)
new_glide = """function startVehicleRoadGlide() {
  if (STATE.timers.vehicleGlide) clearInterval(STATE.timers.vehicleGlide);
  if (STATE.timers.bus) clearInterval(STATE.timers.bus);

  const TICK_MS = 50;
  const dt = TICK_MS / 1000; // 0.05 seconds

  STATE.timers.vehicleGlide = setInterval(() => {
    if (STATE.isSimPaused) return;

    // 1. Update all DTC Transit Buses smoothly along street centerlines
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
    });

    // 2. Update all Vehicles smoothly along street centerlines
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
}"""

code = re.sub(r'function startVehicleRoadGlide\(\)\s*\{[\s\S]*?function moveBuses\(\)\s*\{[\s\S]*?\}\s*\}', new_glide + "\n\nfunction moveBuses() {}\n", code, count=1)
print("Cleaned startVehicleRoadGlide")

# 2. In startSimulation, remove STATE.timers.bus = setInterval(moveBuses...
code = re.sub(r'\/\/ Move buses\s*STATE\.timers\.bus = setInterval\(moveBuses, CONFIG\.SIM_SPEED\);', '// Unified transit & vehicle motion handled in startVehicleRoadGlide', code, count=1)
print("Removed old moveBuses interval in startSimulation")

# 3. Remove duplicate function moveBuses() at bottom of file
code = re.sub(r'function moveBuses\(\)\s*\{[\s\S]*?STATE\.simTick\+\+;\s*\}', '// (Duplicate moveBuses removed - unified engine in startVehicleRoadGlide)', code, count=1)
print("Removed duplicate moveBuses at bottom of file")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved cleaned app.js successfully!")
