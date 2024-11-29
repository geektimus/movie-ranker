"""
This script will get all the movies from a local folder and write them to 
the movies_local.txt file in the data folder
"""

import os
import sys

for filename in os.listdir(sys.argv[1]):
    if not filename.endswith(".mp4"):
        continue

    # Get file size on disk in KB
    file_size = os.path.getsize(os.path.join(
        sys.argv[1], filename))
    file_name_without_extension = os.path.splitext(filename)[0]

    # Write to file in the data folder
    with open(os.path.join("data", "movies_local.txt"), "a", encoding='utf-8') as f:
        f.write(f"{file_size} {file_name_without_extension}\n")
