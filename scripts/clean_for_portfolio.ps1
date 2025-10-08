# Limpia el repo moviendo backups y logs grandes a removed_for_portfolio
$dst = Join-Path (Get-Location) 'removed_for_portfolio'
New-Item -ItemType Directory -Path $dst -Force | Out-Null
$patterns = @('backup_import_*','backup_for_portfolio*')
foreach ($p in $patterns) {
    $dirs = Get-ChildItem -Path . -Directory -Filter $p -ErrorAction SilentlyContinue
    foreach ($d in $dirs) {
        if (Test-Path $d.FullName) {
            Write-Host "Moving directory: $($d.FullName) -> $dst"
            Move-Item -Path $d.FullName -Destination $dst -Force
        }
    }
}
# Mover logs en la raíz y logs con patrones
$logPatterns = @('server*.log','*.log.bak')
foreach ($pat in $logPatterns) {
    $files = Get-ChildItem -Path . -File -Filter $pat -ErrorAction SilentlyContinue
    foreach ($f in $files) {
        Write-Host "Moving file: $($f.FullName) -> $dst"
        Move-Item -Path $f.FullName -Destination $dst -Force
    }
}
Write-Host 'Clean complete.'
