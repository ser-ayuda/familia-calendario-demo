<#
import_original_strip_retos_dryrun.ps1 - Dry-run preview

Uso (PowerShell):
  .\scripts\import_original_strip_retos_dryrun.ps1 -Source 'C:\Users\j\familia_calendario'

Qué hace (modo sólo simulación):
- Verifica que exista la ruta de origen.
- Lista los archivos bajo la ruta de origen que coinciden con 'templates', 'static', o 'tareas'.
- Escanea recursivamente esos archivos por ocurrencias de "reto"/"retos" (insensible a mayúsculas).
- Genera un informe en `scripts\reto_report_dryrun.txt` con las coincidencias encontradas y una lista de archivos que serían copiados.
- No crea backups, no copia ni modifica nada.

Esta herramienta te deja ver exactamente qué tocaría el import real.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Source
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$cwd = (Get-Location).Path
Write-Host "Repo root: $cwd"
Write-Host "Source project (dry-run): $Source"

if (-Not (Test-Path $Source)) {
    Write-Error "Source path does not exist: $Source"
    exit 1
}

$reportPath = Join-Path $cwd 'scripts\reto_report_dryrun.txt'
if (Test-Path $reportPath) { Remove-Item $reportPath -Force }

# Files and folders we would consider copying
$toCheck = @('templates','static','tareas')
$wouldCopy = @()
foreach ($name in $toCheck) {
    $src = Join-Path $Source $name
    if (Test-Path $src) {
        Write-Host "[DRYRUN] Found source folder: $src"
        $wouldCopy += $src
    } else {
        Write-Host "[DRYRUN] Source folder not found (skipping): $src"
    }
}

# Write header
"Dry-run import report - $(Get-Date)`nSource: $Source`n" | Out-File -FilePath $reportPath -Encoding utf8
"Folders that would be copied:" | Out-File -FilePath $reportPath -Append
$wouldCopy | Out-File -FilePath $reportPath -Append

# Scan for 'reto' occurrences in the found folders
foreach ($folder in $wouldCopy) {
    Write-Host "[DRYRUN] Scanning $folder for 'reto' occurrences..."
    Get-ChildItem -Path $folder -Recurse -Include *.py,*.html,*.txt,*.md -ErrorAction SilentlyContinue | Select-String -Pattern '(?i)\b(reto|retos)\b' | ForEach-Object {
        "$($_.Path):$($_.LineNumber): $($_.Line.Trim())" | Out-File -FilePath $reportPath -Append
    }
}

Write-Host "Dry-run complete. Report written to: $reportPath"
Write-Host "No files were modified. Review the report and then run scripts/import_original_strip_retos.ps1 to perform the import."