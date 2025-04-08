import subprocess
import os
import sys

# Ensure the root directory is part of sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.helpers.toml_utils import import_toml

# Path to the configuration file
CONFIG_FILE = os.path.join(script_dir, "update_desktop_ini_config.toml")

def run_powershell_script():
    # Load the configuration file
    config = import_toml(CONFIG_FILE)

    # Retrieve verbosity setting from the TOML file
    verbose = config["config"].get("verbose", False)

    # Define the path to the PowerShell script
    powershell_script = os.path.join(script_dir, "update_desktop_ini.ps1")

    # Verify the PowerShell script exists
    if not os.path.isfile(powershell_script):
        print(f"Error: PowerShell script not found at {powershell_script}")
        return

    #print(f"Running PowerShell script: {powershell_script}")

    try:
        # Pass verbosity configuration to the PowerShell script
        verbosity_flag = "-Verbose" if verbose else "-Silent"
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", powershell_script, verbosity_flag], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the PowerShell script: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    run_powershell_script()