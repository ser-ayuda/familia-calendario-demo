# Auto-start and test for demo server
Set-StrictMode -Version Latest
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
$repo = (Get-Location).Path
Write-Host "Repo root: $repo"

$activate = Join-Path $repo '.venv\Scripts\Activate.ps1'
if (Test-Path $activate) {
    Write-Host "Activating venv via: $activate"
    try { . $activate; Write-Host 'Activated .venv' } catch { Write-Host "Activation failed: $_" }
} else {
    Write-Host "Activate.ps1 not found at $activate"
}

Write-Host 'Python and pip:'
try { python -V } catch { Write-Host 'python not found in PATH' }
try { pip -V } catch { Write-Host 'pip not found in PATH' }
try { where.exe python } catch { }

Write-Host 'Starting start_demo.ps1 (will create/use .venv and start server)'
& "$repo\scripts\start_demo.ps1" -Port 8000

Start-Sleep -Seconds 2

Write-Host 'Running _check_server.ps1'
& "$repo\scripts\_check_server.ps1" -Port 8000

# select python executable to run check_app.py
$py = $null
if (Test-Path (Join-Path $repo '.venv\Scripts\python.exe')) { $py = (Join-Path $repo '.venv\Scripts\python.exe') }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $py = 'python' }
else { Write-Host 'No python executable found to run check_app.py'; exit 2 }

Write-Host "Running check_app.py with: $py"
& $py "$repo\scripts\check_app.py"

Write-Host 'Auto-start+test finished.'
