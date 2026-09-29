const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');

const btnRegex = /<button([^>]*)>([\s\S]*?)<\/button>/gi;
let match;
const buttons = [];
while ((match = btnRegex.exec(html)) !== null) {
  const attrs = match[1];
  const inner = match[2].replace(/<[^>]+>/g, '').trim().substring(0, 40);
  const idMatch = attrs.match(/id=["']([^"']+)["']/i);
  const classMatch = attrs.match(/class=["']([^"']+)["']/i);
  const onclickMatch = attrs.match(/onclick=["']([^"']+)["']/i);
  const id = idMatch ? idMatch[1] : '';
  const cls = classMatch ? classMatch[1] : '';
  const onclick = onclickMatch ? onclickMatch[1] : '';
  buttons.push({ id, cls, inner, onclick });
}

console.log('Total buttons found in index.html:', buttons.length);

const unhandled = [];
buttons.forEach(b => {
  let handled = false;
  if (b.onclick) handled = true;
  if (b.id && (js.includes(`'${b.id}'`) || js.includes(`"${b.id}"`) || js.includes(`\`${b.id}\``) || js.includes(b.id))) {
    handled = true;
  }
  if (!handled && b.cls) {
    b.cls.split(/\s+/).forEach(c => {
      if (c && js.includes(c)) handled = true;
    });
  }
  if (!handled) {
    unhandled.push(b);
  }
});

console.log('Unhandled or potentially unattached buttons count:', unhandled.length);
console.log('Unhandled list:', JSON.stringify(unhandled, null, 2));
