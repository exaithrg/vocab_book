#!/bin/bash

SOURCE_DIR=~/.cache/kdcache/stat
TARGET_DIR=.

# mkdir -p "$TARGET_DIR"

current_hostname=$(hostname)
current_datetime=$(date +"%Y_%m_%d_%H_%M_%S")

for file in "$SOURCE_DIR"/*.json; do
  if [ -e "$file" ]; then
    base_name=$(basename "$file" .json)
    new_file_name="${base_name}_${current_hostname}_${current_datetime}.json"
    cp -i "$file" "$TARGET_DIR/$new_file_name"
  else
    echo "No .json exists"
  fi
done

echo "Copy kdcache json completed"