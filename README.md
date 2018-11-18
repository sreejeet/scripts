# scripts
Scripts for simple automation tasks.

# 1. finder.py (python 3.6.x)
Description:
This is a simple script for searching and logging keywords in multimple
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
follow who dont follow you back and how many
followers  you dont follow. <b>It is very primitive.
You have to manually paste followers (followers_raw.txt)
and following (following_raw.txt)
lists in a file from the browser.</b>
Currently it only supports utf-8 compatible files.

Usage:
```sh
$ python3 .\instagramRelationParser.py username_for_log_file
```
