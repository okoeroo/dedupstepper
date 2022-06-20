#!/usr/bin/env python3

import os
from queue import Queue
from dedupmods import args, db, queueinput, processfiles, dequeueproces


### MAIN
if __name__ == '__main__':
    # initialize arguments and verify arguments.
    # All data is verified to be safely useable
    argp_main = args.argparsing(os.path.basename(__file__))

    # Queue
    q = Queue(maxsize=argp_main.queuesize)

    # Initialize the database
    fod_main = db.FileObjDB(argp_main.db, initdb=False)

    # Start the input gathering
    t = queueinput.bootup_walker_thread(argp_main, q)

    # Dequeue files to dispatch
    dequeueproces.dequeuefilesqueue(q, processfiles.proces_file, (fod_main, argp_main))

    # Search for collisions
    processfiles.search_for_hash_collission(argp_main, fod_main)

