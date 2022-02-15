#!/usr/bin/env python3
import argparse
import os
import sys
import shutil


def remove_dir(dir, recursively):
    if recursively:
        try:
            shutil.rmtree(dir)
        except OSError as e:
            print(f"error: {e.filename}, {e.strerror}")
            sys.exit(1)
    else:
        try:
            os.rmdir(dir)
        except OSError as e:
            print(f"error: {e.filename}, {e.strerror}")
            sys.exit(1)


def remove_file(file):
    try:
        os.unlink(file)
    except OSError as e:
        print(f"error: {e.filename}, {e.strerror}")
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('--r', default=False, help='remove recursively', action='store_true')
parser.add_argument('source', type=str, help='path to the file or directory to remove')
args = parser.parse_args()
if args.source is not None and os.path.exists(args.source):
    if args.r:
        if os.path.isdir(args.source):
            remove_dir(args.source, True)
        else:
            remove_file(args.source)
    else:
        if os.path.isdir(args.source):
            remove_dir(args.source, False)
        else:
            remove_file(args.source)
else:
    print("Provided path doesn't exists")
    sys.exit(1)
