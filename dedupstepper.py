#!/usr/bin/env python3


import os
from multiprocessing import Process, Pool
from dedupmods import args, dataobj, db

#import pprint
#pp = pprint.PrettyPrinter(width=20)


def proces_file(filepath, fod, argp):
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


def walk_files(argp, fod, pool):
    processes = []

    for root, dirs, files in os.walk(argp.path, topdown=False):
        for name in files:
            # Concat to full path
            filepath = os.path.join(root, name)

            # Work with files, success is True, failure is False
            # Parallel or serial
            if argp.parallel:
                proc = Process(target=proces_file, args=(filepath,fod,argp,))
                processes.append(proc)
                proc.start()
            else:
                proces_file(filepath, fod, argp)

    return processes


def search_for_hash_collission(argp, fod):
    fod.search_for_and_and_store_collisions()
    fileobj_collisions = fod.fetch_collision_data()

    print(fileobj_collisions)
    return fileobj_collisions


### MAIN
if __name__ == '__main__':
    # initialize arguments and verify arguments.
    # All data is verified to be safely useable
    argp_main = args.argparsing(os.path.basename(__file__))

    # Start database
    if argp_main.parallel:
        fod_main = db.FileObjDB(argp_main.db, initdb=False)
    else:
        fod_main = db.FileObjDB(argp_main.db, initdb=True)

    with Pool(processes=4) as pool:
        # Walk files and register files
        processes = walk_files(argp_main, fod_main, pool)

    if argp_main.parallel:
        for p in processes:
            p.join()

    # Search for collisions
    search_for_hash_collission(argp_main, fod_main)

