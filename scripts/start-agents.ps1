param(
    [switch]$OrchestratorOnly
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Jdk = Join-Path $Root ".tools\jdk-21"
$Logs = Join-Path $Root "logs"
$Pids = Join-Path $Root ".tools\agent-pids.txt"
$Java = Join-Path $Jdk "bin\java.exe"

if (-not (Test-Path $Java)) {
    Write-Host "JDK 21 not found. Run scripts\setup-jdk.ps1 first."
    exit 1
}

New-Item -ItemType Directory -Force -Path $Logs | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Root ".tools") | Out-Null

$services = @(
    @{ Jar = "agents\intent-agent\target\intent-agent-0.1.0-SNAPSHOT.jar";         Port = 8401; Name = "intent-agent" },
    @{ Jar = "agents\customer-agent\target\customer-agent-0.1.0-SNAPSHOT.jar";     Port = 8402; Name = "customer-agent" },
    @{ Jar = "agents\kyc-agent\target\kyc-agent-0.1.0-SNAPSHOT.jar";               Port = 8403; Name = "kyc-agent" },
    @{ Jar = "agents\aml-agent\target\aml-agent-0.1.0-SNAPSHOT.jar";               Port = 8404; Name = "aml-agent" },
    @{ Jar = "agents\fraud-agent\target\fraud-agent-0.1.0-SNAPSHOT.jar";             Port = 8405; Name = "fraud-agent" },
    @{ Jar = "agents\loan-agent\target\loan-agent-0.1.0-SNAPSHOT.jar";             Port = 8406; Name = "loan-agent" },
    @{ Jar = "agents\underwriting-agent\target\underwriting-agent-0.1.0-SNAPSHOT.jar"; Port = 8407; Name = "underwriting-agent" },
    @{ Jar = "agents\claim-agent\target\claim-agent-0.1.0-SNAPSHOT.jar";           Port = 8408; Name = "claim-agent" },
    @{ Jar = "agents\compliance-agent\target\compliance-agent-0.1.0-SNAPSHOT.jar"; Port = 8409; Name = "compliance-agent" },
    @{ Jar = "agents\audit-agent\target\audit-agent-0.1.0-SNAPSHOT.jar";           Port = 8410; Name = "audit-agent" },
    @{ Jar = "agents\recommendation-agent\target\recommendation-agent-0.1.0-SNAPSHOT.jar"; Port = 8411; Name = "recommendation-agent" },
    @{ Jar = "agents\portfolio-agent\target\portfolio-agent-0.1.0-SNAPSHOT.jar";   Port = 8412; Name = "portfolio-agent" },
    @{ Jar = "agents\escalation-agent\target\escalation-agent-0.1.0-SNAPSHOT.jar"; Port = 8413; Name = "escalation-agent" },
    @{ Jar = "agents\notification-agent\target\notification-agent-0.1.0-SNAPSHOT.jar"; Port = 8414; Name = "notification-agent" },
    @{ Jar = "agent-platform\agent-registry\target\agent-registry-0.1.0-SNAPSHOT.jar"; Port = 8201; Name = "agent-registry" },
    @{ Jar = "agent-platform\orchestrator\target\orchestrator-0.1.0-SNAPSHOT.jar"; Port = 8200; Name = "orchestrator" }
)

if ($OrchestratorOnly) {
    $services = $services | Where-Object { $_.Port -in @(8401, 8406, 8407, 8410, 8411, 8414, 8200) }
}

@() | Set-Content $Pids

foreach ($svc in $services) {
    $jarPath = Join-Path $Root $svc.Jar
    if (-not (Test-Path $jarPath)) {
        Write-Host "Missing JAR: $jarPath - run scripts\build.ps1 first"
        exit 1
    }
    $logFile = Join-Path $Logs "$($svc.Name).log"
    Write-Host "Starting $($svc.Name) on port $($svc.Port)..."
    $args = "-jar `"$jarPath`" --server.port=$($svc.Port)"
    $proc = Start-Process -FilePath $Java -ArgumentList $args -WorkingDirectory $Root `
        -RedirectStandardOutput $logFile `
        -PassThru -WindowStyle Hidden
    Add-Content $Pids $proc.Id
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "Started $($services.Count) services. Logs: $Logs"
Write-Host "Orchestrator:  http://localhost:8200/api/v1/orchestrate"
Write-Host "Registry:      http://localhost:8201/api/v1/registry/agents"
Write-Host "Stop all:      scripts\stop-agents.ps1"
