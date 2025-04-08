#!/bin/bash

# Define the repository path and desktop.ini file
REPO_PATH="$1"
DESKTOP_INI_FILE="$REPO_PATH/desktop.ini"

# Check if desktop.ini exists
if [ -f "$DESKTOP_INI_FILE" ]; then
  # Iterate over lines in desktop.ini and update IconResource paths
  while IFS= read -r line; do
    if [[ $line == IconResource=* ]]; then
      # Extract the relative path
      RELATIVE_PATH="${line#*=}"
      # Generate the absolute path
      ABSOLUTE_PATH="$REPO_PATH/$RELATIVE_PATH"
      # Replace the line with the absolute path
      echo "IconResource=${ABSOLUTE_PATH}" >> "${DESKTOP_INI_FILE}.tmp"
    else
      echo "$line" >> "${DESKTOP_INI_FILE}.tmp"
    fi
  done < "$DESKTOP_INI_FILE"
  
  # Replace the original file with the updated one
  mv "${DESKTOP_INI_FILE}.tmp" "$DESKTOP_INI_FILE"
else
  echo "desktop.ini file not found at $DESKTOP_INI_FILE"
fi