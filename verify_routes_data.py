import re
import math
import json

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000 # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Let's extract VEHICLES array
m = re.search(r'const VEHICLES = (\[[\s\S]*?\]);\s*const HOTLIST', content)
if m:
    veh_str = m.group(1)
    # Parse roadPaths
    for vid in ['VEH-001', 'VEH-002', 'VEH-003']:
        pos = veh_str.find(f"id:'{vid}'")
        if pos == -1:
            pos = veh_str.find(f'id:"{vid}"')
        if pos != -1:
            rp_start = veh_str.find('roadPath:', pos)
            rp_end = veh_str.find(']]', rp_start) + 2
            rp_content = veh_str[rp_start + 9:rp_end].strip()
            # extract all [lat, lng]
            pts = re.findall(r'\[\s*([0-9\.]+)\s*,\s*([0-9\.]+)\s*\]', rp_content)
            coords = [[float(p[0]), float(p[1])] for p in pts]
            total_dist = sum(haversine_m(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1]) for i in range(len(coords)-1))
            start_end_dist = haversine_m(coords[0][0], coords[0][1], coords[-1][0], coords[-1][1])
            print(f"{vid}: {len(coords)} points, Total Road Distance: {total_dist/1000:.2f} km, Start-End Gap: {start_end_dist:.1f} m")

print("\n--- Bus Routes analysis ---")
m_bus = re.search(r'const BUS_ROUTES = (\[[\s\S]*?\]);', content)
if m_bus:
    print("Found BUS_ROUTES:", m_bus.group(1)[:200])
