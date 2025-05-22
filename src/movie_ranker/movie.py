"""
This module contains the Movie class and related functions.
"""
import logging
import re
from typing import Optional, Dict

from src.movie_ranker.omdb_handler import GetMovie


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
        return (f'Movie(name={self.name}, year={self.year}, '
                f'resolution={self.resolution}, rating={self.rating})')

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


def search_movie(movie_api: GetMovie, m: Movie) -> Optional[Dict]:
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