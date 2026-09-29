import re
import json

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Let's inspect BUS_ROUTES and VEHICLES
bus_routes_match = re.search(r'const BUS_ROUTES = (\[[\s\S]*?\]);', code)
if bus_routes_match:
    print("Found BUS_ROUTES definition in app.js")

vehicles_match = re.search(r'const VEHICLES = (\[[\s\S]*?\]);\s*const HOTLIST', code)
if vehicles_match:
    print("Found VEHICLES definition in app.js")
