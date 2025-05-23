#!/usr/bin/env python

import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="SOCEM25 Interface Launcher")
    parser.add_argument(
        "--mode", choices=["shell", "gui", "api"], help="Mode to launch", required=False
    )
    args = parser.parse_args()

    # 1. If user passed --mode flag
    if args.mode:
        mode = args.mode
    # 2. If env var is set (e.g., set SOCEM_MODE=shell)
    elif "SOCEM_MODE" in os.environ:
        mode = os.environ["SOCEM_MODE"]
    # 3. Prompt interactively
    else:
        print("Select interface mode:")
        print("1) Shell (TUI)")
        print("2) GUI")
        print("3) API (FastAPI)")
        choice = input("Choice [1-3]: ").strip()
        mode = {"1": "shell", "2": "gui", "3": "api"}.get(choice, "shell")

    # Dispatch
    if mode == "shell":
        from src.socem25.shell.main import main as shell_main
        shell_main()
    elif mode == "gui":
        from src.socem25.gui.main import main as gui_main
        gui_main()
    elif mode == "api":
        from src.socem25.api.main import main as api_main
        api_main()
    else:
        print(f"Unknown mode '{mode}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
