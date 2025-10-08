param(
    [int]$Port = 8000
)

Set-StrictMode -Version Latest
# Resolve the repo root relative to this script's location so the script works when run from any cwd
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Resolve-Path (Join-Path $scriptDir "..") | Select-Object -ExpandProperty Path
Write-Host "Activating venv and running server on 127.0.0.1:$Port (foreground) from repo root: $repoRoot"

$activatePath = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"
if (-Not (Test-Path $activatePath)) {
    Write-Error ".venv not found at $activatePath. Create or run .venv first."; exit 1
}

& $activatePath
Push-Location $repoRoot
try {
    python manage.py runserver 127.0.0.1:$Port
} finally {
    Pop-Location
}
