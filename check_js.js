const fs = require('fs');
const parser = require('@babel/parser');

const code = fs.readFileSync('frontend2/src/App.jsx', 'utf8');

try {
    parser.parse(code, {
        sourceType: 'module',
        plugins: ['jsx']
    });
    console.log('Parse successful!');
} catch (e) {
    console.error('Parse failed!');
    console.error(e.message);
    console.error(e.loc);

    const lines = code.split('\n');
    const start = Math.max(0, e.loc.line - 5);
    const end = Math.min(lines.length, e.loc.line + 5);
    for (let i = start; i < end; i++) {
        console.log(`${i + 1}: ${lines[i]}`);
        if (i + 1 === e.loc.line) {
            console.log(' '.repeat(e.loc.column) + '^');
        }
    }
}
