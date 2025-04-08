import os

def update_paths(repo_path, desktop_ini_path):
    # Get absolute path of the repository
    absolute_repo_path = os.path.abspath(repo_path)
    
    # Read desktop.ini file
    with open(desktop_ini_path, 'r') as file:
        lines = file.readlines()
    
    # Update IconResource paths
    updated_lines = []
    for line in lines:
        if line.startswith("IconResource="):
            relative_path = line.split("=")[1].strip()
            absolute_path = os.path.join(absolute_repo_path, relative_path)
            updated_lines.append(f"IconResource={absolute_path}\n")
        else:
            updated_lines.append(line)
    
    # Write updated paths back to desktop.ini
    with open(desktop_ini_path, 'w') as file:
        file.writelines(updated_lines)

# Example usage
update_paths("path/to/cloned/repo", "path/to/cloned/repo/desktop.ini")