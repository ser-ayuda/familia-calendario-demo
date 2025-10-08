param(
    [int]$Port = 8000
)

Write-Host '--- .server_pid ---'
if (Test-Path '.server_pid') {
    $pidVal = Get-Content .server_pid
    Write-Host "PID: $pidVal"
} else {
    Write-Host '.server_pid not found'
    exit 2
}

Write-Host '--- Process info ---'
try {
    Get-Process -Id $pidVal | Select-Object Id,ProcessName,StartTime | Format-List
} catch {
    Write-Host "No process with PID $pidVal running"
}

Write-Host '--- Port test ---'
Test-NetConnection -ComputerName 127.0.0.1 -Port $Port | Select-Object RemoteAddress,RemotePort,TcpTestSucceeded | Format-List

Write-Host '--- tail server_err.log (last 200 lines) ---'
if (Test-Path 'server_err.log') { Get-Content server_err.log -Tail 200 } else { Write-Host 'server_err.log not found' }

Write-Host '--- tail server_stdout.log (last 200 lines) ---'
if (Test-Path 'server_stdout.log') { Get-Content server_stdout.log -Tail 200 } else { Write-Host 'server_stdout.log not found' }

Write-Host '--- End checks ---'
