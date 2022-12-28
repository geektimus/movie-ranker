import re
import os

import pandas as pd
import numpy as np

from tabulate import tabulate

from decouple import config
from omdb_handler import GetMovie

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

filename = config('local_filepath')
current_path = os.getcwd()
parquet_location = '%s/data/movies.parquet.gzip' % current_path

movie_api = GetMovie(api_key=config('omdbapi_key'))

base_rating = "5.5"


class Movie:
    movie_regex = r'(\d+)\s+(.*)\s+\((\d+)\)\s?(?:\[(.*p)\])?'

    def __init__(self, name, year, size, resolution=None, rating=None):
        self.name = name
        self.year = year
        self.resolution = resolution
        self.rating = rating
        self.size_in_bytes = size

    def __str__(self) -> str:
        return 'Movie(%s,%s,%s,%s)' % (self.name, self.year, self.resolution, self.rating)


def to_movie(line):
    p1 = re.compile(Movie.movie_regex)
    r = p1.match(line)
    if r:
        return Movie(r.group(2), r.group(3), r.group(1), r.group(4))
    else:
        print(f"Error: Could not parse: {line}")


def get_movie_rating(m: Movie):
    movie_api.get_movie(title=m.name, year=m.year)
    rating = movie_api.get_data('imdbrating')
    m.rating = rating.get('imdbrating', 0.0)
    return m


def search_movie(m: Movie):
    res = movie_api.get_movie(title=m.name, year=m.year)
    if res == 'Movie not found!':
        return None
    else:
        movie = movie_api.get_data('title', 'year', 'rated', 'released', 'runtime', 'genre', 'metascore', 'imdbrating',
                                   'boxoffice')
        movie["size_in_bytes"] = m.size_in_bytes
        movie["resolution"] = m.resolution
        return movie


def get_movies_from_api():
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]

    movies = []

    for i in lines:
        movie = to_movie(i)
        data = search_movie(movie)
        if data is not None:
            movies.append(data)
        else:
            print('Error: %s not found!' % movie)
    return movies


file_exists = os.path.exists(parquet_location) and os.path.isfile(parquet_location)

if file_exists:
    # Load parquet file into df, print df
    df = pd.read_parquet(parquet_location)
    print('Parquet file loaded from %s' % parquet_location)
else:
    # Search for the movies, save parquet file, print df
    movie_data = get_movies_from_api()
    df = pd.DataFrame(movie_data)
    df.to_parquet(parquet_location, compression='gzip')

unrated_movies = df.query('imdbrating == "N/A"')

rated_movies = df.query('imdbrating != "N/A"').copy()
ratings = rated_movies['imdbrating'].astype(float)
rated_movies.loc[:, 'imdbrating'] = ratings

filtered_by_rating = rated_movies.query(f'imdbrating < {base_rating}')
sorted_data = filtered_by_rating.sort_values(by=['imdbrating', 'boxoffice'], ascending=False)

sorted_data["size_in_bytes"] = pd.to_numeric(sorted_data["size_in_bytes"])
sorted_data["size_in_mb"] = (sorted_data["size_in_bytes"] / 1000000).apply(np.ceil)
sorted_data["size_in_gb"] = (sorted_data["size_in_bytes"] / 1000000000).round(2)
sorted_data.drop("size_in_bytes", axis=1, inplace=True)

print(f"Movies with Rating less than {base_rating}")
print(tabulate(sorted_data, headers='keys', tablefmt='psql'))

print("Unrated Movies")
print(tabulate(unrated_movies, headers='keys', tablefmt='psql'))
