"""
Command line interface for the movie ranker application.
"""
import os
import sys
import argparse
import warnings
import logging
from typing import Dict, Any

from dotenv import load_dotenv

from src.movie_ranker.omdb_handler import GetMovie
from src.movie_ranker.ranker import process_movies


def parse_args() -> Dict[str, Any]:
    """
    Parse command line arguments for movie ranker.
    
    Returns:
        Dictionary of parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            'Rank movies based on their IMDB ratings and the number of '
            'votes they have received.'
        )
    )
    parser.add_argument(
        '--file',
        help='The file to load the movies from'
    )
    parser.add_argument(
        '--output', 
        help='The file to save the movies to'
    )
    parser.add_argument(
        '--parquet',
        help='The parquet file location to use for updates',
        default='data/movies.parquet.gzip'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help=(
            'Update the movies from the file passed with --file. If used, '
            'the existing parquet file will be updated and overwritten.'
        )
    )
    
    return vars(parser.parse_args())


def main() -> None:
    """Main function for the movie ranker CLI."""
    # Suppress pandas FutureWarning
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('omdbapi_key', '')
    if not api_key:
        logging.error("Error: No OMDB API key found in environment variables")
        sys.exit(1)
    
    # Parse arguments
    args = parse_args()
    
    # Create movie API client
    movie_api = GetMovie(api_key=api_key)
    
    # Process movies
    process_movies(
        file_path=args['file'],
        output_path=args['output'],
        parquet_path=args['parquet'],
        update=args['update'],
        movie_api=movie_api
    )


if __name__ == '__main__':
    main()