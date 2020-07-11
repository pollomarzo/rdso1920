#!usr/bin/env python3
import os
import sys
import re
from collections import defaultdict

# "^([\w\d\-]+\.[c|h])|([M|m]akefile)$"
C_PATTERN = re.compile(r"^\w+\.c$")
H_PATTERN = re.compile(r"^\w+\.h$")
M_PATTERN = re.compile(r"[M|m]akefile")

startdir = sys.argv[1]
c_files = []
h_files = []
makefiles = []

for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
        fullpath = os.path.join(dirpath, filename)
        if C_PATTERN.match(filename):
            c_files.append(fullpath)
        elif H_PATTERN.match(filename):
            h_files.append(fullpath)
        elif M_PATTERN.match(filename):
            makefiles.append(fullpath)


total_lines = defaultdict(int)
for file in c_files:
    lines = len(open(file).readlines())
    print(f"{file} {lines}")
    total_lines['c'] += lines

print(f"tot .c {total_lines['c']}")

for file in h_files:
    lines = len(open(file).readlines())
    print(f"{file} {lines}")
    total_lines['h'] += lines

print(f"tot .h {total_lines['h']}")

for file in makefiles:
    lines = len(open(file).readlines())
    print(f"{file} {lines}")
    total_lines['makefiles'] += lines

print(f"tot Makefiles {total_lines['makefiles']}")

print(f"tot source {sum(total_lines.values())}")
