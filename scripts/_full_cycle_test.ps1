# Full cycle test: start -> check -> stop -> verify
param(
    [int]$Port = 8000
)

Set-StrictMode -Version Latest
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
$repo = (Get-Location).Path
Write-Host "Repo: $repo"

$activate = Join-Path $repo '.venv\Scripts\Activate.ps1'
if (Test-Path $activate) {
    Write-Host "Activating venv: $activate"
    try { . $activate; Write-Host 'Activated .venv' } catch { Write-Host "Activation failed: $_" }
} else {
    Write-Host "Activate.ps1 not found at $activate -- will use direct python executable"
}

# Start server in background
Write-Host 'Starting demo (background)'
& "$repo\scripts\start_demo.ps1" -Port $Port -DoNotOpenBrowser
Start-Sleep -Seconds 2

# Run quick server checks
Write-Host 'Running server checks'
& "$repo\scripts\_check_server.ps1" -Port $Port

# Run smoke test with check_app.py
$py = Join-Path $repo '.venv\Scripts\python.exe'
if (-Not (Test-Path $py)) { $py = 'python' }
Write-Host "Running check_app.py with: $py"
try {
    & $py "$repo\scripts\check_app.py"
} catch {
    Write-Host "check_app.py failed: $_"
}

# Stop server
Write-Host 'Stopping demo'
& "$repo\scripts\stop_demo.ps1" -Port $Port -Force
Start-Sleep -Seconds 1

# Verify stopped
Write-Host 'Verifying stop'
if (Test-Path "$repo\.server_pid") { Write-Host '.server_pid still exists:'; Get-Content "$repo\.server_pid" } else { Write-Host '.server_pid removed' }
$net = Test-NetConnection -ComputerName 127.0.0.1 -Port $Port
Write-Host "Port $Port listening? $($net.TcpTestSucceeded)"

Write-Host 'Full cycle finished.'
