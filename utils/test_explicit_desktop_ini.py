import subprocess
import os

def run_powershell_script():
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the relative path to the PowerShell script
    powershell_script = os.path.join(script_dir, "test_explicit_desktop_ini.ps1")

    # Check if the PowerShell script exists
    if not os.path.isfile(powershell_script):
        print(f"Error: PowerShell script not found at {powershell_script}")
        return

    print(f"Running PowerShell script: {powershell_script}")

    try:
        # Run the PowerShell command
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", powershell_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the PowerShell script: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    run_powershell_script()