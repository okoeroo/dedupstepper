#!/usr/bin/env python3

import os
from dedupmods import args, dataobj, db


def proces_file(filepath) -> 'success':
    # Avoid Symlinks
    if os.path.islink(filepath):
        print(f"Warning: symlink detected. Skipping. \"{filepath}\"")
        return False

    if not os.path.isfile(filepath):
        print(f"Warning: file is not a regular file. Skipping. \"{filepath}\"")
        return False

    if argp.debug:
        print(f"Info: grab meta and calc hash \"{filepath}\"")

    # Read meta data and calc hash into obj
    obj = dataobj.DataObj(filepath)
    obj.hash = dataobj.calc_hash_file(filepath)

    if obj.hash is None:
        print(f"Warning: could not calculate hash \"{filepath}\"")
        return False

    if argp.debug:
        print(f"Info: registering \"{filepath}\" with id \"{obj.id}\"")

    # Store into database
    fod.store_file_obj(obj)

    if argp.debug:
        print(f"Info: stored \"{filepath}\" with id \"{obj.id}\"")

    # All ok
    return True


def walk_files(argp, fod) -> bool:
    for root, dirs, files in os.walk(argp.path, topdown=False):
        for name in files:
            # Concat to full path
            filepath = os.path.join(root, name)

            # Work with files, success is True, failure is False
            if not proces_file(filepath):
                continue


def search_for_hash_collission(argp, fod) -> bool:
    fod.search_for_and_and_store_collisions()
    fod.fetch_collision_data()



### MAIN
if __name__ == '__main__':
    # initialize arguments and verify arguments.
    # All data is verified to be safely useable
    argp = args.argparsing(os.path.basename(__file__))

    # Start database
    fod = db.FileObjDB(argp.db)

    # Walk files and register files
    rc = walk_files(argp, fod)

    search_for_hash_collission(argp, fod)
