"""
This script is used to rank movies based on their IMDB ratings and the number 
of votes they have received.
It also allows users to search for movies and view their details.
"""

import os
import re
import sys
import warnings

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate

from omdb_handler import GetMovie

warnings.simplefilter(action='ignore', category=FutureWarning)

load_dotenv()

current_path = os.getcwd()
parquet_location = f'{current_path}/data/movies.parquet.gzip'

movie_api = GetMovie(api_key=os.getenv('omdbapi_key', ''))
BASE_MOVIE_RATING = "4.5"


class Movie:
    """
    Represents a movie and its metadata.
    """
    movie_regex = r'(\d+)\s+(.*)\s+\((\d+)\)\s?(?:\[(.*p)\])?'

    def __init__(self, name: str, year: str, size: str, resolution: str = "", rating: float = 0.0):
        self.name = name
        self.year = year
        self.resolution = resolution
        self.rating = rating
        self.size_in_bytes = size

    def __str__(self) -> str:
        return f'Movie(name={self.name}, year={self.year}, resolution={self.resolution}, rating={self.rating})'

    @staticmethod
    def empty() -> 'Movie':
        """Returns an instance of Movie with default values (i.e., all attributes are empty strings or 0.0)"""
        return Movie("", "", "")


def to_movie(line):
    """	Parses a line of text into a Movie object.

    Args:
        line (str): The line to parse.

    Returns:
        Movie: A movie object representing the given line.
    """

    p1 = re.compile(Movie.movie_regex)
    r = p1.match(line)
    if r:
        return Movie(r.group(2), r.group(3), r.group(1), r.group(4))

    print(f"Error: Could not parse: {line}")
    return None


def search_movie(m: Movie):
    """
    Searches for a movie with the given attributes.

    Args:
        m (Movie): The movie object to search for.

    Returns:
        bool: Whether the movie was found.
    """

    res = movie_api.get_movie(title=m.name, year=m.year)
    if res == 'Movie not found!':
        return None

    movie = movie_api.get_data('title', 'year', 'rated', 'released', 'runtime', 'genre', 'metascore', 'imdbrating',
                               'boxoffice')
    movie["size_in_bytes"] = m.size_in_bytes
    movie["resolution"] = m.resolution
    return movie


def get_movies_from_api(file: str) -> list:
    """Load a list of movies from an API and save them to the provided file.

    Args:
        file (str): The file to load/save the movies from/to.

    Returns:
        list: A list of Movie objects.
    """
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


if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    print(
        f"No argument provided. Please run the script with an argument. {len(sys.argv)}")
    sys.exit(1)

filename = sys.argv[1]

movies_file_exists = os.path.exists(filename) and os.path.isfile(filename)

if not movies_file_exists:
    print(f"No Valid Input File Provided: {filename}")

file_exists = os.path.exists(
    parquet_location) and os.path.isfile(parquet_location)

if file_exists:
    # Load parquet file into df, print df
    df = pd.read_parquet(parquet_location)
    print(f'Parquet file loaded from {parquet_location}')
else:
    # Search for the movies, save parquet file, print df
    movie_data = get_movies_from_api(filename)
    df = pd.DataFrame(movie_data)
    df.to_parquet(parquet_location, compression='gzip')

unrated_movies = df.query('imdbrating == "N/A"')

rated_movies = df.query('imdbrating != "N/A"').copy()
ratings = rated_movies['imdbrating'].astype(float)
rated_movies.loc[:, 'imdbrating'] = ratings

filtered_by_rating = rated_movies.query(f'imdbrating < {BASE_MOVIE_RATING}')
sorted_data = filtered_by_rating.sort_values(
    by=['imdbrating', 'boxoffice'], ascending=False)

sorted_data["size_in_bytes"] = pd.to_numeric(sorted_data["size_in_bytes"])
sorted_data["size_in_mb"] = (
    sorted_data["size_in_bytes"] / 1000000).apply(np.ceil)
sorted_data["size_in_gb"] = (
    sorted_data["size_in_bytes"] / 1000000000).round(2)
sorted_data.drop("size_in_bytes", axis=1, inplace=True)

print(f"Movies with Rating less than {BASE_MOVIE_RATING}")
print(tabulate(sorted_data, headers='keys', tablefmt='psql'))  # type: ignore

print("Unrated Movies")
print(tabulate(unrated_movies, headers='keys', tablefmt='psql'))  # type: ignore
