#!/usr/bin/env python3
import argparse
import fileinput
import re

non_printable = re.compile(r'[\n\r\t]')
parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', help='input file, if empty, stdin is used')
args = parser.parse_args()
output = []
for line in fileinput.input(files=args.file if args.file is not None else ('-', )):
    output.append(non_printable.sub('', line))
output.sort()
print(*output, sep='\n')
