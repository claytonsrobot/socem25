#!/bin/bash

# Get the project directory (one level above the script's location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Define the base path for media icons
MEDIA_ICON_BASE_PATH="$PROJECT_DIR/media/media-ico"

# Recursively find all desktop.ini files
find "$PROJECT_DIR" -name "desktop.ini" | while read -r DESKTOP_INI_PATH; do
    echo "Processing: $DESKTOP_INI_PATH"

    # Read and process desktop.ini
    UPDATED_LINES=""
    while IFS= read -r LINE; do
        if [[ $LINE == IconResource=* ]]; then
            EXISTING_FILENAME=$(basename "${LINE#IconResource=}")
            NEW_ABSOLUTE_PATH="$MEDIA_ICON_BASE_PATH/$EXISTING_FILENAME"
            UPDATED_LINES+="IconResource=$NEW_ABSOLUTE_PATH"$'\n'
        else
            UPDATED_LINES+="$LINE"$'\n'
        fi
    done < "$DESKTOP_INI_PATH"

    # Write updated lines back to desktop.ini
    echo "$UPDATED_LINES" > "$DESKTOP_INI_PATH"
done