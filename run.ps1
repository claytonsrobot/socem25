# Set the PYTHONPATH environment variable to src
$env:PYTHONPATH="src"

# Check for mode argument and call the corresponding script
if ($args[0] -eq "shell") {
    poetry run python -m socem25.shell.main
}
elseif ($args[0] -eq "gui") {
    poetry run python -m socem25.gui.main
}
elseif ($args[0] -eq "api") {
    poetry run python -m socem25.api.main
}
else {
    Write-Host "Usage: .\run.ps1 {shell|gui|api}"
    exit 1
}
