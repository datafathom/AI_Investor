<#
.SYNOPSIS
    AI Investor Deployment Script
.DESCRIPTION
    Automates the deployment process:
    1. Pulls latest code from Git
    2. Updates Python dependencies
    3. (Optional) Restarts services
.EXAMPLE
    .\deploy.ps1
#>

Write-Host "🚀 Starting Deployment for AI Investor..." -ForegroundColor Cyan

# 1. Pull Latest Code
Write-Host "📥 Pulling latest code..." -ForegroundColor Yellow
git pull
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git pull failed!" -ForegroundColor Red
    exit 1
}

# 2. Check/Create Venv
if (-not (Test-Path "venv")) {
    Write-Host "🛠️ Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# 3. Activate Venv and Install Deps
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

# 4. Run Tests (Sanity Check)
Write-Host "🧪 Running sanity tests..." -ForegroundColor Yellow
$env:PYTHONPATH = "c:\Users\astir\Desktop\AI_Company\AI_Investor"
pytest tests/web/test_dashboard_api.py # Run a fast test
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed! Aborting deployment." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deployment Complete! Services are ready." -ForegroundColor Green
