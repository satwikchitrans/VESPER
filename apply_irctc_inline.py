# -*- coding: utf-8 -*-
"""
Apply IRCTC color palette to inline styles in index.html and app.js.
Only colors — no layout or structure changes.
"""
import re

for fname in ['index.html', 'app.js']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Map old colors → IRCTC palette
    replacements = {
        # Cyan/neon → orange
        '#00f0ff': '#ec6e2a',
        '#00d2df': '#d4601f',
        '#00e4f5': '#ec6e2a',
        '#06b6d4': '#ec6e2a',
        '#22d3ee': '#ec6e2a',
        '#67e8f9': '#ec6e2a',

        # Dark backgrounds → IRCTC blue
        '#0b111e': '#213d77',
        '#0d1527': '#213d77',
        '#0f172a': '#213d77',
        '#131f37': '#1a3160',
        '#0b1322': '#e8edf5',
        '#080c16': '#f4f6fb',
        '#0a0e17': '#f4f6fb',
        '#0e1525': '#213d77',
        '#0c1525': '#213d77',
        '#101828': '#213d77',
        '#1e293b': '#2c4f8a',
        '#334155': '#4a6ba5',

        # Purple/indigo → blue
        '#a855f7': '#213d77',
        '#818cf8': '#2c4f8a',
        '#6366f1': '#213d77',
        '#8b5cf6': '#213d77',

        # Pink → orange
        '#ec4899': '#ec6e2a',

        # Orange variants → unified IRCTC orange
        '#f97316': '#ec6e2a',
        '#fb792b': '#ec6e2a',
        '#ea580c': '#d4601f',
        '#f59e0b': '#ec6e2a',
        '#fbbf24': '#ec6e2a',
        '#d97706': '#d4601f',

        # Accent blue → IRCTC blue
        '#38bdf8': '#213d77',
        '#3b82f6': '#213d77',
        '#2563eb': '#213d77',
        '#1d4ed8': '#1a3160',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Fix rgba patterns for cyan glow
    content = re.sub(r'rgba\(0,\s*240,\s*255,', 'rgba(236, 110, 42,', content)
    content = re.sub(r'rgba\(0,\s*224,\s*245,', 'rgba(236, 110, 42,', content)
    content = re.sub(r'rgba\(6,\s*182,\s*212,', 'rgba(236, 110, 42,', content)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Applied IRCTC colors to {fname}')

print('Done. All inline colors updated.')
