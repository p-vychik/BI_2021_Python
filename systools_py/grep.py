#!/usr/bin/env python3
import argparse
import fileinput
import re

parser = argparse.ArgumentParser()
parser.add_argument('reg_pattern', type=str, help='regex pattern in single quotes')
parser.add_argument('file', nargs='?', help='input file, if empty, stdin is used')
args = parser.parse_args()

output = []
for line in fileinput.input(files=args.file if args.file is not None else ('-', )):
    if re.search(args.reg_pattern, line):
        output.append(line)
print(*output, sep='\n')
