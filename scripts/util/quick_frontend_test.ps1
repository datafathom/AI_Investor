# Quick Frontend Test Script
# Simple script to verify frontend can start

Write-Host "🔍 Quick Frontend Test" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

Set-Location frontend2

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  Installing dependencies..." -ForegroundColor Yellow
    npm install --legacy-peer-deps
}

# Check package.json
if (-not (Test-Path "package.json")) {
    Write-Host "❌ package.json not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies ready" -ForegroundColor Green
Write-Host ""
Write-Host "Starting dev server..." -ForegroundColor Yellow
Write-Host "Open http://localhost:5173 (or configured port) in your browser" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start dev server
npm run dev
