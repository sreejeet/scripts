# scripts
Scripts for simple automation tasks.

# 1. finder.py (python 3.6.x)
Description:
This is a simple script for searching and logging keywords in multiple
files inside a directory recursively (looks for files inside
sub-directories as well).
Currently it only supports utf-8 compatible files.

Usage:
```sh
$ python3 /path/to/search/ keyword_file.txt
```

# 2. selenium_1.py (python 3.7.0)
Description:
A selenium script to automate liking posts on your instagram feed.

Usage:
```CMD
> python3 .\engine.py [posts_to_like=20] [notify_like=5] [max_errors=5]
```
