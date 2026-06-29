$Root = Split-Path -Parent $PSScriptRoot
$Pids = Join-Path $Root ".tools\platform-pids.txt"

if (Test-Path $Pids) {
    Get-Content $Pids | ForEach-Object {
        $processId = [int]$_
        if (Get-Process -Id $processId -ErrorAction SilentlyContinue) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped PID $processId"
        }
    }
    Remove-Item $Pids -Force
}

Get-CimInstance Win32_Process -Filter "Name='node.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'mcp-servers' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Write-Host "Platform edge services stopped."
