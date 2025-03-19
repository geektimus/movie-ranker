"""
This script will get all the movies from a local folder and write them to 
the movies_local.txt file in the data folder
"""

import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Get movies from local folder and save to file')
    parser.add_argument('--input', '-i', 
                        required=True,
                        help='Input folder containing movie files')
    parser.add_argument('--output', '-o',
                        default=os.path.join("data", "movies.local.txt"),
                        help='Output file path (default: data/movies.local.txt)')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    for filename in os.listdir(args.input):
        if not filename.endswith(".mp4"):
            continue

        # Get file size on disk in KB
        file_size = os.path.getsize(os.path.join(args.input, filename))
        file_name_without_extension = os.path.splitext(filename)[0]

        # Write to specified output file
        with open(args.output, "a", encoding='utf-8') as f:
            f.write(f"{file_size} {file_name_without_extension}\n")

if __name__ == "__main__":
    main()
