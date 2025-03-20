"""
Tests for the OMDB handler module
"""
import pytest
from unittest.mock import patch, MagicMock
from movie_ranker.omdb_handler import GetMovie

def test_get_movie_success(mock_movie_api, sample_movie_data):
    """Test successful movie retrieval"""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Response": "True",
            **sample_movie_data
        }
        mock_get.return_value = mock_response

        result = mock_movie_api.get_movie("Test Movie", "2024")
        assert result == {k.lower(): v for k, v in sample_movie_data.items()}

def test_get_movie_not_found(mock_movie_api):
    """Test movie not found case"""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Response": "False",
            "Error": "Movie not found!"
        }
        mock_get.return_value = mock_response

        result = mock_movie_api.get_movie("Non Existent Movie", "2024")
        assert result == "Movie not found!"

def test_get_data(mock_movie_api, sample_movie_data):
    """Test getting specific movie data fields"""
    mock_movie_api.values = {k.lower(): v for k, v in sample_movie_data.items()}
    
    result = mock_movie_api.get_data('title', 'year', 'rating')
    assert result == {
        'title': 'Test Movie',
        'year': '2024',
        'rating': 'key not found!'
    } 