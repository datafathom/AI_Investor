# Frontend Verification Script (PowerShell)
# Verifies the frontend is properly set up and working

Write-Host "🔍 Frontend Verification Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Set-Location frontend2

# Check Node.js version
Write-Host "1. Checking Node.js version..." -ForegroundColor Yellow
$nodeVersion = node -v
Write-Host "   ✅ Node.js: $nodeVersion" -ForegroundColor Green
if ($nodeVersion -notmatch '^v(18|19|20|21|22)') {
    Write-Host "   ⚠️  Warning: Node.js 18+ recommended" -ForegroundColor Yellow
}

# Check if dependencies are installed
Write-Host ""
Write-Host "2. Checking dependencies..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "   ⚠️  node_modules not found. Installing..." -ForegroundColor Yellow
    npm install --legacy-peer-deps
} else {
    Write-Host "   ✅ node_modules exists" -ForegroundColor Green
}

# Check package.json scripts
Write-Host ""
Write-Host "3. Checking package.json scripts..." -ForegroundColor Yellow
$packageJson = Get-Content package.json | ConvertFrom-Json
if ($packageJson.scripts.dev) {
    Write-Host "   ✅ dev script found" -ForegroundColor Green
} else {
    Write-Host "   ❌ dev script not found" -ForegroundColor Red
    exit 1
}

# Check for main entry point
Write-Host ""
Write-Host "4. Checking entry points..." -ForegroundColor Yellow
$entryPoints = @("src/main.jsx", "src/main.js", "src/index.jsx", "src/index.js")
$found = $false
foreach ($entry in $entryPoints) {
    if (Test-Path $entry) {
        Write-Host "   ✅ Entry point found: $entry" -ForegroundColor Green
        $found = $true
        break
    }
}
if (-not $found) {
    Write-Host "   ❌ Entry point not found" -ForegroundColor Red
    exit 1
}

# Check for App component
Write-Host ""
Write-Host "5. Checking App component..." -ForegroundColor Yellow
if ((Test-Path "src/App.jsx") -or (Test-Path "src/App.js")) {
    Write-Host "   ✅ App component found" -ForegroundColor Green
} else {
    Write-Host "   ❌ App component not found" -ForegroundColor Red
    exit 1
}

# Check vite config
Write-Host ""
Write-Host "6. Checking Vite configuration..." -ForegroundColor Yellow
if (Test-Path "vite.config.js") {
    Write-Host "   ✅ vite.config.js found" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  vite.config.js not found" -ForegroundColor Yellow
}

# Try to build (quick syntax check)
Write-Host ""
Write-Host "7. Running build check..." -ForegroundColor Yellow
$buildOutput = npm run build 2>&1
if ($buildOutput -match "error") {
    Write-Host "   ❌ Build has errors" -ForegroundColor Red
    Write-Host $buildOutput
    exit 1
} else {
    Write-Host "   ✅ Build successful" -ForegroundColor Green
}

# Check if dist was created
if (Test-Path "dist") {
    Write-Host "   ✅ dist directory created" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  dist directory not found after build" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Frontend verification complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start dev server: npm run dev" -ForegroundColor White
Write-Host "2. Open http://localhost:3000" -ForegroundColor White
Write-Host "3. Check browser console for errors" -ForegroundColor White
Write-Host '4. Test navigation and key features' -ForegroundColor White

Set-Location ..
