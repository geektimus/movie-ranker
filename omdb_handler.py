from dataclasses import dataclass

import requests


@dataclass
class GetMovie:
    """
    instantiate the class, passing api key.

    :param api_key: ombdapi key

    :Example:
    movie = GetMovie(api_key='your api key')
    """
    api_key: str
    values: dict = None

    def get_movie(self, title, year):
        """
        Get all data movie.
        :param title: movie title to search
        :param year: movie year to search
        :Example:
        movie.get_movie(title='Interstellar', plot='full'))
        """
        url = 'http://www.omdbapi.com/'
        payload = {'t': title, 'y': year,
                   'r': 'json', 'apikey': self.api_key}
        result = requests.get(url, params=payload).json()
        self.values = {k.lower(): v for k, v in result.items(
        )} if result['Response'] == 'True' else result['Error']
        return self.values

    def get_data(self, *args):
        """
        Get values passing keys as parameter.

        :Example:
        movie.get_data('Director', 'Actors')
        """
        items = {item.lower(): self.values.get(
            item.lower(), 'key not found!') for item in args}

        return items
