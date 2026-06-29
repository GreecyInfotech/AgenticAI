param(
    [switch]$SkipMcp
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Jdk = Join-Path $Root ".tools\jdk-21"
$Java = Join-Path $Jdk "bin\java.exe"
$Logs = Join-Path $Root "logs"
$Pids = Join-Path $Root ".tools\platform-pids.txt"

if (-not (Test-Path $Java)) {
    Write-Host "JDK 21 not found. Run scripts\setup-jdk.ps1 first."
    exit 1
}

New-Item -ItemType Directory -Force -Path $Logs | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Root ".tools") | Out-Null
@() | Set-Content $Pids

function Start-JavaService($name, $jarRel, $port) {
    $jarPath = Join-Path $Root $jarRel
    if (-not (Test-Path $jarPath)) {
        Write-Host "Missing JAR: $jarPath - run scripts\build.ps1 first"
        exit 1
    }
    $logFile = Join-Path $Logs "$name.log"
    Write-Host "Starting $name on port $port..."
    $args = "-jar `"$jarPath`" --server.port=$port"
    $proc = Start-Process -FilePath $Java -ArgumentList $args -WorkingDirectory $Root `
        -RedirectStandardOutput $logFile -PassThru -WindowStyle Hidden
    Add-Content $Pids $proc.Id
    Start-Sleep -Seconds 2
}

# MCP servers
if (-not $SkipMcp) {
    $mcpDir = Join-Path $Root "mcp-servers"
    if (Test-Path (Join-Path $mcpDir "package.json")) {
        if (-not (Test-Path (Join-Path $mcpDir "node_modules"))) {
            Write-Host "Installing MCP server dependencies..."
            Push-Location $mcpDir; npm install --silent; Pop-Location
        }
        Write-Host "Starting MCP servers..."
        $mcpProc = Start-Process -FilePath "node" -ArgumentList "src/start-all.js" `
            -WorkingDirectory $mcpDir -RedirectStandardOutput (Join-Path $Logs "mcp-servers.log") `
            -PassThru -WindowStyle Hidden
        Add-Content $Pids $mcpProc.Id
        Start-Sleep -Seconds 3
    }
}

# BFFs and gateway
Start-JavaService "customer-bff" "bff\customer-bff\target\customer-bff-0.1.0-SNAPSHOT.jar" 8101
Start-JavaService "employee-bff" "bff\employee-bff\target\employee-bff-0.1.0-SNAPSHOT.jar" 8102
Start-JavaService "admin-bff" "bff\admin-bff\target\admin-bff-0.1.0-SNAPSHOT.jar" 8103
Start-JavaService "api-gateway" "api-gateway\target\api-gateway-0.1.0-SNAPSHOT.jar" 8000
Start-JavaService "ai-gateway" "ai-gateway\model-router\target\model-router-0.1.0-SNAPSHOT.jar" 8300
Start-JavaService "rag-api" "rag\rag-api\target\rag-api-0.1.0-SNAPSHOT.jar" 8350
Start-JavaService "tools-api" "tools\tools-api\target\tools-api-0.1.0-SNAPSHOT.jar" 8450
Start-JavaService "search-api" "search\search-api\target\search-api-0.1.0-SNAPSHOT.jar" 8370
Start-JavaService "messaging-api" "messaging\messaging-api\target\messaging-api-0.1.0-SNAPSHOT.jar" 8550

Write-Host ""
Write-Host "Platform edge layer started."
Write-Host "API Gateway:   http://localhost:8000"
Write-Host "Customer BFF:  http://localhost:8000/api/customer/v1/chat"
Write-Host "Employee BFF:  http://localhost:8000/api/employee/v1/chat"
Write-Host "Admin BFF:     http://localhost:8000/api/admin/v1/agents"
Write-Host "MCP servers:   http://localhost:8501-8506"
Write-Host "AI Gateway:    http://localhost:8300/api/v1/chat/completions"
Write-Host "RAG Service:   http://localhost:8350/api/v1/retrieve"
Write-Host "Search API:    http://localhost:8370/api/v1/search"
Write-Host "Tools API:     http://localhost:8450/api/v1/tools"
Write-Host "Messaging API: http://localhost:8550/api/v1/topics"
Write-Host "Grafana:       http://localhost:3000 (docker compose up -d grafana)"
Write-Host "Frontend:      http://localhost:5173 (run scripts\start-frontend.ps1)"
Write-Host "Stop:          scripts\stop-platform.ps1"
