import os

def update_all_desktop_ini_files():
    # Get the project directory (one level above the script's location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Define the new base path for media icons
    media_icon_base_path = os.path.join(project_dir, "media", "media-ico")
    
    # Walk through the project directory to find all desktop.ini files
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.lower() == "desktop.ini":
                desktop_ini_path = os.path.join(root, file)
                print(f"Processing: {desktop_ini_path}")
                update_desktop_ini(desktop_ini_path, media_icon_base_path)

def update_desktop_ini(desktop_ini_path, media_icon_base_path):
    # Read the desktop.ini file
    with open(desktop_ini_path, 'r') as file:
        lines = file.readlines()
    
    # Update IconResource paths
    updated_lines = []
    for line in lines:
        if line.startswith("IconResource="):
            existing_filename = os.path.basename(line.split("=")[1].strip())
            new_absolute_path = os.path.join(media_icon_base_path, existing_filename)
            updated_lines.append(f"IconResource={new_absolute_path}\n")
        else:
            updated_lines.append(line)
    
    # Write the updated lines back to the desktop.ini file
    with open(desktop_ini_path, 'w') as file:
        file.writelines(updated_lines)

# Run the script
if __name__ == "__main__":
    update_all_desktop_ini_files()