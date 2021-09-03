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


class FileObj:
    def __init__(self, filepath):
        if filepath is None or filepath == "":
            raise "Error"

        self.filepath = filepath
        self.obj = {}

        self.update()
        self.hash()


    def hash(self):
        if not os.path.isfile(self.filepath):
            return

        with open(self.filepath, "rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest();

            self.obj['hash'] = readable_hash
            return readable_hash


    def update(self):
        self.obj['filepath'] = self.filepath
        self.obj['statinfo'] = os.stat(self.filepath)

        self.obj['isfile']   = os.path.isfile(self.filepath)
        self.obj['isdir']    = os.path.isdir(self.filepath)
        self.obj['islink']   = os.path.islink(self.filepath)
        self.obj['ismount']  = os.path.ismount(self.filepath)


    def print(self):
        print(self.obj)


### MAIN
if __name__ == "__main__":
    args = argparsing(os.path.basename(__file__))

    mem = []

    print(args.path)
    for root, dirs, files in os.walk(args.path, topdown=False):
        for name in files:
            fo = FileObj(os.path.join(root, name))
            mem.append(fo)

        for name in dirs:
            fo = FileObj(os.path.join(root, name))
            mem.append(fo)

    for m in mem:
        m.print()
