"""
This script is used to rank movies based on their IMDB ratings and the number
of votes they have received.
It also allows users to search for movies and view their details.
"""

import os
import re
import sys
import argparse
import warnings
import logging
from typing import Optional, Dict, List
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate

from movie_ranker.omdb_handler import GetMovie

warnings.simplefilter(action='ignore', category=FutureWarning)

load_dotenv()

# Get the package data directory
package_dir = Path(__file__).parent
data_dir = package_dir / "data"
parquet_location = data_dir / "movies.parquet.gzip"

movie_api = GetMovie(api_key=os.getenv('omdbapi_key', ''))

BASE_MOVIE_RATING = "4.5"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Movie:
    """
    Represents a movie and its metadata.

    This class stores information about movies including name, year, resolution,
    rating, and size in bytes.
    """
    movie_regex = r'(\d+)\s+(.*)\s+\((\d+)\)\s?(?:\[(.*p)\])?'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', "")
        self.year = kwargs.get('year', "")
        self.resolution = kwargs.get('resolution', "")
        self.rating = kwargs.get('rating', 0.0)
        self.size_in_bytes = kwargs.get('size', "")

    def __str__(self) -> str:
        return f'Movie(name={self.name}, year={self.year}, ' \
            f'resolution={self.resolution}, rating={self.rating})'

    @staticmethod
    def empty() -> 'Movie':
        """Returns an instance of Movie with default values"""
        return Movie()


def to_movie(line: str) -> Optional[Movie]:
    """Parses a line of text into a Movie object."""
    p1 = re.compile(Movie.movie_regex)
    r = p1.match(line)
    if r:
        # Create a dictionary with the parsed values
        movie_data = {
            'name': r.group(2),
            'year': r.group(3),
            'size': r.group(1),
            'resolution': r.group(4) or ""
        }
        return Movie(**movie_data)

    logging.error("Error: Could not parse: %s", line)
    return None


def search_movie(m: Movie) -> Optional[Dict]:
    """Searches for a movie with the given attributes."""
    res = movie_api.get_movie(title=m.name, year=m.year)
    if res == 'Movie not found!':
        return None

    movie = movie_api.get_data(
        'title',
        'year',
        'rated',
        'released',
        'runtime',
        'genre',
        'metascore',
        'imdbrating',
        'boxoffice'
    )
    movie["size_in_bytes"] = m.size_in_bytes
    movie["resolution"] = m.resolution if m.resolution else ""
    return movie


def get_movies_from_api(file: str) -> List[Dict]:
    """Load a list of movies from an API and save them to the provided file."""
    with open(file, encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    movies = []
    for i in lines:
        movie = to_movie(i)
        if movie is None:
            continue

        data = search_movie(movie)
        if data is not None:
            movies.append(data)
        else:
            print(f'Warning: {movie} not found!')
    return movies


def update_movies(
    parquet_df: pd.DataFrame,
    movies: List[Dict]
) -> pd.DataFrame:
    """Update the dataframe with the given list of movies."""
    for movie in movies:
        if movie['title'] in parquet_df['title'].values:
            parquet_df = parquet_df[parquet_df['title'] != movie['title']]
        parquet_df = pd.concat(
            [parquet_df, pd.DataFrame([movie])],
            ignore_index=True
        )
    return parquet_df


def print_movies(df: pd.DataFrame):
    """Print the movies in the dataframe."""
    print(tabulate(
        df.values.tolist(),
        headers=df.columns.tolist(),
        tablefmt='psql'
    ))


def main():
    """Main function for the script."""
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
        default=str(data_dir / "movies.parquet.gzip")
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help=(
            'Update the movies from the file passed with --file. If used, '
            'the existing parquet file will be updated and overwritten.'
        )
    )

    args = parser.parse_args()

    if not args.file:
        print('Error: No input file provided.')
        sys.exit(1)

    if not args.output:
        print('Error: No output file provided.')
        sys.exit(1)

    if args.update:
        if not args.parquet:
            print('Error: No parquet file provided.')
            sys.exit(1)

        if not os.path.exists(args.parquet):
            print('Error: No parquet file found.')
            sys.exit(1)

        parquet_df = pd.read_parquet(args.parquet)
        with open(args.file, encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]

        movies = []
        for i in lines:
            movie = to_movie(i)
            if not movie:
                continue

            data = search_movie(movie)
            if data is not None:
                movies.append(data)
            else:
                print(f'Warning: {movie} not found!')

        updated_df = update_movies(parquet_df, movies)
        updated_df.to_parquet(args.output, compression='gzip')
        print_movies(updated_df)
    else:
        movie_data = get_movies_from_api(args.file)
        df = pd.DataFrame(movie_data)
        df.to_parquet(args.output, compression='gzip')
        print_movies(df)


if __name__ == '__main__':
    main()
