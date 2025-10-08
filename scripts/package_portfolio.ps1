param(
    [string]$OutDir = $(Resolve-Path -Path .).Path,
    [string]$Prefix = 'familia_calendario_public-portfolio'
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error 'git is required to run this script. Please install Git and ensure it is on PATH.'
    exit 1
}

$ts = Get-Date -Format 'yyyyMMddHHmm'
$zipName = "{0}-{1}.zip" -f $Prefix, $ts
$zipPath = Join-Path $OutDir $zipName

Write-Host "Creating portfolio ZIP -> $zipPath"

# Create temp folder and export HEAD with git archive
$tmp = Join-Path $env:TEMP ([System.IO.Path]::GetRandomFileName())
New-Item -ItemType Directory -Path $tmp | Out-Null
try {
    git archive --format=tar HEAD | tar -xf - -C $tmp
    # Remove backup folders if present
    Get-ChildItem -Path (Join-Path $tmp 'backup_import_*') -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $bf = Join-Path $tmp 'backup_for_portfolio'
    if (Test-Path $bf) { Remove-Item -Recurse -Force $bf }

    Compress-Archive -Path (Join-Path $tmp '*') -DestinationPath $zipPath -Force
    Write-Host "ZIP created at $zipPath"
}
finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}
