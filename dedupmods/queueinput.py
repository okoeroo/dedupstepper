#!/usr/bin/env python3

import os
from threading import Thread

ENDMARKER = "<THEEND>"


def walk_files(argp, q):
    for root, dirs, files in os.walk(argp.path, topdown=False):
        for name in files:
            # Concat to full path
            filepath = os.path.join(root, name)

            # Queue Put a full path
            if argp.debug:
                print(f"Queueing: {filepath}")

            q.put(filepath)

    q.put(ENDMARKER)


def bootup_walker_thread(argp, q):
    thread = Thread(target=walk_files, args=(argp, q,))
    thread.start()

    if argp.debug:
        print(f"Info: Thread started to walk files in {argp.path}")

    return thread
