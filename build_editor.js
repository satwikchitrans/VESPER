const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'index.html');
const editorPath = path.join(__dirname, 'editor.html');

let html = fs.readFileSync(indexPath, 'utf8');

// Replace app.js script with editor.js
html = html.replace(/<script src="app\.js"><\/script>/g, '<script src="editor.js"></script>');
html = html.replace(/<script src="live-edit\.js"><\/script>/g, '');

// Update title in editor.html
html = html.replace('<title>VESPER — Unified Command &amp; Control Center</title>', '<title>VESPER Studio — Visual Platform Editor</title>');

fs.writeFileSync(editorPath, html, 'utf8');
console.log('Successfully generated editor.html:', fs.statSync(editorPath).size, 'bytes');
