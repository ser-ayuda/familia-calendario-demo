<#
Quick start PowerShell script for running the demo locally on Windows (development only).

Usage: in a PowerShell prompt at repository root run:
  .\scripts\quick_start.ps1

#>

Set-StrictMode -Version Latest
Write-Host "Quick start: crear/activar venv, instalar dependencias, ejecutar migraciones y cargar fixtures"

$venvPath = Join-Path $PSScriptRoot '..' '.venv'
$python = Join-Path $venvPath 'Scripts\\python.exe'

if (-not (Test-Path $python)) {
    Write-Host "Creando virtualenv en $venvPath..."
    python -m venv $venvPath
}

Write-Host "Instalando dependencias..."
Start-Process -FilePath $python -ArgumentList '-m','pip','install','-r','requirements.txt' -NoNewWindow -Wait

Write-Host "Aplicando migraciones..."
Start-Process -FilePath $python -ArgumentList 'manage.py','migrate','--noinput' -NoNewWindow -Wait

Write-Host "Creando admin y usuarios demo (idempotente)..."
try {
    Start-Process -FilePath $python -ArgumentList 'manage.py','crear_demo' -NoNewWindow -Wait -ErrorAction Stop
} catch {
    try { Start-Process -FilePath $python -ArgumentList 'manage.py','create_demo_admin' -NoNewWindow -Wait } catch { Write-Host 'Comandos de creación de demo pueden variar; revisa scripts/' }
}

Write-Host "Cargando fixtures (si no existen datos ya)..."
Start-Process -FilePath $python -ArgumentList 'manage.py','loaddata','fixtures/contenttypes.json','fixtures/auth.json','fixtures/tareas.json' -NoNewWindow -Wait

Write-Host "Iniciando servidor de desarrollo en http://127.0.0.1:8000"
Start-Process -FilePath $python -ArgumentList 'manage.py','runserver' -NoNewWindow -Wait
