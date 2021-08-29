#!/usr/bin/env python3
import sys
import os
import argparse
import hashlib

def check_correctness(parser, args):
    if args.path is None:
        print("= Error: No path given")
        print("---")
        parser.print_help()
        return False

    elif not os.path.exists(args.path):
        print(f"= Error: Path does not exist \"{args.path}\"")
        print("---")
        parser.print_help()
        return False

    return True

def argparsing(exec_file):
    parser = argparse.ArgumentParser(exec_file)
    parser.add_argument("--path",
                        dest='path',
                        help="Path to traverse.",
                        default=None,
                        type=str)

    args = parser.parse_args()
    if not check_correctness(parser, args):
        sys.exit(1)

    return args


def file_hash(filepath):
    with open(filepath, "rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        print(readable_hash)
        return readable_hash

def file_handling(filepath):
    statinfo = os.stat(filepath)

    obj = {}

    obj['filepath'] = filepath
    obj['statinfo'] = statinfo

    obj['isfile']   = os.path.isfile(filepath)
    obj['isdir']    = os.path.isdir(filepath)
    obj['islink']   = os.path.islink(filepath)
    obj['ismount']  = os.path.ismount(filepath)

    if os.path.isfile(filepath):
        obj['hash'] = file_hash(filepath)

    print(obj)
    return obj


### MAIN
if __name__ == "__main__":
    args = argparsing(os.path.basename(__file__))

    mem = []

    print(args.path)
    for root, dirs, files in os.walk(args.path, topdown=False):
        for name in files:
            obj = file_handling(os.path.join(root, name))

        for name in dirs:
            obj = file_handling(os.path.join(root, name))


