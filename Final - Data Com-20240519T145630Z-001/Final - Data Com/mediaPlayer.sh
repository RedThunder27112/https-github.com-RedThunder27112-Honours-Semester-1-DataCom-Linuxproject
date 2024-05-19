#!/bin/bash

# Check if mpv is installed
if ! command -v mpv &> /dev/null; then
    echo "Error: mpv is not installed. Please install mpv to use this script."
    exit 1
fi

# Check if the folder path is provided as argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

folder_path=$1

# Check if the provided folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: Folder '$folder_path' not found."
    exit 1
fi

# List all files in the folder
files=$(find "$folder_path" -type f -iname "*.mp3" -o -iname "*.wav" -o -iname "*.flac" -o -iname "*.ogg")

# Check if there are any music files in the folder
if [ -z "$files" ]; then
    echo "No music files found in the specified folder."
    exit 0
fi

# Iterate over each music file and play it
for file in $files; do
    echo "Playing: $file"
    mpv --no-video "$file"
done
