const fs = require('fs');
const path = require('path');

const FRONTEND_DIR = path.join(__dirname, '../frontend2/src');
const WORKERS_DIR = path.join(FRONTEND_DIR, 'workers');
const SERVICES_DIR = path.join(FRONTEND_DIR, 'services');
const UTILS_DIR = path.join(FRONTEND_DIR, 'utils');
const WIDGETS_DIR = path.join(FRONTEND_DIR, 'widgets/OptionsChain');
const INDEX_HTML = path.join(__dirname, '../frontend2/index.html');

console.log('Verifying Phase 5 Implementation...\n');

const checks = [
    { name: 'Worker Directory', path: WORKERS_DIR, type: 'dir' },
    { name: 'Calculation Worker', path: path.join(WORKERS_DIR, 'calculationWorker.js'), type: 'file' },
    { name: 'Worker Manager', path: path.join(SERVICES_DIR, 'workerManager.js'), type: 'file' },
    { name: 'IndexedDB Provider', path: path.join(UTILS_DIR, 'indexedDBProvider.js'), type: 'file' },
    { name: 'Storage Service', path: path.join(UTILS_DIR, 'storageService.js'), type: 'file' },
];

let allPassed = true;

checks.forEach(check => {
    try {
        if (fs.existsSync(check.path)) {
            console.log(`[PASS] ${check.name} found.`);
        } else {
            console.error(`[FAIL] ${check.name} NOT found at ${check.path}`);
            allPassed = false;
        }
    } catch (e) {
        console.error(`[ERROR] checking ${check.name}:`, e.message);
        allPassed = false;
    }
});

// Check HTML for Font Optimization
try {
    const htmlContent = fs.readFileSync(INDEX_HTML, 'utf8');
    if (htmlContent.includes('href="https://fonts.googleapis.com"')) {
        console.log('[PASS] Font Preconnect found in index.html');
    } else {
        console.error('[FAIL] Font Preconnect NOT found in index.html');
        allPassed = false;
    }
} catch (e) {
    console.error('[ERROR] reading index.html:', e.message);
    allPassed = false;
}

// Check Virtualization Import
try {
    const widgetPath = path.join(WIDGETS_DIR, 'OptionsChainWidget.jsx');
    const widgetContent = fs.readFileSync(widgetPath, 'utf8');
    if (widgetContent.includes("from 'react-window'")) {
        console.log('[PASS] react-window usage found in OptionsChainWidget.jsx');
    } else {
        console.error('[FAIL] react-window usage NOT found in OptionsChainWidget.jsx');
        allPassed = false;
    }
} catch (e) {
    console.error('[ERROR] reading OptionsChainWidget.jsx:', e.message);
    allPassed = false;
}

if (allPassed) {
    console.log('\nSUCCESS: Phase 5 Verification Complete.');
    process.exit(0);
} else {
    console.error('\nFAILURE: Phase 5 Verification Failed.');
    process.exit(1);
}
