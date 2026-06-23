# Stop locally running Smart Port services (Windows)
Write-Host "Stopping Smart Port services on known ports..." -ForegroundColor Yellow

$ports = @(9080, 8081, 8100, 5173, 5174, 5175, 5176)
foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    foreach ($conn in $conns) {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($proc -and $proc.ProcessName -match 'node|python') {
            Write-Host "Stopping $($proc.ProcessName) (PID $($proc.Id)) on port $port"
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        }
    }
}
Write-Host "Done." -ForegroundColor Green
