# scripts
Scripts for simple automation tasks.

#    1. finder.py (python 3.6.x)
    Description:
      This is a simple script for finding and logging keywords in multimple
      files inside a directory recursively (looks for files inside
      sub-directories as well).
      Takes 2 arguments:
        1. Path to directory to search.
        2. A text keyword file with line separated keywords (without spaces).
    Usage:
      ```sh
      $ python3 /path/to/search/ keyword_file.txt
      ```
