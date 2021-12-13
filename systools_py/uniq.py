#!/usr/bin/env python3
import argparse
import fileinput
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help='input file, if empty, stdin is used')
args = parser.parse_args()
uniq = {}
for line in fileinput.input(files=args.file if args.file is not None else ('-', )):
    coded_line = hashlib.sha256(line.encode()).hexdigest()
    if coded_line in uniq:
        uniq[coded_line] = None
    else:
        uniq[coded_line] = line
for _, value in uniq.items():
    if value is not None:
        print(value, sep='')
