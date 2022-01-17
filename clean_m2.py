import datetime
import os
import pathlib

file_set = set()

for root, subdirs, files in os.walk(pathlib.Path.home() / '.m2' / 'repository'):
    if not subdirs:
        stat = os.stat(root)
        cdatetime = datetime.datetime.fromtimestamp(stat.st_ctime)
        if cdatetime.year <= 2020:
            file_set.add(root)
