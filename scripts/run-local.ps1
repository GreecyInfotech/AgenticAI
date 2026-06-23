$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    .\.venv\Scripts\pip install -e .
}

$env:PYTHONPATH = $root

$services = @(
    @{ Dir = "api-gateway"; Port = 8000 },
    @{ Dir = "agent-gateway"; Port = 8001 },
    @{ Dir = "rag"; Port = 8002 }
)

Write-Host "Starting Enterprise Agentic AI Platform..."
foreach ($svc in $services) {
    Start-Process -NoNewWindow -FilePath ".\.venv\Scripts\uvicorn" -ArgumentList "main:app", "--host", "0.0.0.0", "--port", $svc.Port, "--app-dir", $svc.Dir
    Write-Host "  Started $($svc.Dir) on :$($svc.Port)"
}

Write-Host ""
Write-Host "API Gateway:    http://localhost:8000"
Write-Host "Agent Gateway:  http://localhost:8001"
Write-Host "RAG Service:    http://localhost:8002"
Write-Host ""
Write-Host "B2B Portal:  cd frontend/b2b-portal && npm install && npm run dev  -> http://localhost:3001"
Write-Host "B2C Portal:  cd frontend/b2c-portal && npm install && npm run dev  -> http://localhost:3002"
