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


# 2. instagramRealtionParser.py (python 3.6.x)
Description:
This script is used to derive how many people you
follow who don't follow you back and how many
followers  you don't follow. <b>It is very primitive.
You have to manually paste followers (followers_raw.txt)
and following (following_raw.txt)
lists in a file from the browser.</b>
Currently it only supports utf-8 compatible files.

Usage:
```sh
$ python3 .\instagramRelationParser.py username_for_log_file
```

# 3. selenium_1.py (python 3.7.0)
Description:
A selenium script to automate liking posts on your instagram feed.

Usage:
```CMD
> python3 .\engine.py [posts_to_like=20] [notify_like=5] [max_errors=5]
```
