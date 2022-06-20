#!/usr/bin/env python3

from queue import Queue
from dedupmods import args, dataobj, db, queueinput, processfiles, dequeueproces
from multiprocessing import Process, Pool



def dequeuefilesqueue(q: Queue, func: callable, arg_tup: tuple):
    endmarker_found = False

    fod, argp = arg_tup

    with Pool(processes=11) as pool:
        while True:
            if argp.debug:
                print(f"Queue size: {q.qsize()}")

            item = q.get()

            if argp.debug:
                print(f'Working on {item}')

            if item == queueinput.ENDMARKER:
                endmarker_found = True
            else:
                result = pool.apply_async(func, (item, fod, argp))
                result.get()

            if argp.debug:
                print(f'Finished {item}')

            q.task_done()

            if q.empty() and endmarker_found:
                break

    if argp.debug:
        print("Joining Queue")

    q.join()
