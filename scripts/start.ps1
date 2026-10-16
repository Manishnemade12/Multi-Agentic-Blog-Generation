param(
    [switch]$Generate,
    [switch]$News,
    [string]$Date
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Starting BlogBoard frontend at http://localhost:8000"
Start-Process -FilePath "python" `
    -ArgumentList "-m", "http.server", "8000", "--directory", "blogboard\web" `
    -WorkingDirectory $root

if ($Generate -or $News) {
    $arguments = @("-m", "blogboard.run")
    if ($News) { $arguments += "--ainews" }
    if ($Date) { $arguments += @("--date", $Date) }
    Write-Host "Running BlogBoard generation pipeline..."
    & python @arguments
} else {
    Write-Host "Frontend is running. Add -Generate to publish an article."
    Write-Host "Press Ctrl+C to stop this command. Stop the server with its Python process in Task Manager."
    while ($true) { Start-Sleep -Seconds 3600 }
}
