# -*- coding: utf-8 -*-
"""
Apply IRCTC-inspired color palette (blue #213d77, orange, white) across
the entire VESPER style.css.  Only colors change — no layout, no sizing,
no structural edits.
"""
import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# ─── 1. Rewrite :root color tokens ─────────────────────────────────
old_root = """:root {
  --bg-primary: #080c16;
  --bg-secondary: #0d1527;
  --bg-tertiary: #131f37;
  --bg-card: rgba(15, 23, 42, 0.88);
  --bg-glass: rgba(13, 21, 39, 0.85);
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-medium: rgba(255, 255, 255, 0.14);
  --border-accent: #00f0ff;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #64748b;
  --accent-cyan: #00f0ff;
  --accent-blue: #38bdf8;
  --accent-indigo: #818cf8;
  --accent-purple: #a855f7;
  --accent-green: #10b981;
  --accent-lime: #22c55e;
  --accent-yellow: #fbbf24;
  --accent-orange: #f97316;
  --accent-red: #ef4444;
  --accent-pink: #ec4899;
  --shadow-glow-cyan: 0 0 16px rgba(0, 240, 255, 0.25);
  --shadow-glow-red: 0 0 16px rgba(239, 68, 68, 0.35);"""

new_root = """:root {
  --bg-primary: #f4f6fb;
  --bg-secondary: #213d77;
  --bg-tertiary: #1a3160;
  --bg-card: rgba(255, 255, 255, 0.96);
  --bg-glass: rgba(33, 61, 119, 0.92);
  --border-subtle: rgba(33, 61, 119, 0.12);
  --border-medium: rgba(33, 61, 119, 0.22);
  --border-accent: #ec6e2a;
  --text-primary: #1a1a2e;
  --text-secondary: #4a5568;
  --text-muted: #718096;
  --accent-cyan: #ec6e2a;
  --accent-blue: #213d77;
  --accent-indigo: #2c4f8a;
  --accent-purple: #213d77;
  --accent-green: #10b981;
  --accent-lime: #22c55e;
  --accent-yellow: #ec6e2a;
  --accent-orange: #ec6e2a;
  --accent-red: #ef4444;
  --accent-pink: #ec6e2a;
  --shadow-glow-cyan: 0 0 12px rgba(236, 110, 42, 0.25);
  --shadow-glow-red: 0 0 12px rgba(239, 68, 68, 0.25);"""

css = css.replace(old_root, new_root)

# ─── 2. Broad sweeping color replacements ───────────────────────────
# Map old dark-mode backgrounds → IRCTC blue/white
color_map = {
    # Dark backgrounds → IRCTC blue or white
    '#080c16':  '#f4f6fb',
    '#0d1527':  '#213d77',
    '#131f37':  '#1a3160',
    '#0b111e':  '#213d77',
    '#0b1322':  '#e8edf5',
    '#0f172a':  '#213d77',
    '#0a0e17':  '#f4f6fb',
    '#0e1525':  '#213d77',
    '#0a1020':  '#213d77',
    '#0c1525':  '#213d77',
    '#0e1a2e':  '#1a3160',
    '#101828':  '#213d77',
    '#111827':  '#213d77',
    '#1e293b':  '#2c4f8a',
    '#1f2937':  '#2c4f8a',
    '#334155':  '#4a6ba5',
    '#374151':  '#4a6ba5',

    # Neon cyan → IRCTC orange accent
    '#00f0ff':  '#ec6e2a',
    '#00d2df':  '#d4601f',
    '#00e4f5':  '#ec6e2a',
    '#06b6d4':  '#ec6e2a',
    '#22d3ee':  '#ec6e2a',
    '#67e8f9':  '#f59e0b',

    # Purple/indigo → blue
    '#a855f7':  '#213d77',
    '#818cf8':  '#2c4f8a',
    '#6366f1':  '#213d77',
    '#8b5cf6':  '#213d77',

    # Pink → orange
    '#ec4899':  '#ec6e2a',
    '#f472b6':  '#ec6e2a',

    # Keep functional orange as IRCTC orange
    '#f97316':  '#ec6e2a',
    '#fb792b':  '#ec6e2a',
    '#ea580c':  '#d4601f',
    '#f59e0b':  '#ec6e2a',
    '#fbbf24':  '#ec6e2a',

    # Light text on dark → ensure readability
    '#f8fafc':  '#ffffff',
    '#e2e8f0':  '#e8edf5',
    '#cbd5e1':  '#c5d0e0',
}

for old_color, new_color in color_map.items():
    css = css.replace(old_color, new_color)

# ─── 3. Fix specific rgba patterns used heavily ────────────────────
# Cyan rgba glows → orange glows
css = re.sub(r'rgba\(0,\s*240,\s*255,', 'rgba(236, 110, 42,', css)
css = re.sub(r'rgba\(0,\s*224,\s*245,', 'rgba(236, 110, 42,', css)
css = re.sub(r'rgba\(6,\s*182,\s*212,', 'rgba(236, 110, 42,', css)
css = re.sub(r'rgba\(34,\s*211,\s*238,', 'rgba(236, 110, 42,', css)

# Purple rgba → blue
css = re.sub(r'rgba\(168,\s*85,\s*247,', 'rgba(33, 61, 119,', css)
css = re.sub(r'rgba\(129,\s*140,\s*248,', 'rgba(33, 61, 119,', css)

# Pink rgba → orange
css = re.sub(r'rgba\(236,\s*72,\s*153,', 'rgba(236, 110, 42,', css)

# Dark-mode card bg rgba → white card
css = re.sub(r'rgba\(15,\s*23,\s*42,\s*0\.88\)', 'rgba(255, 255, 255, 0.96)', css)
css = re.sub(r'rgba\(13,\s*21,\s*39,\s*0\.85\)', 'rgba(33, 61, 119, 0.92)', css)
css = re.sub(r'rgba\(15,\s*23,\s*42,\s*0\.9[0-9]*\)', 'rgba(33, 61, 119, 0.94)', css)
css = re.sub(r'rgba\(11,\s*17,\s*32,\s*0\.9[0-9]*\)', 'rgba(33, 61, 119, 0.96)', css)
css = re.sub(r'rgba\(13,\s*21,\s*39,\s*0\.9[0-9]*\)', 'rgba(33, 61, 119, 0.94)', css)
css = re.sub(r'rgba\(10,\s*16,\s*30,', 'rgba(33, 61, 119,', css)
css = re.sub(r'rgba\(8,\s*12,\s*22,', 'rgba(26, 49, 96,', css)

# ─── 4. Top bar: make it IRCTC deep blue header ────────────────────
css = css.replace(
    'background: rgba(11, 17, 32, 0.95);',
    'background: #213d77;'
)

# ─── 5. Fix scrollbar thumb hover (was cyan) ───────────────────────
css = css.replace(
    'background: var(--accent-cyan);',
    'background: #ec6e2a;'
)

# ─── 6. Body background ────────────────────────────────────────────
css = css.replace(
    'background: var(--bg-primary);',
    'background: #f4f6fb;'
)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Applied IRCTC color palette (blue #213d77, orange #ec6e2a, white) across all sections.')
