#!/usr/bin/env python3
import argparse
import fileinput


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help='input file, if empty, stdin is used')
parser.add_argument('--n', type=int, default=10, help='input file, if empty, stdin is used')
args = parser.parse_args()
lines = []
for line in fileinput.input(files=args.file if args.file is not None else ('-', )):
    lines.append(line)
if args.n >= len(lines):
    lower_bound = -1
else:
    lower_bound = len(lines)-1-args.n
for ind in range(len(lines)-1, lower_bound, -1):
    print(lines[ind], sep='')
