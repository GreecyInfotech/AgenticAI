$Root = Split-Path -Parent $PSScriptRoot
$Pids = Join-Path $Root ".tools\agent-pids.txt"

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

Get-CimInstance Win32_Process -Filter "Name='java.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'bfsi-agentic-ai-platform' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; Write-Host "Stopped java PID $($_.ProcessId)" }

Write-Host "All agent processes stopped."
