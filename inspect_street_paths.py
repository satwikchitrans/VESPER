import json, re, math

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 # m
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def check_jumps(name, rpath):
    print(f'Checking {name} (total pts: {len(rpath)})...')
    large_jumps = []
    for i in range(len(rpath)-1):
        d = haversine(rpath[i][0], rpath[i][1], rpath[i+1][0], rpath[i+1][1])
        if d > 100:
            large_jumps.append((i, d, rpath[i], rpath[i+1]))
    print(f'  Found {len(large_jumps)} segments > 100m.')
    for j in large_jumps[:10]:
        print(f'    idx {j[0]}: {j[1]:.1f}m from {j[2]} to {j[3]}')

# Extract VEHICLES
for vid in ['VEH-001', 'VEH-002', 'VEH-003']:
    pos = text.find(f"id:'{vid}'")
    if pos == -1: pos = text.find(f'id:"{vid}"')
    rp_start = text.find('roadPath:', pos)
    rp_end = text.find(']]', rp_start) + 2
    pts = re.findall(r'\[\s*([0-9\.]+)\s*,\s*([0-9\.]+)\s*\]', text[rp_start:rp_end])
    coords = [[float(p[0]), float(p[1])] for p in pts]
    check_jumps(vid, coords)

# Also check BUS_ROUTES
m_bus = re.search(r'const BUS_ROUTES = (\[[\s\S]*?\]);', text)
if m_bus:
    bus_str = m_bus.group(1)
    for bus_id in ['BUS-DTC-419', 'BUS-DTC-522', 'BUS-DTC-764', 'BUS-DTC-335']:
        pos = bus_str.find(f"id: '{bus_id}'")
        if pos != -1:
            rp_start = bus_str.find('roadPath:', pos)
            if rp_start != -1:
                rp_end = bus_str.find(']]', rp_start) + 2
                pts = re.findall(r'\[\s*([0-9\.]+)\s*,\s*([0-9\.]+)\s*\]', bus_str[rp_start:rp_end])
                coords = [[float(p[0]), float(p[1])] for p in pts]
                check_jumps(bus_id, coords)
