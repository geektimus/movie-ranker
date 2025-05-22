# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Movie Ranker is a Python-based tool to analyze a movie collection and identify which movies can potentially be deleted based on their IMDB ratings (typically those with ratings < 6.0). The project consists of:

1. A script to scan local movie files and generate a list with their sizes
2. A tool to fetch movie metadata from the OMDB API
3. A movie ranking system that processes and displays movie information

## Environment Setup

The project uses Python 3.13+ and manages dependencies with uv. The main dependencies include:

- pandas and pyspark for data processing
- omdbapi for fetching movie data
- python-dotenv for environment variable management
- tabulate for formatted console output

## Key Commands

### Setting Up Environment Variables

The project requires an OMDB API key to fetch movie data. Create a `.env` file in the project root with:

```text
omdbapi_key=your_api_key_here
```

### Scanning Movie Files

To scan a local folder for movie files and generate a list:

```bash
python get_movies_from_local.py --input /path/to/movies --output /path/to/output.txt
```

Arguments:

- `--input` or `-i`: (Required) Input folder containing movie files
- `--output` or `-o`: (Optional) Output file path (default: data/movies.local.txt)

### Ranking Movies

To rank movies based on their IMDB ratings:

```bash
python movie_ranker.py --file /path/to/movie/list.txt --output /path/to/output.parquet
```

Arguments:

- `--file`: The file containing movie information (required)
- `--output`: The file to save processed movies to (required)
- `--parquet`: The parquet file location to use for updates (default: data/movies.parquet.gzip)
- `--update`: Flag to update existing parquet file with new movie data

## Code Structure

### Core Components

1. **get_movies_from_local.py**: Scans local folders for movie files (.mp4) and saves their names and sizes to a text file.

2. **omdb_handler.py**: Contains the `GetMovie` class that interfaces with the OMDB API to retrieve movie metadata.

3. **movie_ranker.py**: Main script that:
   - Parses movie information from text files
   - Fetches additional metadata from OMDB API
   - Processes and ranks movies based on their ratings
   - Saves data in parquet format and displays formatted results

### Data Processing

The project uses both pandas and PySpark for data processing:

- pandas.ipynb: Jupyter notebook for data analysis with pandas
- pyspark.ipynb: Jupyter notebook for data analysis with PySpark

Movie data is stored in parquet format with gzip compression for efficient storage and retrieval.