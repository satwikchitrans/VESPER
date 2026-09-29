"""
Fetch REAL road geometry from OpenStreetMap via OSRM public API.
This replaces the fake linear-interpolation paths with actual street-following coordinates.
"""
import urllib.request
import json
import math
import time
import sys

OSRM_BASE = "https://router.project-osrm.org/route/v1/driving"

def fetch_osrm_route(waypoints, overview="full"):
    """Query OSRM for a route through waypoints, return decoded geometry as [[lat,lng], ...]"""
    coords_str = ";".join(f"{wp[1]},{wp[0]}" for wp in waypoints)
    url = f"{OSRM_BASE}/{coords_str}?overview={overview}&geometries=geojson&steps=false"
    
    print(f"  Fetching OSRM route ({len(waypoints)} waypoints)...", end=" ", flush=True)
    
    req = urllib.request.Request(url, headers={"User-Agent": "VESPER-Prototype/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"FAILED: {e}")
        return None
    
    if data.get("code") != "Ok" or not data.get("routes"):
        print(f"FAILED: {data.get('code', 'unknown')}")
        return None
    
    route = data["routes"][0]
    geojson_coords = route["geometry"]["coordinates"]
    
    path = [[round(c[1], 5), round(c[0], 5)] for c in geojson_coords]
    
    dist_km = route["distance"] / 1000
    print(f"OK - {len(path)} points, {dist_km:.2f} km")
    return path


def haversine(p1, p2):
    lat1, lon1 = math.radians(p1[0]), math.radians(p1[1])
    lat2, lon2 = math.radians(p2[0]), math.radians(p2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def densify(path, max_gap_m=12.0):
    """Insert extra points so no two consecutive points are more than max_gap_m apart"""
    result = [path[0]]
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i+1]
        dist = haversine(p1, p2)
        steps = max(1, int(math.ceil(dist / max_gap_m)))
        for s in range(1, steps):
            t = s / float(steps)
            lat = round(p1[0] + (p2[0]-p1[0])*t, 5)
            lng = round(p1[1] + (p2[1]-p1[1])*t, 5)
            result.append([lat, lng])
        result.append(p2)
    return result


def validate_path(name, path):
    total_m = 0
    max_gap = 0
    for i in range(len(path)-1):
        d = haversine(path[i], path[i+1])
        total_m += d
        if d > max_gap:
            max_gap = d
    loop_gap = haversine(path[0], path[-1])
    print(f"  [{name}] {len(path)} pts | {total_m/1000:.2f} km | max gap: {max_gap:.1f}m | loop closure: {loop_gap:.1f}m")


# Corridor 1: Karol Bagh -> CP -> ITO -> Pragati Maidan
C1_WAYPOINTS = [
    [28.65136, 77.19067],
    [28.64650, 77.19550],
    [28.64300, 77.20100],
    [28.63980, 77.20750],
    [28.63700, 77.21000],
    [28.63280, 77.21970],
    [28.63150, 77.21672],
    [28.62900, 77.22800],
    [28.62788, 77.24369],
    [28.62200, 77.24500],
    [28.61545, 77.24843],
]

# Corridor 2: AIIMS -> Ring Road -> Moolchand -> Nehru Place
C2_WAYPOINTS = [
    [28.56544, 77.21015],
    [28.56880, 77.21600],
    [28.57093, 77.23908],
    [28.57004, 77.24220],
    [28.56200, 77.24800],
    [28.55500, 77.25000],
    [28.54921, 77.25270],
]

# Corridor 3: Dhaula Kuan -> Sardar Patel Marg -> India Gate
C3_WAYPOINTS = [
    [28.59216, 77.16162],
    [28.59700, 77.17200],
    [28.60350, 77.18350],
    [28.60600, 77.18730],
    [28.60800, 77.19700],
    [28.60900, 77.20400],
    [28.61296, 77.22766],
]

# Corridor 4: CP -> India Gate -> AIIMS -> Saket
C4_WAYPOINTS = [
    [28.63280, 77.21970],
    [28.61296, 77.22766],
    [28.60000, 77.22300],
    [28.58500, 77.21800],
    [28.56544, 77.21015],
    [28.55000, 77.21500],
    [28.52440, 77.21670],
]

CORRIDORS = [
    ("Corridor 1 (Karol Bagh - Pragati Maidan)", C1_WAYPOINTS),
    ("Corridor 2 (AIIMS - Nehru Place)", C2_WAYPOINTS),
    ("Corridor 3 (Dhaula Kuan - India Gate)", C3_WAYPOINTS),
    ("Corridor 4 (CP - AIIMS - Saket)", C4_WAYPOINTS),
]


def main():
    print("=" * 70)
    print("VESPER: Fetching REAL road geometry from OpenStreetMap/OSRM")
    print("=" * 70)
    
    all_paths = {}
    
    for i, (name, waypoints) in enumerate(CORRIDORS):
        print(f"\n[{i+1}/4] {name}")
        
        outbound = fetch_osrm_route(waypoints)
        if not outbound:
            print(f"  ERROR: Could not fetch route for {name}")
            sys.exit(1)
        
        time.sleep(1.5)
        
        return_wps = list(reversed(waypoints))
        return_path = fetch_osrm_route(return_wps)
        if not return_path:
            print(f"  ERROR: Could not fetch return route for {name}")
            sys.exit(1)
        
        time.sleep(1.5)
        
        full_path = outbound + return_path[1:]
        dense = densify(full_path, max_gap_m=12.0)
        validate_path(name, dense)
        all_paths[f"p{i+1}"] = dense
    
    # Save JSON
    with open("real_street_paths.json", "w") as f:
        json.dump(all_paths, f)
    print(f"\nSaved real_street_paths.json")
    
    # Write real_roads.js
    roads_js = "// AUTO-GENERATED: Real OpenStreetMap road geometry via OSRM\n"
    roads_js += "// DO NOT EDIT - regenerate with fetch_real_roads.py\n\n"
    for key, path in all_paths.items():
        var_name = f"REAL_ROAD_{key.upper()}"
        roads_js += f"const {var_name} = {json.dumps(path)};\n\n"
    
    with open("real_roads.js", "w", encoding="utf-8") as f:
        f.write(roads_js)
    print(f"Written real_roads.js")
    
    # Patch app.js
    print(f"\nPatching app.js...")
    
    with open("app.js", "r", encoding="utf-8") as f:
        app_js = f.read()
    
    lines = app_js.split("\n")
    new_lines = []
    i_line = 0
    while i_line < len(lines):
        line = lines[i_line]
        
        if "// Link dense roadPaths to BUS_ROUTES" in line or "// Link REAL OpenStreetMap" in line:
            new_lines.append("// Link REAL OpenStreetMap road paths to BUS_ROUTES and VEHICLES")
            new_lines.append("// (Generated from OSRM public routing API - actual street geometry)")
            new_lines.append("if (typeof REAL_ROAD_P1 !== 'undefined') {")
            new_lines.append("  VEHICLES[0].roadPath = REAL_ROAD_P1;")
            new_lines.append("  VEHICLES[1].roadPath = REAL_ROAD_P2;")
            new_lines.append("  VEHICLES[2].roadPath = REAL_ROAD_P3;")
            new_lines.append("  BUS_ROUTES[0].roadPath = REAL_ROAD_P1;")
            new_lines.append("  BUS_ROUTES[1].roadPath = REAL_ROAD_P2;")
            new_lines.append("  BUS_ROUTES[2].roadPath = REAL_ROAD_P3;")
            new_lines.append("  if (BUS_ROUTES[3]) BUS_ROUTES[3].roadPath = REAL_ROAD_P4;")
            new_lines.append("}")
            new_lines.append("")
            i_line += 1
            while i_line < len(lines):
                s = lines[i_line].strip()
                if s.startswith("if (BUS_ROUTES") or s.startswith("VEHICLES[") or s.startswith("BUS_ROUTES[") or s == "" or s == "}":
                    i_line += 1
                else:
                    break
            continue
        
        new_lines.append(line)
        i_line += 1
    
    with open("app.js", "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    print("Patched app.js")
    
    print(f"\nDONE. All entities now use real OSM road geometry.")


if __name__ == "__main__":
    main()
