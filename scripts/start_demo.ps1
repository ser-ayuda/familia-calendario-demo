<#
start_demo.ps1

PowerShell helper to prepare the demo environment and start the Django dev server.

Usage:
  .\scripts\start_demo.ps1 [-Port 8000]

This script will:
  - ensure a virtualenv exists at ./.venv (create if missing)
  - install requirements from requirements.txt (if present)
  - run makemigrations/migrate
  - run scripts/create_demo.py to populate demo data
  - open a new PowerShell window and run the development server on 127.0.0.1:<Port>

#>
param(
    [int]$Port = 8000,
    [switch]$Force
)

Set-StrictMode -Version Latest
Try {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Set-Location $scriptDir\..

    $pwd = (Get-Location).Path
    Write-Host "Working directory: $pwd"

    # Ensure venv exists
    if (-Not (Test-Path "$pwd\.venv\Scripts\python.exe")) {
        Write-Host "Creating virtualenv .venv..."
        python -m venv .venv
    }

    $venvPython = Join-Path $pwd ".venv\Scripts\python.exe"
    if (-Not (Test-Path $venvPython)) {
        Write-Error "Could not find venv python at $venvPython"
        Exit 1
    }

    Write-Host "Using venv python: $venvPython"

    # Upgrade pip and install requirements if present
    Write-Host "Ensuring pip and dependencies..."
    try { & $venvPython -m pip install --upgrade pip } catch { Write-Warning ("pip upgrade failed: {0}" -f $_) }
    if (Test-Path "$pwd\requirements.txt") {
    try { & $venvPython -m pip install -r "$pwd\requirements.txt" } catch { Write-Warning ("pip install -r requirements.txt failed: {0}" -f $_) }
    }

    # Run migrations (non-interactive)
    Write-Host "Applying migrations..."
    & $venvPython "$pwd\manage.py" migrate --noinput

    # Create demo data if helper exists
    Write-Host "Creating demo data (if available)..."
    if (Test-Path "$pwd\scripts\create_demo.py") {
    try { & $venvPython "$pwd\scripts\create_demo.py" } catch { Write-Warning ("create_demo.py failed: {0}" -f $_) }
    } else {
        Write-Host "No scripts/create_demo.py found; skipping demo data creation"
    }

    # Check for existing listener on the port
    $existing = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($existing) {
    $pids = $existing | Select-Object -ExpandProperty OwningProcess -Unique
    Write-Warning ("Found existing listener(s) on port {0} from PID(s): {1}" -f $Port, ($pids -join ', '))
        if ($Force) {
            Write-Host ("Force flag set: stopping existing process(es) {0}" -f ($pids -join ', '))
            foreach ($id in $pids) {
                try { Stop-Process -Id $id -Force -ErrorAction Stop; Write-Host ("Stopped PID {0}" -f $id) } catch { Write-Warning ("Failed to stop PID {0}: {1}" -f $id, $_) }
            }
            Start-Sleep -Seconds 1
        } else {
            Write-Host "Use -Force to kill the existing process(es) or choose another port. Aborting."
            Exit 1
        }
    }

    # Prepare log files
    $outLog = Join-Path $pwd 'server_stdout.log'
    $errLog = Join-Path $pwd 'server_err.log'
    Write-Host "Logs: $outLog, $errLog"

    # Start server using 'python -m django runserver' to avoid manage.py arg parsing issues
    Write-Host "Starting development server on 127.0.0.1:$Port"
    # Create a small helper script under scripts/ to reliably run the Django server with the desired port
    $helperPath = Join-Path $pwd 'scripts\_runserver_helper.py'
    $helperContent = @"
import os
import sys
from django.core.management import execute_from_command_line

repo_root = r"{0}"
os.chdir(repo_root)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
# Ensure settings module for this helper
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hogar.settings')

execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:{1}'])
"@ -f $pwd, $Port

    try {
        Set-Content -Path $helperPath -Value $helperContent -Encoding utf8
    } catch {
        Write-Warning ("Could not write helper script {0}: {1}" -f $helperPath, $_)
    }

    $argList = @($helperPath)
    $proc = Start-Process -FilePath $venvPython -ArgumentList $argList -WorkingDirectory $pwd -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru

    if (-Not $proc) {
        Write-Error "Failed to start server process"
        Exit 1
    }

    # Wait for the server to open the port
    $tries = 0
    while ($tries -lt 60) {
        Start-Sleep -Milliseconds 500
        $conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
        if ($conn) { break }
        $tries++
    }

    # Persist PID of the python process
    try {
        Set-Content -Path "$pwd\.server_pid" -Value $proc.Id -Encoding ascii
        Write-Host "Server started (pid $($proc.Id)). .server_pid written."
    } catch {
        Write-Warning ("Could not write .server_pid: {0}" -f $_)
    }

    try {
        Start-Process "http://127.0.0.1:$Port"
    } catch {
        Write-Host ("Could not open browser automatically: {0}" -f $_)
    }

    Write-Host "Done. If the demo admin was created, credentials are demo_admin / demo1234."
} Catch {
    Write-Error ("Error during start_demo: {0}" -f $_)
    Exit 1
}
