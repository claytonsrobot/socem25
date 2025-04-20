@echo off
:: Set the PYTHONPATH to src
set PYTHONPATH=src

:: Check for mode argument and call the corresponding script
if "%1" == "shell" (
    poetry run python -m socem25.shell.main
) else if "%1" == "gui" (
    poetry run python -m socem25.gui.main
) else if "%1" == "api" (
    poetry run python -m socem25.api.main
) else (
    echo Usage: run.bat {shell|gui|api}
    exit /b 1
)
