import re
import os

import pandas as pd
from decouple import config
from tabulate import tabulate

from omdb_handler import GetMovie

filename = config('local_filepath') 
current_path = os.getcwd()

movie_api = GetMovie(api_key=config('omdbapi_key'))

class Movie:

    movie_regex = "(.*)\s+\((\d+)\)\s?(?:\[(.*)\])?"

    def __init__(self, name, year, resolution=None, rating=None):
        self.name = name
        self.year = year
        self.resolution = resolution
        self.rating = rating
    
    def __str__(self) -> str:
        return 'Movie(%s,%s,%s,%s)' % (self.name, self.year, self.resolution, self.rating)

def to_movie(line):
    r = re.match(Movie.movie_regex, line)
    return Movie(r.group(1), r.group(2), r.group(3))

def get_movie_rating(m: Movie):
    #print('Searching for %s' % m)
    res = movie_api.get_movie(title=m.name, year=m.year)
    rating = movie_api.get_data('imdbrating')
    m.rating = rating.get('imdbrating', 0.0)
    return m


def search_movie(m: Movie):
    #print('Searching for %s' % m)
    res = movie_api.get_movie(title=m.name, year=m.year)
    if res == 'Movie not found!':
        return None
    else:
        return movie_api.get_data('title','year','rated', 'released', 'runtime', 'genre', 'metascore', 'imdbrating', 'boxoffice')

with open(filename) as f:
    lines = [line.rstrip('\n') for line in f]

movie_data = []

for i in lines:
    movie = to_movie(i)
    data = search_movie(movie)
    if data != None:
        movie_data.append(data)
    else:
        print('Error: %s not found!' % movie)

df = pd.DataFrame(movie_data)

print(tabulate(df, headers='keys', tablefmt='psql'))

df.to_parquet('%s/data/movies.parquet.gzip' % current_path, compression='gzip')
