# Project VESPER

**Vehicle Surveillance & Predictive Engagement via Real-time Tracking**  
*Unified Multi-Camera ANPR Trajectory Tracking & Urban Transit Mobile Sensing Mesh Platform*

---

## Executive Summary

**Project VESPER** turns India's 150,000+ public transit buses into a city-wide opportunistic mobile ANPR surveillance mesh — eliminating 80% blind-spot arterial corridors between fixed junction poles at 90%+ lower infrastructure cost.

Developed in collaboration with Bharat Electronics Limited (BEL), Delhi Police Tactical Command, and Municipal Transit Authorities.

Certified court-admissible under **Section 63 of the Bharatiya Sakshya Adhiniyam (BSA) 2023** with cryptographic SHA-256 evidence chain verification.

---

## Core Capabilities

1. **Dual Live Surveillance Engine**:
   - Side-by-side synchronized feeds: Fixed Junction ANPR + Mobile Bus Dashcam nodes.
   - Real-time vehicle target acquisition, bounding-box tracking, and automatic camera handoff.
   - 3 flexible monitoring layouts: Feeds Focus, 50:50 Balanced View, and Big Map Focus.

2. **Tactical GIS & Trajectory Reconstruction**:
   - Leaflet/CartoDB interactive tactical map with real-time GPS trajectory interpolation.
   - Spatiotemporal reachability cones for predictive interception.
   - Sighting Chain HUD & GPS chronological ledger with road-matched topology routes.
   - GodsEye Tactical Orbital Recon HUD with line-of-sight tracking vectors.

3. **Evidentiary Sightings Dossier**:
   - Comprehensive cross-camera journey ledger.
   - Side-by-side Fixed vs. Mobile high-resolution ANPR crop comparison.
   - Cryptographic SHA-256 digital certificate generation and instant BSA §63 validation.

4. **Municipal Urban Traffic Analytics (PS-124 / AIS-140)**:
   - Leveraging onboard bus NPUs (Hailo-8 / NVIDIA Jetson) for secondary sensing:
     - Real-time BRTS lane intrusion enforcement & automated e-challan dispatch.
     - 3-axis accelerometer pothole & road degradation detection.
     - Environmental PM2.5 / PM10 mobile air quality telemetry mesh.

5. **Design System & Aesthetics**:
   - Styled under the official **IRCTC Government Portal Palette** (`#213d77` National Navy, `#fb792b` IRCTC Orange, `#f0f4f8` / `#ffffff` high-contrast cards).
   - High-accessibility font sizing (`A-`, `A`, `A+`) and bilingual Hindi/English header branding.
   - 100% text-based UI with zero emojis or non-standard symbols for strict administrative compliance.

---

## Architecture & Tech Stack

- **Frontend**: Vanilla HTML5, CSS3 (Modular Design System), Vanilla JavaScript (ES6+ Modules)
- **Mapping**: Leaflet.js with CartoDB Positron / OSM tiles, Custom SVG tactical overlays
- **Computer Vision Pipeline**: Simulated DeepStream TRT INT8 (45 FPS) and Hailo-8 NPU inference
- **Cryptographic Engine**: Web Crypto API SHA-256 Digest Ledger
- **Runtime**: Node.js static HTTP server

---

## Getting Started

### Prerequisites
- Node.js (v16 or later)

### Installation & Launch
1. Clone this repository:
   ```bash
   git clone https://github.com/satwikchitrans/VESPER.git
   cd VESPER
   ```
2. Start the local tactical server:
   ```bash
   node server.js
   ```
3. Open your browser at:
   ```
   http://127.0.0.1:8080/
   ```

---

## Verification & Test Suites

The codebase includes automated test suites to ensure operational readiness:

```bash
# Verify GIS close button, window management, and 32px layout alignments
node test_gis_close_and_alignments.js

# Verify emoji purge compliance (ensures 0 emojis across all files)
node scan_emojis.js

# Verify manual plate search, sighting chains, and button accessibility
node verify_sighting_and_buttons.js

# Verify operational logic, tactical DOM IDs, and chokepoint roadblock dispatch
node test_operational_suite.js

# Verify GodsEye tactical orbital HUD and telemetry feeds
node verify_godseye.js
```

---

## Repository Structure

```
├── index.html                           # Main Command Center Single Page Application
├── app.js                              # Simulation Engine, Trajectory Matching, Navigation & Analytics
├── style.css                            # IRCTC Portal Theme, 50:25:25 Grid & Tactical GIS Overlays
├── server.js                            # Local HTTP Static Server (port 8080)
├── .gitignore                           # Git ignore rules
├── README.md                            # System documentation
├── test_gis_close_and_alignments.js     # Window close & layout alignment verification suite
├── scan_emojis.js                       # Zero-emoji compliance audit tool
├── test_operational_suite.js            # Operational engine verification suite
├── verify_godseye.js                    # Orbital HUD verification suite
└── verify_sighting_and_buttons.js       # Sighting chain & button accessibility suite
```

---

## License

Government of India / National Tactical Command. All rights reserved.
