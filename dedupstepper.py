#!/usr/bin/env python3

import os
from dedubmods import args, dataobj, db


def walk_files(argp, fod) -> bool:
    for root, dirs, files in os.walk(argp.path, topdown=False):
        for name in files:
            if argp.debug:
                print(f"Info: grab meta and calc hash \"{os.path.join(root, name)}\"")

            # Read meta data and calc hash into obj
            obj = dataobj.DataObj(os.path.join(root, name))

            if argp.debug:
                print(f"Info: registering \"{os.path.join(root, name)}\" with id \"{obj.id}\"")

            fod.store_file_obj(obj)

            if argp.debug:
                print(f"Info: stored \"{os.path.join(root, name)}\" with id \"{obj.id}\"")


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
