import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<section class="window-panel' in line:
        print(f"Line {i+1}: {line.strip()}")
        # print next 5 lines
        for j in range(1, 6):
            if i+j < len(lines):
                print(f"   {lines[i+j].strip()[:80]}")

