"""
This module contains functions for ranking movies based on their IMDB ratings.
"""
import os
import sys
import logging
from typing import Dict, List

import pandas as pd
from tabulate import tabulate

from src.movie_ranker.movie import to_movie, search_movie
from src.movie_ranker.omdb_handler import GetMovie


def get_movies_from_api(movie_api: GetMovie, file: str) -> List[Dict]:
    """Load a list of movies from an API and save them to the provided file."""
    with open(file, encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    movies = []
    for i in lines:
        movie = to_movie(i)
        if movie is None:
            continue

        data = search_movie(movie_api, movie)
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


def print_movies(df: pd.DataFrame) -> None:
    """Print the movies in the dataframe."""
    print(tabulate(
        df.values.tolist(),
        headers=df.columns.tolist(),
        tablefmt='psql'
    ))


def process_movies(
    file_path: str,
    output_path: str,
    parquet_path: str,
    update: bool,
    movie_api: GetMovie
) -> None:
    """
    Process movies from file and write to output.
    
    Args:
        file_path: Path to file containing movie information
        output_path: Path to save processed movies
        parquet_path: Path to parquet file for updates
        update: Whether to update existing parquet file
        movie_api: GetMovie instance for API access
    """
    if not file_path:
        logging.error('Error: No input file provided.')
        sys.exit(1)

    if not output_path:
        logging.error('Error: No output file provided.')
        sys.exit(1)

    if update:
        if not parquet_path:
            logging.error('Error: No parquet file provided.')
            sys.exit(1)

        if not os.path.exists(parquet_path):
            logging.error('Error: No parquet file found.')
            sys.exit(1)

        parquet_df = pd.read_parquet(parquet_path)
        with open(file_path, encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]

        movies = []
        for i in lines:
            movie = to_movie(i)
            if not movie:
                continue

            data = search_movie(movie_api, movie)
            if data is not None:
                movies.append(data)
            else:
                logging.warning('Warning: %s not found!', movie)

        updated_df = update_movies(parquet_df, movies)
        updated_df.to_parquet(output_path, compression='gzip')
        print_movies(updated_df)
    else:
        movie_data = get_movies_from_api(movie_api, file_path)
        df = pd.DataFrame(movie_data)
        df.to_parquet(output_path, compression='gzip')
        print_movies(df)