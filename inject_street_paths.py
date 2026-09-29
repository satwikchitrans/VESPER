import json
import re
import math

with open('street_paths.json', 'r') as f:
    streets = json.load(f)

p1 = streets['p1']
p2 = streets['p2']
p3 = streets['p3']
p4 = streets['p4']

def haversine(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2
    R = 6371000 # m
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def find_nearest_idx(path, target_lat, target_lng):
    best_idx = 0
    min_d = float('inf')
    for i, pt in enumerate(path):
        d = haversine(pt, [target_lat, target_lng])
        if d < min_d:
            min_d = d
            best_idx = i
    return best_idx, min_d

# Checkpoints for VEH-001
c1_checks = [
    {'cam':'CAM-JNC-04', 'lat':28.65136, 'lng':77.19067},
    {'cam':'BUS-DTC-419', 'lat':28.63706, 'lng':77.21005},
    {'cam':'CAM-JNC-01', 'lat':28.6315, 'lng':77.21672},
    {'cam':'CAM-JNC-02', 'lat':28.62788, 'lng':77.24369},
    {'cam':'CAM-JNC-10', 'lat':28.61545, 'lng':77.24843},
]
for c in c1_checks:
    idx, d = find_nearest_idx(p1, c['lat'], c['lng'])
    c['pathIdx'] = idx
    print(f"VEH-001 {c['cam']} -> pathIdx {idx} (snap dist: {d:.1f}m)")

# Checkpoints for VEH-002
c2_checks = [
    {'cam':'CAM-JNC-05', 'lat':28.56544, 'lng':77.21015},
    {'cam':'BUS-DTC-522', 'lat':28.57093, 'lng':77.23908},
    {'cam':'CAM-JNC-08', 'lat':28.57004, 'lng':77.2422},
    {'cam':'CAM-JNC-07', 'lat':28.54921, 'lng':77.2527},
]
for c in c2_checks:
    idx, d = find_nearest_idx(p2, c['lat'], c['lng'])
    c['pathIdx'] = idx
    print(f"VEH-002 {c['cam']} -> pathIdx {idx} (snap dist: {d:.1f}m)")

# Checkpoints for VEH-003
c3_checks = [
    {'cam':'CAM-JNC-09', 'lat':28.59216, 'lng':77.16162},
    {'cam':'BUS-DTC-764', 'lat':28.60513, 'lng':77.1981},
    {'cam':'CAM-JNC-11', 'lat':28.61296, 'lng':77.22766},
]
for c in c3_checks:
    idx, d = find_nearest_idx(p3, c['lat'], c['lng'])
    c['pathIdx'] = idx
    print(f"VEH-003 {c['cam']} -> pathIdx {idx} (snap dist: {d:.1f}m)")

# Read app.js
with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

# Build updated VEHICLES definition with strictly street-aligned paths
p1_str = json.dumps(p1)
p2_str = json.dumps(p2)
p3_str = json.dumps(p3)
p4_str = json.dumps(p4)

new_vehicles_code = f"""const VEHICLES = [
  {{ id:'VEH-001', plate:'DL 1C AE 4921', type:'Sedan', color:'White', make:'Maruti Swift Dzire', status:'tracking', isStolen:false, reidHash:'a4f891b2', speedKmh: 44,
    corridorName: 'Pusa Road - Panchkuian Marg - Connaught Place - ITO - Pragati Maidan Corridor',
    trajectory: [
      {{cam:'CAM-JNC-04',time:0,lat:28.65136,lng:77.19067,conf:0.96,street:'Pusa Road Crossing (Karol Bagh)',pathIdx:{c1_checks[0]['pathIdx']}}},
      {{cam:'BUS-DTC-419',time:4,lat:28.63706,lng:77.21005,conf:0.82,mobile:true,street:'Panchkuian Marg (Mobile Intercept)',pathIdx:{c1_checks[1]['pathIdx']}}},
      {{cam:'CAM-JNC-01',time:7,lat:28.6315,lng:77.21672,conf:0.97,street:'Connaught Place Outer Circle',pathIdx:{c1_checks[2]['pathIdx']}}},
      {{cam:'CAM-JNC-02',time:12,lat:28.62788,lng:77.24369,conf:0.94,street:'ITO Flyover / Vikas Marg',pathIdx:{c1_checks[3]['pathIdx']}}},
      {{cam:'CAM-JNC-10',time:16,lat:28.61545,lng:77.24843,conf:0.91,street:'Pragati Maidan / Mathura Rd',pathIdx:{c1_checks[4]['pathIdx']}}},
    ],
    roadPath: {p1_str}
  }},
  {{ id:'VEH-002', plate:'UP 16 AB 7843', type:'SUV', color:'Black', make:'Toyota Fortuner', status:'tracking', isStolen:true, reidHash:'c3d20e6f', speedKmh: 56,
    corridorName: 'AIIMS Flyover - Mahatma Gandhi Ring Road - Moolchand - Lajpat Nagar - Nehru Place',
    trajectory: [
      {{cam:'CAM-JNC-05',time:0,lat:28.56544,lng:77.21015,conf:0.93,street:'AIIMS Flyover',pathIdx:{c2_checks[0]['pathIdx']}}},
      {{cam:'BUS-DTC-522',time:3,lat:28.57093,lng:77.23908,conf:0.78,mobile:true,street:'Moolchand Metro Corridor',pathIdx:{c2_checks[1]['pathIdx']}}},
      {{cam:'CAM-JNC-08',time:6,lat:28.57004,lng:77.2422,conf:0.95,street:'Lajpat Nagar Flyover',pathIdx:{c2_checks[2]['pathIdx']}}},
      {{cam:'CAM-JNC-07',time:10,lat:28.54921,lng:77.2527,conf:0.89,street:'Nehru Place Outer Ring',pathIdx:{c2_checks[3]['pathIdx']}}},
    ],
    roadPath: {p2_str}
  }},
  {{ id:'VEH-003', plate:'HR 26 DK 9912', type:'Hatchback', color:'Red', make:'Hyundai i20', status:'lost', isStolen:false, reidHash:'f7a913dd', speedKmh: 40,
    corridorName: 'Dhaula Kuan Interchange - Sardar Patel Marg - Teen Murti - India Gate C-Hexagon',
    trajectory: [
      {{cam:'CAM-JNC-09',time:0,lat:28.59216,lng:77.16162,conf:0.91,street:'Dhaula Kuan Junction',pathIdx:{c3_checks[0]['pathIdx']}}},
      {{cam:'BUS-DTC-764',time:5,lat:28.60513,lng:77.1981,conf:0.68,mobile:true,street:'Panchsheel Marg Corridor',pathIdx:{c3_checks[1]['pathIdx']}}},
      {{cam:'CAM-JNC-11',time:9,lat:28.61296,lng:77.22766,conf:0.88,street:'India Gate Circle',pathIdx:{c3_checks[2]['pathIdx']}}},
    ],
    roadPath: {p3_str}
  }}
];"""

# Replace VEHICLES in app.js
app_js = re.sub(r'const VEHICLES = \[[\s\S]*?\];\s*(?=\/\/ Link dense roadPaths|const HOTLIST)', new_vehicles_code + "\n\n", app_js, count=1)

# Update BUS_ROUTES roadPath linkage
bus_linkage = f"""// Link dense roadPaths to BUS_ROUTES
if (BUS_ROUTES[0]) BUS_ROUTES[0].roadPath = VEHICLES[0].roadPath;
if (BUS_ROUTES[1]) BUS_ROUTES[1].roadPath = VEHICLES[1].roadPath;
if (BUS_ROUTES[2]) BUS_ROUTES[2].roadPath = VEHICLES[2].roadPath;
if (BUS_ROUTES[3]) BUS_ROUTES[3].roadPath = {p4_str};
"""

app_js = re.sub(r'\/\/ Link dense roadPaths to BUS_ROUTES[\s\S]*?if \(VEHICLES\[2\]\) VEHICLES\[2\]\.speedKmh = 40; \/\/ i20 Hatchback', bus_linkage, app_js, count=1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Injected street-aligned roadPaths into app.js successfully!")
