param(
    [switch]$DoMove,
    [switch]$DoZip
)

# This script identifies common backup/import artifacts and either lists them,
# or moves them to backup_for_portfolio/ (if -DoMove) and optionally zips that dir (if -DoZip).

$root = (Get-Location).Path
$targets = @(
    'backup_import_*',
    'backup_import_*/**',
    'templates/reto-backup',
    'templates/reto-backup/**'
)

$found = @()
foreach ($t in $targets) {
    $items = Get-ChildItem -Path $t -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
    if ($items) { $found += $items }
}

if (-Not $found) { Write-Host "No obvious backup artifacts found."; exit 0 }

Write-Host "Found the following artifact files (count: $($found.Count)):"
$found | ForEach-Object { Write-Host " - $_" }

if ($DoMove) {
    $dest = Join-Path $root 'backup_for_portfolio'
    if (-Not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest | Out-Null }
    Write-Host "Moving artifacts to $dest"
    foreach ($item in $found) {
        $full = (Resolve-Path $item -ErrorAction SilentlyContinue).ProviderPath
        if ($full.StartsWith($root)) {
            $rel = $full.Substring($root.Length)
            if ($rel.StartsWith('\') -or $rel.StartsWith('/')) { $rel = $rel.Substring(1) }
        } else {
            $rel = Split-Path $full -Leaf
        }
        $targetPath = Join-Path $dest $rel
        $targetDir = Split-Path $targetPath -Parent
        if (-Not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir | Out-Null }
    try { Move-Item -LiteralPath $item -Destination $targetPath -Force -ErrorAction Stop } catch { Write-Warning ("Failed to move {0}: {1}" -f $item, $_) }
    }
    Write-Host "Move complete."
    if ($DoZip) {
        $zipPath = Join-Path $root 'backup_for_portfolio.zip'
        if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
        Write-Host "Zipping $dest -> $zipPath"
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [IO.Compression.ZipFile]::CreateFromDirectory($dest, $zipPath)
        Write-Host "Zip created at $zipPath"
    }
}
