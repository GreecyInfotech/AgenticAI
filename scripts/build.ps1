$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Jdk = Join-Path $Root ".tools\jdk-21"

if (-not (Test-Path "$Jdk\bin\java.exe")) {
    Write-Host "JDK 21 not found at $Jdk"
    Write-Host "Run: scripts\setup-jdk.ps1"
    exit 1
}

$env:JAVA_HOME = $Jdk
$env:PATH = "$Jdk\bin;$env:PATH"

Set-Location $Root
Write-Host "Building BFSI agents..."
mvn clean install -DskipTests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Build successful."
