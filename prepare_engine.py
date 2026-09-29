import re
import json
import math

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_code = f.read()

# Generate Route 335 waypoints & dense points
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

print(f"Dense p4 created: {len(p4)} points")
