# Smart Port AI Platform - Local Production Run (Windows)
# Usage: .\scripts\start-local.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

# Load environment
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

$env:JWT_SECRET = if ($env:JWT_SECRET) { $env:JWT_SECRET } else { "change-me-in-production" }
$env:JWT_ISSUER = if ($env:JWT_ISSUER) { $env:JWT_ISSUER } else { "smart-port-ai-platform" }
$env:API_GATEWAY_PORT = if ($env:API_GATEWAY_PORT) { $env:API_GATEWAY_PORT } else { "9080" }
$env:AGENT_GATEWAY_PORT = if ($env:AGENT_GATEWAY_PORT) { $env:AGENT_GATEWAY_PORT } else { "8081" }
$env:OTEL_EXPORTER_OTLP_ENDPOINT = if ($env:OTEL_EXPORTER_OTLP_ENDPOINT) { $env:OTEL_EXPORTER_OTLP_ENDPOINT } else { "http://localhost:4317" }

Write-Host "Starting Smart Port AI Platform..." -ForegroundColor Cyan
Write-Host "Root: $Root"

# Start API Gateway (port 9080 — 8080 may be in use by other apps)
Write-Host "[1/5] API Gateway on port $env:API_GATEWAY_PORT..."
Start-Process -FilePath "node" -ArgumentList "dist/main.js" -WorkingDirectory "$Root\api-gateway" -WindowStyle Hidden

Start-Sleep -Seconds 2

# Start Agent Gateway
Write-Host "[2/5] Agent Gateway on port $env:AGENT_GATEWAY_PORT..."
Start-Process -FilePath "node" -ArgumentList "dist/main.js" -WorkingDirectory "$Root\agent-gateway" -WindowStyle Hidden

Start-Sleep -Seconds 2

# Start Vessel Agent
Write-Host "[3/5] Vessel Agent on port 8100..."
$env:PYTHONPATH = "$Root\agents\vessel-agent\src"
$env:SERVICE_NAME = "vessel-agent"
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100" -WorkingDirectory "$Root\agents\vessel-agent\src" -WindowStyle Hidden

Start-Sleep -Seconds 2

# Start Port Operations UI
Write-Host "[4/5] Port Operations UI on port 5173..."
Start-Process -FilePath "npx" -ArgumentList "--yes", "pnpm@9.15.0", "--filter", "port-operations-ui", "dev" -WorkingDirectory $Root -WindowStyle Hidden

# Start Executive Dashboard
Write-Host "[5/5] Executive Dashboard on port 5174..."
Start-Process -FilePath "npx" -ArgumentList "--yes", "pnpm@9.15.0", "--filter", "executive-dashboard", "dev" -WorkingDirectory $Root -WindowStyle Hidden

Start-Sleep -Seconds 8

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Smart Port AI Platform is RUNNING" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host " API Gateway:        http://localhost:$env:API_GATEWAY_PORT/api/docs"
Write-Host " Agent Gateway:      http://localhost:$env:AGENT_GATEWAY_PORT/agents/docs"
Write-Host " Port Operations:    http://localhost:5173  (operator/operator)"
Write-Host " Executive Dashboard:http://localhost:5174  (executive/executive)"
Write-Host " Customs Dashboard:  http://localhost:5175  (customs/customs)"
Write-Host ""
Write-Host " NOTE: API Gateway uses port 9080 (8080 may be occupied)."
Write-Host "       Start Docker Desktop for full infra (Postgres, Kafka)."
Write-Host ""
Write-Host " Stop all:  powershell -File scripts/stop-local.ps1"
