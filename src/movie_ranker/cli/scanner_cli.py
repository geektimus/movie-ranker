"""
Command line interface for the movie file scanner.
"""
import os
import argparse

from src.movie_ranker.utils.file_scanner import scan_movie_files, write_movies_to_file


def parse_args():
    """
    Parse command line arguments for the scanner.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Get movies from local folder and save to file')
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input folder containing movie files')
    parser.add_argument(
        '--output', '-o',
        default=os.path.join("data", "movies.local.txt"),
        help='Output file path (default: data/movies.local.txt)')
    return parser.parse_args()


def main():
    """Main function for the scanner CLI."""
    args = parse_args()
    
    # Scan movie files
    movies = scan_movie_files(args.input)
    
    # Write to file
    write_movies_to_file(movies, args.output)
    
    print(f"Scanned {len(movies)} movie files and wrote to {args.output}")


if __name__ == "__main__":
    main()