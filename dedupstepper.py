#!/usr/bin/env python3

import os
import sys
from threading import Thread
from queue import Queue
#import threading, queue
from multiprocessing import Process, Pool
from dedupmods import args, dataobj, db, queueinput, processfiles, dequeueproces



### MAIN
if __name__ == '__main__':
    # initialize arguments and verify arguments.
    # All data is verified to be safely useable
    argp_main = args.argparsing(os.path.basename(__file__))

    # Queue
    q = Queue(maxsize=1000)

    # Start the input gathering
    t = queueinput.bootup_walker_thread(argp_main, q)

    # Initialize the database
    fod_main = db.FileObjDB(argp_main.db, initdb=True)

    # Dequeue files to dispatch
    dequeueproces.dequeuefilesqueue(q, processfiles.proces_file, (fod_main, argp_main))

    # Search for collisions
    processfiles.search_for_hash_collission(argp_main, fod_main)

