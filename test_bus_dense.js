const fs = require('fs');

// Read app.js
let appJs = fs.readFileSync('app.js', 'utf8');

// Let's create Route 335 dense points
const r335_waypoints = [
    [28.6328, 77.2197], [28.6300, 77.2205], [28.6250, 77.2220], [28.6190, 77.2245],
    [28.6129, 77.2276], [28.6050, 77.2260], [28.5950, 77.2220], [28.5860, 77.2210],
    [28.5770, 77.2160], [28.5672, 77.2100], [28.5580, 77.2070], [28.5440, 77.2065],
    [28.5350, 77.2100], [28.5244, 77.2167],
    // Return loop
    [28.5255, 77.2175], [28.5360, 77.2110], [28.5450, 77.2075], [28.5590, 77.2080],
    [28.5680, 77.2110], [28.5780, 77.2170], [28.5870, 77.2215], [28.5960, 77.2225],
    [28.6060, 77.2265], [28.6135, 77.2280], [28.6200, 77.2250], [28.6260, 77.2225],
    [28.6310, 77.2210], [28.6328, 77.2197]
];

function interpolateSegment(p1, p2, stepM = 20.0) {
    const lat1 = p1[0], lng1 = p1[1];
    const lat2 = p2[0], lng2 = p2[1];
    const dx = (lng2 - lng1) * 111320 * Math.cos(Math.PI / 180 * (lat1 + lat2) / 2);
    const dy = (lat2 - lat1) * 110540;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const numSteps = Math.max(1, Math.floor(dist / stepM));
    const res = [];
    for (let s = 0; s < numSteps; s++) {
        const t = s / numSteps;
        res.push([+(lat1 + (lat2 - lat1) * t).toFixed(5), +(lng1 + (lng2 - lng1) * t).toFixed(5)]);
    }
    return res;
}

const p4 = [];
for (let i = 0; i < r335_waypoints.length - 1; i++) {
    p4.push(...interpolateSegment(r335_waypoints[i], r335_waypoints[i + 1], 20.0));
}
p4.push(r335_waypoints[r335_waypoints.length - 1]);

console.log('p4 points:', p4.length);
