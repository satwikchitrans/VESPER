import re
import json
import math

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Let's extract VEHICLES roadPath for VEH-001, VEH-002, VEH-003
def extract_road_path(vid):
    pos = code.find(f"id:'{vid}'")
    if pos == -1: pos = code.find(f'id:"{vid}"')
    rp_start = code.find('roadPath:', pos)
    rp_end = code.find(']]', rp_start) + 2
    rp_content = code[rp_start + 9:rp_end].strip()
    pts = re.findall(r'\[\s*([0-9\.]+)\s*,\s*([0-9\.]+)\s*\]', rp_content)
    return [[float(p[0]), float(p[1])] for p in pts]

p1 = extract_road_path('VEH-001') # Karol Bagh - CP - ITO - Pragati Maidan loop (794 pts)
p2 = extract_road_path('VEH-002') # AIIMS - Moolchand - Lajpat - Nehru Place loop (560 pts)
p3 = extract_road_path('VEH-003') # Dhaula Kuan - Teen Murti - India Gate loop (636 pts)

# Route 335: CP -> Janpath -> India Gate -> Lodhi Rd -> AIIMS -> Saket loop
# Let's create high-density road path connecting CP to Saket and returning
def interpolate_segment(p_start, p_end, step_m=15.0):
    # simple linear interpolation between points
    lat1, lng1 = p_start
    lat2, lng2 = p_end
    # meters approx
    dx = (lng2 - lng1) * 111320 * math.cos(math.radians((lat1+lat2)/2))
    dy = (lat2 - lat1) * 110540
    dist = math.sqrt(dx*dx + dy*dy)
    num_steps = max(1, int(dist / step_m))
    res = []
    for s in range(num_steps):
        t = s / float(num_steps)
        res.append([round(lat1 + (lat2 - lat1)*t, 5), round(lng1 + (lng2 - lng1)*t, 5)])
    return res

# Route 335 key road corridors in Delhi:
# CP Outer Circle (28.6328, 77.2197) -> Janpath -> Rajpath / India Gate (28.6129, 77.2276)
# -> National Gallery / Shahjahan Rd -> Lodhi Garden / Jor Bagh (28.5860, 77.2210)
# -> Sri Aurobindo Marg -> AIIMS / Safdarjung (28.5672, 77.2100)
# -> Green Park -> Hauz Khas Metro (28.5440, 77.2065) -> Press Enclave Rd / Saket Select City (28.5244, 77.2167)
# -> Return via Mehrauli-Badarpur Rd -> Sri Aurobindo Marg -> Janpath -> CP
r335_waypoints = [
    [28.6328, 77.2197], [28.6300, 77.2205], [28.6250, 77.2220], [28.6190, 77.2245],
    [28.6129, 77.2276], [28.6050, 77.2260], [28.5950, 77.2220], [28.5860, 77.2210],
    [28.5770, 77.2160], [28.5672, 77.2100], [28.5580, 77.2070], [28.5440, 77.2065],
    [28.5350, 77.2100], [28.5244, 77.2167],
    # Return loop
    [28.5255, 77.2175], [28.5360, 77.2110], [28.5450, 77.2075], [28.5590, 77.2080],
    [28.5680, 77.2110], [28.5780, 77.2170], [28.5870, 77.2215], [28.5960, 77.2225],
    [28.6060, 77.2265], [28.6135, 77.2280], [28.6200, 77.2250], [28.6260, 77.2225],
    [28.6310, 77.2210], [28.6328, 77.2197]
]

p4 = []
for i in range(len(r335_waypoints)-1):
    p4.extend(interpolate_segment(r335_waypoints[i], r335_waypoints[i+1], step_m=20.0))
p4.append(r335_waypoints[-1])

print(f"Generated Route 335 dense path: {len(p4)} coordinates")
print(f"Bus 419 path points: {len(p1)}")
print(f"Bus 522 path points: {len(p2)}")
print(f"Bus 764 path points: {len(p3)}")
print(f"Bus 335 path points: {len(p4)}")
