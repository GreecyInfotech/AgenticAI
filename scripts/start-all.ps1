$Root = Split-Path -Parent $PSScriptRoot
Write-Host "Starting agents..."
& (Join-Path $PSScriptRoot "start-agents.ps1")
Start-Sleep -Seconds 10
Write-Host "Starting platform edge (gateway, BFFs, MCP)..."
& (Join-Path $PSScriptRoot "start-platform.ps1")
