<# _stop_demo_fixed.ps1

Temporary fixed stop script. Use this to stop the running demo server and then replace stop_demo.ps1 with this file if everything works.
#>
param()

try {
    $pidFile = Join-Path (Get-Location).Path ".server_pid"
    if (-Not (Test-Path $pidFile)) {
        Write-Host ".server_pid not found. Nothing to stop."; exit 0
    }
    $pid = Get-Content $pidFile -ErrorAction Stop | ForEach-Object { $_.Trim() } | Select-Object -First 1
    if (-not $pid) { Write-Host ".server_pid empty"; exit 0 }
    Write-Host "Stopping PID $pid ..."
    try {
        Stop-Process -Id ([int]$pid) -Force -ErrorAction Stop
        Write-Host "Process $pid stopped."
    } catch {
        Write-Warning ("Could not stop process {0}: {1}" -f $pid, $_)
    }
    Remove-Item $pidFile -ErrorAction SilentlyContinue
} catch {
    Write-Error ("Error while stopping demo: {0}" -f $_)
    Exit 1
}