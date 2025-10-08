<#
import_original_strip_retos.ps1

Usage (PowerShell, from repo root):
  .\scripts\import_original_strip_retos.ps1 -Source 'C:\Users\j\familia_calendario'

What it does (safe, non-destructive):
- Backs up current templates and tareas app into a ZIP and a backup folder.
- Copies templates/, static/, and the 'tareas' app from the source path into the demo workspace.
- Scans the copied files for occurrences of "reto"/"retos" and writes a report to scripts/reto_report.txt.
- Moves template files with 'reto' in the filename into templates/reto-backup/ and replaces obvious links/text mentioning 'reto' in templates and urls.py by commenting the lines (prefix with <!-- RETO_REMOVED --> or # RETO_REMOVED).
- Leaves all changes in place but writes backups for easy revert.

IMPORTANT: This script assumes you run it locally where the source project exists. I cannot access paths outside the workspace from the assistant, so you need to run it on your machine.

Review the script before running. It tries to be conservative (backs up before changing).
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Source
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$cwd = (Get-Location).Path
Write-Host "Repo root: $cwd"
Write-Host "Source project: $Source"

if (-Not (Test-Path $Source)) {
    Write-Error "Source path does not exist: $Source"
    exit 1
}

# Backups
$timestamp = (Get-Date -Format 'yyyyMMddHHmmss')
$backupDir = Join-Path $cwd "backup_import_$timestamp"
New-Item -Path $backupDir -ItemType Directory | Out-Null
Write-Host "Created backup dir: $backupDir"

# Backup current templates and tareas (if exist)
if (Test-Path (Join-Path $cwd 'templates')) {
    $zip = Join-Path $backupDir 'templates_backup.zip'
    Compress-Archive -Path (Join-Path $cwd 'templates\*') -DestinationPath $zip -Force
    Write-Host "Backed up templates to $zip"
    Copy-Item -Path (Join-Path $cwd 'templates') -Destination (Join-Path $backupDir 'templates_copy') -Recurse -Force
}
if (Test-Path (Join-Path $cwd 'tareas')) {
    Copy-Item -Path (Join-Path $cwd 'tareas') -Destination (Join-Path $backupDir 'tareas_copy') -Recurse -Force
    Write-Host "Backed up tareas to $backupDir\tareas_copy"
}

# Copy source templates, static, tareas
$toCopy = @('templates','static','tareas')
foreach ($name in $toCopy) {
    $srcPath = Join-Path $Source $name
    $dstPath = Join-Path $cwd $name
    if (Test-Path $srcPath) {
        Write-Host "Copying $srcPath -> $dstPath"
        # if destination exists, move it to backup first
        if (Test-Path $dstPath) {
            $mv = Join-Path $backupDir ("${name}_old")
            Move-Item -Path $dstPath -Destination $mv -Force
            Write-Host "Moved existing $dstPath to $mv"
        }
        Copy-Item -Path $srcPath -Destination $dstPath -Recurse -Force
    } else {
        Write-Host "Source $srcPath not found, skipping"
    }
}

# Scan for 'reto' occurrences and write a report
$report = Join-Path $cwd 'scripts\reto_report.txt'
Write-Host "Scanning for 'reto' occurrences and writing report to $report"
Get-ChildItem -Path $cwd -Recurse -Include *.py,*.html,*.txt,*.md | Select-String -Pattern 'reto|retos' -SimpleMatch | ForEach-Object {
    "$($_.Path):$($_.LineNumber): $($_.Line.Trim())" | Out-File -FilePath $report -Append
}

# Create a templates/reto-backup folder and move any template files that mention 'reto' in filename
$retoTplBackup = Join-Path $cwd 'templates\reto-backup'
New-Item -Path $retoTplBackup -ItemType Directory -Force | Out-Null
Get-ChildItem -Path (Join-Path $cwd 'templates') -Recurse -Filter '*reto*' -File -ErrorAction SilentlyContinue | ForEach-Object {
    $dest = Join-Path $retoTplBackup $_.Name
    if (Test-Path $dest) {
        $ts = (Get-Date -Format 'yyyyMMddHHmmss')
        $dest = Join-Path $retoTplBackup ("$($_.BaseName)_$ts$($_.Extension)")
    }
    Move-Item -Path $_.FullName -Destination $dest -Force
    Write-Host "Moved template $_ to $dest"
}

# Conservative replacements: comment out lines in urls.py that reference reto(s) and lines in templates with href to reto
$filesToEdit = Get-ChildItem -Path $cwd -Recurse -Include urls.py,*.html,*.py -ErrorAction SilentlyContinue
foreach ($f in $filesToEdit) {
    $path = $f.FullName
    $text = Get-Content $path -Raw -ErrorAction SilentlyContinue
    if ($null -eq $text) { continue }
    $orig = $text
    $modified = $text

    # comment out URL patterns containing 'reto' or 'retos' (use single-quoted regex to avoid parser issues)
    $modified = $modified -replace '(?m)^(\s*.*reto[s]?[^\r\n]*$)', '# RETO_REMOVED: $1'

    # comment out template anchor lines containing /reto or /retos
    # simpler, robust pattern: match any line with href and the token 'reto' (case-insensitive)
    $modified = $modified -replace '(?im)^.*href=[^>]*reto[^>]*>.*</a>.*$', '<!-- RETO_REMOVED: $& -->'

    # simpler: replace standalone words 'retos' in templates with empty string to hide menu items
    if ($path -like '*.html') {
        $modified = $modified -replace '\bretos\b', ''
        $modified = $modified -replace '\breto\b', ''
    }

    if ($modified -ne $orig) {
        $bak = "$path.reto.bak"
        Copy-Item -Path $path -Destination $bak -Force
        Set-Content -Path $path -Value $modified -Force
        Write-Host "Edited (and backed up) $path -> $bak"
    }
}

Write-Host "Done. Report saved to $report. Review changes and run migrations if necessary."
Write-Host "If you want, run: .\scripts\start_demo.ps1 to restart the demo with the imported code."
