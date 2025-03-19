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
python get_movies_from_local.py --input /path/to/movies

# Specifying custom output file
python get_movies_from_local.py --input /path/to/movies --output /path/to/output.txt

# Using short form arguments
python get_movies_from_local.py -i /path/to/movies -o /path/to/output.txt
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
