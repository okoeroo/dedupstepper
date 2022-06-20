#!/usr/bin/env python3

import sys
import os
import argparse


def check_correctness(parser, args):
    if args.path is None:
        print("Error: No path given")
        print("---")
        parser.print_help()
        return False

    elif not os.path.exists(args.path):
        print(f"Error: Path does not exist \"{args.path}\"")
        print("---")
        parser.print_help()
        return False

    return True

def argparsing(exec_file):
    parser = argparse.ArgumentParser(exec_file)

    parser.add_argument('--debug',
                    dest='debug',
                    default=False,
                    action="store_true",
                    help="Print debug output")

    parser.add_argument("--db",
                        dest='db',
                        help="Path to the database file.",
                        default='file_objects.db',
#                        default=':memory:',
                        type=str)

    parser.add_argument("--path",
                        dest='path',
                        help="Path to traverse.",
                        default=".",
                        type=str)

    parser.add_argument("--procnum",
                        dest='procnum',
                        help="Number of processes.",
                        default=None,
                        type=int)

    args = parser.parse_args()
    if not check_correctness(parser, args):
        sys.exit(1)

    return args

