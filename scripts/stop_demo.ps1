<# stop_demo.ps1

Stops the demo server previously started by start_demo.ps1. It reads .server_pid and kills that process (if running).
#>
param(
    [int]$Port = 8000,
    [switch]$Force
)

try {
    $pwd = (Get-Location).Path
    $pidFile = Join-Path $pwd ".server_pid"
    if (Test-Path $pidFile) {
        $raw = Get-Content $pidFile -ErrorAction Stop | ForEach-Object { $_.Trim() } | Select-Object -First 1
        if ($raw) {
            # Extract digits from the file in case it contains accidental text like '[int]1234'
            $digits = ($raw -replace '\D','')
            if ($digits -and [int]::TryParse($digits,[ref]$null)) {
                $serverPid = [int]$digits
                Write-Host ("Stopping PID {0} ..." -f $serverPid)
                try { Stop-Process -Id $serverPid -Force -ErrorAction Stop; Write-Host ("Process {0} stopped." -f $serverPid) } catch { Write-Warning (("Could not stop process {0}: {1}" -f $serverPid, $_)) }
            } else {
                Write-Warning (".server_pid contains unexpected value: '{0}'. Skipping Stop-Process." -f $raw)
            }
        } else { Write-Host ".server_pid is empty" }
        # Remove PID file regardless (it may be stale)
        Remove-Item $pidFile -ErrorAction SilentlyContinue

        # Wait a short while for the port to close
        $waitTries = 0
        while ($waitTries -lt 10) {
            Start-Sleep -Milliseconds 300
            $listeners = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
            if (-Not $listeners) { break }
            $waitTries++
        }

        # If still listening and Force is specified, kill any processes owning the listener
        $listeners = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
        if ($listeners) {
            $pids = $listeners | Select-Object -ExpandProperty OwningProcess -Unique
            Write-Warning ("Port {0} still has listeners from PID(s): {1}" -f $Port, ($pids -join ', '))
            if ($Force) {
                foreach ($id in $pids) {
                    try {
                        Write-Host ("Forcing stop of PID {0}" -f $id)
                        Stop-Process -Id $id -Force -ErrorAction Stop
                        Write-Host ("Stopped PID {0}" -f $id)
                    } catch {
                        Write-Warning (("Failed to stop PID {0}: {1}" -f $id, $_))
                    }
                }
            } else {
                Write-Host "Use -Force to kill remaining listeners on the port."
            }
        }
        # Remove helper script if present
        $helperPath = Join-Path $pwd 'scripts\_runserver_helper.py'
        if (Test-Path $helperPath) { Remove-Item $helperPath -ErrorAction SilentlyContinue }
        Exit 0
    }

    # Fallback: look for any process listening on the port
    $listeners = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($listeners) {
    $pids = $listeners | Select-Object -ExpandProperty OwningProcess -Unique
    Write-Host ("Found processes listening on port {0}: {1}" -f $Port, ($pids -join ', '))
        if ($Force) {
            foreach ($id in $pids) {
                try { Stop-Process -Id $id -Force -ErrorAction Stop; Write-Host ("Stopped PID {0}" -f $id) } catch { Write-Warning ("Could not stop PID {0}: {1}" -f $id, $_) }
            }
            Exit 0
        } else {
            Write-Host "Use -Force to kill them or run start_demo with a different port."; Exit 1
        }
    }

    Write-Host "No .server_pid and no process listening on port $Port. Nothing to stop."
} catch {
    Write-Error ("Error while stopping demo: {0}" -f $_)
    Exit 1
}