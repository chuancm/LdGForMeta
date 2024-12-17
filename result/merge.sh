#!/bin/bash

# Check if a file name is provided as an argument
if [ -z "$1" ]; then
    echo "Please provide a file name for the merged file."
    exit 1
fi

# The name of the merged file is the first argument
merged_file="$1"
# Clear or create the merged file
> "$merged_file"
shift
# Loop through all .txt files in the current folder
for file in "$@"; do
    # Check if the file exists
    if [[ -f "$file" ]]; then
        cat "$file" >> "$merged_file"  # Append the content of the file to the merged file
#        echo "" >> "$merged_file"      # Optional: add a newline
    else 
	echo "warning: $file does not exit"
    fi

done

echo "All specified .txt files have been merged into $merged_file"
