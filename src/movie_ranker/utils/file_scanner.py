"""
This module contains functions for scanning local files.
"""
import os
from typing import List, Tuple


def scan_movie_files(input_dir: str) -> List[Tuple[int, str]]:
    """
    Scan a directory for movie files and return file sizes and names.
    
    Args:
        input_dir: Directory containing movie files
        
    Returns:
        List of tuples containing file size and name without extension
    """
    result = []
    for filename in os.listdir(input_dir):
        if not filename.endswith(".mp4"):
            continue

        # Get file size on disk
        file_size = os.path.getsize(os.path.join(input_dir, filename))
        file_name_without_extension = os.path.splitext(filename)[0]
        
        result.append((file_size, file_name_without_extension))
        
    return result


def write_movies_to_file(movies: List[Tuple[int, str]], output_file: str) -> None:
    """
    Write movie information to a file.
    
    Args:
        movies: List of tuples containing file size and name
        output_file: Path to output file
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding='utf-8') as f:
        for file_size, file_name in movies:
            f.write(f"{file_size} {file_name}\n")