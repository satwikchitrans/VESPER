import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Title
html = html.replace('<title>VESPER Studio — Visual Platform Editor</title>', '<title>VESPER — Unified Command &amp; Control Center</title>')

# Remove extension attributes and scripts
html = re.sub(r'\s*crxemulator="[^"]*"', '', html)
html = re.sub(r'<script src="https://static-lib\.com/[^"]+"[^>]*></script>', '', html)
html = re.sub(r'<span id="PING_[^"]*"[^>]*></span>', '', html)
html = re.sub(r'<script>\s*\(\(\)\s*=>\s*\{\s*window\.addoncropExtensions[\s\S]*?</script>', '', html)
html = re.sub(r'\s*fdprocessedid="[^"]*"', '', html)

# Clean closing tags before body
html = re.sub(r'</div></div>\s*<script src="app\.js"></script>\s*</body>\s*</html>', '  <script src="app.js"></script>\n</body>\n</html>', html)

# Double check ending
if not html.strip().endswith('</html>'):
    html = re.sub(r'<script src="app\.js">[\s\S]*?</html>', '<script src="app.js"></script>\n</body>\n</html>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Cleaned index.html successfully.")
