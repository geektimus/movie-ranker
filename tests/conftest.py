"""
Pytest configuration file with common fixtures
"""
import os
import pytest
from pathlib import Path
from movie_ranker.omdb_handler import GetMovie

@pytest.fixture
def test_data_dir():
    """Fixture to get the test data directory"""
    return Path(__file__).parent / "data"

@pytest.fixture
def mock_movie_api():
    """Fixture to create a mock movie API instance"""
    return GetMovie(api_key="test_key")

@pytest.fixture
def sample_movie_data():
    """Fixture to provide sample movie data for testing"""
    return {
        "title": "Test Movie",
        "year": "2024",
        "rated": "PG-13",
        "released": "2024-01-01",
        "runtime": "120 min",
        "genre": "Action, Drama",
        "metascore": "85",
        "imdbrating": "8.5",
        "boxoffice": "$100M"
    } 