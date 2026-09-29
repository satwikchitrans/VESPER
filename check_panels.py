import re

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

print("--- Panels ---")
for m in re.finditer(r'<section[^>]+id="(window-[^"]+)"[^>]*>', h):
    print(m.group(0))

print("--- Tabs ---")
for m in re.finditer(r'<button[^>]+data-window="([^"]+)"[^>]*>', h):
    print(m.group(0))
