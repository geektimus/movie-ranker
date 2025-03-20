# Movie Ranker

Repo created to check my movie collection and know which movies I can delete (rating &lt; 6.0)

## Movie File Scanner

This script scans a local folder for movie files (.mp4) and saves their information to a text file.

### Usage

The script supports the following command-line arguments:

- `--input` or `-i`: (Required) Input folder containing movie files
- `--output` or `-o`: (Optional) Output file path (default: data/movies.local.txt)

#### Examples

```bash
# Using default output location (data/movies.local.txt)
python -m movie_ranker.get_movies_from_local --input /path/to/movies

# Specifying custom output file
python -m movie_ranker.get_movies_from_local --input /path/to/movies --output /path/to/output.txt

# Using short form arguments
python -m movie_ranker.get_movies_from_local -i /path/to/movies -o /path/to/output.txt
```

### Output Format

The script generates a text file with each line containing:
- File size (in bytes)
- Movie name (without extension)

## Useful commands

### Generate the movie list with its size in kb

```bash
find ./ -mindepth 2 -type d -not -iname "*subs" -not -iname "*spanish*" -exec du -hk {} \; | grep -Evi "(subs|spanish)" | awk -F"/" '{print substr($1, 1, length($1)-1) $3}' > $HOME/Downloads/movies.txt
```

## Installation and Project Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-ranker.git
cd movie-ranker
```

2. Create and activate a virtual environment (recommended):
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On Unix or MacOS
python -m venv venv
source venv/bin/activate
```

3. Install the package in development mode with all dependencies:
```bash
pip install -e ".[dev]"
```

### Development Tools

The project includes several development tools configured in `pyproject.toml`:

- **Testing**: Run tests with coverage reporting
```bash
pytest
```

- **Code Formatting**: Format code using Black and isort
```bash
black .
isort .
```

- **Type Checking**: Run type checks with mypy
```bash
mypy .
```

- **Linting**: Check code style with flake8
```bash
flake8
```

### Project Structure

```
movie-ranker/
├── src/
│   └── movie_ranker/     # Main package directory
├── tests/               # Test files
├── data/               # Data files
├── pyproject.toml      # Project configuration and dependencies
└── README.md          # This file
```

### Environment Variables

The project uses `python-dotenv` for environment variable management. Create a `.env` file in the root directory with your configuration:

```env
# Add your environment variables here
```

### Dependencies

Main dependencies are managed through `pyproject.toml`. To update dependencies:

1. Edit `pyproject.toml`
2. Run `pip install -e ".[dev]"` to update your environment

### Building and Distribution

To build the package:
```bash
python -m build
```

This will create distribution files in the `dist/` directory.
