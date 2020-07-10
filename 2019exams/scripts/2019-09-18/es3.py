#!/usr/bin/env python3
import os
import sys
from collections import defaultdict

inodes = defaultdict(list)

for dirpath, _, filenames in os.walk(sys.argv[1]):
    for filename in filenames:
        fullpath = str(os.path.join(dirpath, filename))
        stats = os.stat(fullpath)
        inodes[stats.st_ino].append(fullpath)

for ino_no, filenames in inodes.items():
    if len(filenames) > 1:
        print(f"{' '.join(filenames)}")
