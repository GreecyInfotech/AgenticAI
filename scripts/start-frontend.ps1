$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Frontend = Join-Path $Root "frontend"

if (-not (Test-Path (Join-Path $Frontend "package.json"))) {
    Write-Host "Frontend not found at $Frontend"
    exit 1
}

Push-Location $Frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..."
    npm install
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created frontend/.env from .env.example"
}

Write-Host "Starting frontend dev server on http://localhost:5173"
npm run dev

Pop-Location
