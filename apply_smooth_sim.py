import re
import json
import math

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# 1. Generate Route 335 dense points
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

def interpolate_segment(p1, p2, step_m=20.0):
    lat1, lng1 = p1
    lat2, lng2 = p2
    dx = (lng2 - lng1) * 111320 * math.cos(math.radians((lat1+lat2)/2))
    dy = (lat2 - lat1) * 110540
    dist = math.sqrt(dx*dx + dy*dy)
    num_steps = max(1, int(dist / step_m))
    res = []
    for s in range(num_steps):
        t = s / float(num_steps)
        res.append([round(lat1 + (lat2 - lat1)*t, 5), round(lng1 + (lng2 - lng1)*t, 5)])
    return res

p4 = []
for i in range(len(r335_waypoints)-1):
    p4.extend(interpolate_segment(r335_waypoints[i], r335_waypoints[i+1], step_m=20.0))
p4.append(r335_waypoints[-1])

p4_json = json.dumps(p4)

# Replace BUS_ROUTES definition in app.js
new_bus_routes = f"""const BUS_ROUTES = [
  {{ id: 'BUS-DTC-419', name: 'Route 419 DOWN', route: 'Karol Bagh - CP - ITO - Pragati Maidan', speedKmh: 34,
    waypoints: [{{lat:28.6514,lng:77.1907}},{{lat:28.6430,lng:77.2010}},{{lat:28.6370,lng:77.2100}},{{lat:28.6315,lng:77.2167}},{{lat:28.6278,lng:77.2300}},{{lat:28.6278,lng:77.2437}},{{lat:28.6200,lng:77.2479}},{{lat:28.6163,lng:77.2479}}] }},
  {{ id: 'BUS-DTC-522', name: 'Route 522 UP', route: 'AIIMS - Moolchand - Lajpat - Nehru Place', speedKmh: 36,
    waypoints: [{{lat:28.5672,lng:77.2100}},{{lat:28.5690,lng:77.2200}},{{lat:28.5704,lng:77.2388}},{{lat:28.5650,lng:77.2450}},{{lat:28.5560,lng:77.2500}},{{lat:28.5491,lng:77.2533}}] }},
  {{ id: 'BUS-DTC-764', name: 'Route 764 RING', route: 'Dhaula Kuan - India Gate - Saket', speedKmh: 38,
    waypoints: [{{lat:28.5922,lng:77.1616}},{{lat:28.5980,lng:77.1800}},{{lat:28.6050,lng:77.1980}},{{lat:28.6129,lng:77.2100}},{{lat:28.6129,lng:77.2295}},{{lat:28.5900,lng:77.2250}},{{lat:28.5600,lng:77.2200}},{{lat:28.5244,lng:77.2167}}] }},
  {{ id: 'BUS-DTC-335', name: 'Route 335 EXPRESS', route: 'CP - India Gate - AIIMS - Saket', speedKmh: 35,
    waypoints: [{{lat:28.6328,lng:77.2197}},{{lat:28.6280,lng:77.2240}},{{lat:28.6200,lng:77.2280}},{{lat:28.6129,lng:77.2295}},{{lat:28.5950,lng:77.2200}},{{lat:28.5800,lng:77.2150}},{{lat:28.5672,lng:77.2100}},{{lat:28.5450,lng:77.2150}},{{lat:28.5244,lng:77.2167}}],
    roadPath: {p4_json} }},
];"""

code = re.sub(r'const BUS_ROUTES = \[[\s\S]*?\];', new_bus_routes, code, count=1)
print("Updated BUS_ROUTES definition")

# Let's link roadPath for bus routes after VEHICLES is defined
link_bus_paths_code = """
// Link dense roadPaths to BUS_ROUTES
if (BUS_ROUTES[0] && VEHICLES[0]) BUS_ROUTES[0].roadPath = VEHICLES[0].roadPath;
if (BUS_ROUTES[1] && VEHICLES[1]) BUS_ROUTES[1].roadPath = VEHICLES[1].roadPath;
if (BUS_ROUTES[2] && VEHICLES[2]) BUS_ROUTES[2].roadPath = VEHICLES[2].roadPath;
// Set realistic velocities
if (VEHICLES[0]) VEHICLES[0].speedKmh = 44; // Normal Dzire
if (VEHICLES[1]) VEHICLES[1].speedKmh = 56; // Stolen Fortuner (high speed fleeing)
if (VEHICLES[2]) VEHICLES[2].speedKmh = 40; // i20 Hatchback
"""

# Insert link_bus_paths_code right after const VEHICLES = [...];
veh_end = code.find('const HOTLIST = [')
if veh_end != -1:
    code = code[:veh_end] + link_bus_paths_code + "\n" + code[veh_end:]
    print("Inserted bus path linkage")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved stage 1 of app.js")
