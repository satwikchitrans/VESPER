const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');
const css = fs.readFileSync('style.css', 'utf8');

// Regex to detect emoji and special signs
const emojiRegex = /[\u{1F300}-\u{1FAFF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{2600}-\u{27BF}\u{FE0F}\u{1F900}-\u{1F9FF}\u{1FA70}-\u{1FAFF}\u{2300}-\u{23FF}\u{2B50}\u{25AA}\u{25AB}\u{25B6}\u{25C0}\u{25FC}\u{25FB}\u{2700}-\u{27BF}]/gu;

console.log('=== EMOJI AND SYMBOL SCAN ===\n');

function scanFile(name, content) {
  const matches = [...content.matchAll(emojiRegex)].map(m => m[0]);
  const unique = [...new Set(matches)];
  console.log(`${name}: Found ${matches.length} emojis/signs (${unique.length} unique)`);
  console.log('Unique list:', unique.join(' '));
}

scanFile('index.html', html);
scanFile('app.js', js);
scanFile('style.css', css);
