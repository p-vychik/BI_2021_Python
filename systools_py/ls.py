#!/usr/bin/env python3
import argparse
import sys
import os


parser = argparse.ArgumentParser()
parser.add_argument('--a', default=False, help='list hidden dirs', action='store_true')
parser.add_argument('dir', nargs='?', help='input directory, if empty, script current dir is used')
path = ''
args = parser.parse_args()
if args.dir is not None:
    if os.path.isdir(args.dir):
        path = args.dir
    else:
        print("Path doesn't exists")
        sys.exit(1)
else:
    path = os.getcwd()

for entry in os.listdir(path):
    if args.a:
        print(entry)
    else:
        if not entry.startswith('.'):
            print(entry)
