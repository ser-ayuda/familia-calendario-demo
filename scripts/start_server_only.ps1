param(
    [int]$Port = 8000,
    [string]$HostName = '127.0.0.1',
    [switch]$Force
)

Set-StrictMode -Version Latest
Try {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Set-Location $scriptDir\..
    param(
        [int]$Port = 8000,
        [string]$HostName = '127.0.0.1',
        [switch]$Force
    )

    Set-StrictMode -Version Latest
    Try {
        $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
        Set-Location $scriptDir\..
        $pwd = (Get-Location).Path

        $venvActivate = Join-Path $pwd ".venv\Scripts\Activate.ps1"
        $venvPython = Join-Path $pwd ".venv\Scripts\python.exe"
        if (-Not (Test-Path $venvPython)) { Write-Error "Virtualenv python not found at $venvPython. Create .venv first or run start_demo.ps1."; Exit 1 }

        # If something is already listening on the port, optionally kill it
        $existing = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
        if ($existing) {
            $pids = $existing | Select-Object -ExpandProperty OwningProcess -Unique
            Write-Warning ("Found existing listener(s) on port {0}: {1}" -f $Port, ($pids -join ', '))
            if ($Force) {
                foreach ($id in $pids) {
                    try { Stop-Process -Id $id -Force -ErrorAction Stop; Write-Host ("Stopped PID {0}" -f $id) } catch { Write-Warning ("Failed to stop PID {0}: {1}" -f $id, $_) }
                }
                Start-Sleep -Seconds 1
            } else { Write-Host "Use -Force to kill existing listener(s) or choose another port."; Exit 1 }
        }

        $outLog = Join-Path $pwd 'server_stdout.log'
        $errLog = Join-Path $pwd 'server_err.log'

        Write-Host ("Starting development server on {0}:{1} (logs -> {2}, {3})" -f $HostName, $Port, $outLog, $errLog)

        # Build the command to run in a new PowerShell window: activate venv then call python manage.py runserver
        $activateCmd = "& '$venvActivate'"
        $runCmd = "& '$venvPython' '$pwd\manage.py' runserver '$HostName:$Port'"
        $fullCmd = "$activateCmd; $runCmd"

        $proc = Start-Process -FilePath pwsh -ArgumentList ('-NoExit','-Command',$fullCmd) -WorkingDirectory $pwd -PassThru
        if (-Not $proc) { Write-Error "Failed to start server process"; Exit 1 }

        # Wait briefly for the port to be listened on
        $tries = 0
        while ($tries -lt 80) {
            Start-Sleep -Milliseconds 500
            $conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
            if ($conn) { break }
            $tries++
        }

        Set-Content -Path "$pwd\.server_pid" -Value $proc.Id -Encoding ascii
        Write-Host ("Server launched in new PowerShell window (pid {0}). .server_pid written." -f $proc.Id)
        $url = "http://{0}:{1}" -f $HostName, $Port
        try { Start-Process $url } catch { }

    } Catch {
        Write-Error "Error while starting server-only: $_"
        Exit 1
    }
