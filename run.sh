#!/bin/bash

# Set the PYTHONPATH to the src directory
export PYTHONPATH=src

# Check for mode argument and call the corresponding script
if [ "$1" == "shell" ]; then
    poetry run python -m socem25.shell.main
elif [ "$1" == "gui" ]; then
    poetry run python -m socem25.gui.main
elif [ "$1" == "api" ]; then
    poetry run python -m socem25.api.main
else
    echo "Usage: ./run.sh {shell|gui|api}"
    exit 1
fi
