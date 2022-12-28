# Movie Ranker

Repo created to check my movie collection and know which movies I can delete (rating &lt; 6.0)

## Useful commands

### Generate the movie list with its size in kb

```bash
find ./ -mindepth 2 -type d -not -iname "*subs" -not -iname "*spanish*" -exec du -hk {} \; | grep -Evi "(subs|spanish)" | awk -F"/" '{print substr($1, 1, length($1)-1) $3}' > $HOME/Downloads/movies.txt
```
