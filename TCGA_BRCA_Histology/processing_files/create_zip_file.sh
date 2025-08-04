#!/bin/bash

# Create a zip file name.
zip_file_name="missing_svs_images.zip"

# Check if the zip file already exists, and delete it if it does.
if [ -f "$zip_file_name" ]; then
  echo "Deleting existing zip file: $zip_file_name"
  rm "$zip_file_name"
fi

# Find directories with "-" in their names.
find . -type d -name "*-*" | while read -r directory; do
  echo "Processing directory: $directory"

  # Find .svs files within the current directory.
  svs_file=$(find "$directory" -type f -name "*.svs")

  if [ -n "$svs_file" ]; then
    echo "Found .svs file: $svs_file"
    # Add the .svs file to the zip archive.
    zip "$zip_file_name" "$svs_file"
    if [ $? -eq 0 ]; then
      echo "Successfully added $svs_file to $zip_file_name"
    else
      echo "Error adding $svs_file to $zip_file_name"
    fi
  else
    echo "No .svs file found in $directory"
  fi
done

echo "Finished processing.  The zip archive is: $zip_file_name"
