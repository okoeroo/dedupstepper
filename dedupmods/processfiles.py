#!/usr/bin/env python3

import os
import sys
from threading import Thread
import threading, queue
from multiprocessing import Process, Pool
from dedupmods import args, dataobj, db, queueinput


def proces_file(filepath, fod, argp):
    # Check if already in the database, skip if found
    if fod.check_if_path_already_present(filepath):
        if argp.debug:
            print(f"Skipping: filepath already in database. \"{filepath}\"")
        return True

    # Avoid Symlinks
    if os.path.islink(filepath):
        if argp.debug:
            print(f"Warning: symlink detected. Skipping. \"{filepath}\"")
        return False

    if not os.path.isfile(filepath):
        if argp.debug:
            print(f"Warning: file is not a regular file. Skipping. \"{filepath}\"")
        return False


    # Read meta data into obj
    if argp.debug:
        print(f"Info: grab meta \"{filepath}\"")
    obj = dataobj.DataObj(filepath)

    # Read calc hash into obj
    if argp.debug:
        print(f"Info: calc hash \"{filepath}\"")
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


def pretty_print_collisions(fileobj_collisions):
#    print(fileobj_collisions)

    for collision_group_count, collision_group in enumerate(fileobj_collisions):
        print(f"--- Collision group {collision_group_count}")
        for fileobj in collision_group:
            print(f"  - File: {fileobj.filepath}")
            print(f"    Size: {fileobj.size}")
            print(f"    Hash: {fileobj.hash}")


def search_for_hash_collisions(argp, fod):
    fod.search_for_and_and_store_collisions()
    fileobj_collisions = fod.fetch_collision_data()

    # Print collisions
    if argp.print_collisions:
        pretty_print_collisions(fileobj_collisions)

    return fileobj_collisions

