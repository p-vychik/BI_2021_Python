#!/usr/bin/env python3
import argparse
import fileinput
import re
import sys


def func_caller(line):
    output = []
    if args.l:
        output.append(count_lines())
    if args.w:
        output.append(count_words(line))
    if args.c:
        output.append(count_bytes(line))
    return output


def count_lines():
    return 1


def count_words(source):
    return len(re.findall(r'\b\w+\b', source))


def count_bytes(source):
    return sys.getsizeof(source)


parser = argparse.ArgumentParser()
parser.add_argument('--l', default=True, help='count new lines', action='store_true')
parser.add_argument('--w', default=True, help='count words', action='store_true')
parser.add_argument('--c', default=True, help='count bytes', action='store_true')
parser.add_argument('file', type=str, nargs='?', help='input file, if empty, stdin is used')

args = parser.parse_args()
output = []
for line in fileinput.input(files=args.file if args.file is not None else ('-', )):
    output.append(list(func_caller(line)))
print(*list(map(sum, zip(*output))))
