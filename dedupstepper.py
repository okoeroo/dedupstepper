#!/usr/bin/env python3
import asyncio
import aiosqlite
import sys
import os
import argparse
import hashlib

import aiofiles
import asyncio
import json

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

    parser.add_argument("--procnum",
                        dest='procnum',
                        help="Number of processes.",
                        default=None,
                        type=int)

    args = parser.parse_args()
    if not check_correctness(parser, args):
        sys.exit(1)

    return args


async def ahash(filepath):
    async with aiofiles.open(filepath, mode='rb') as f:
        b = await f.read()
        readable_hash = hashlib.sha256(b).hexdigest()
        return readable_hash


class FileObj:
    def __init__(self, filepath):
        if filepath is None or filepath == "":
            raise "Error"

        self.filepath = filepath
        self.obj = {}
        self.obj['filepath'] = self.filepath

        # self.update()
        # self.hash()


    async def ahash(self):
        h = await ahash(self.filepath)
        print(h)
        self.obj['hash'] = h


    def hash(self):
        if not os.path.isfile(self.filepath):
            return

        with open(self.filepath, "rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()

            self.obj['hash'] = readable_hash


    def chash(self):
        if not os.path.isfile(self.filepath):
            return

        h_s = hashlib.sha256()

        with open(self.filepath, 'rb') as f:
            # 16 * 1024 * 64 = 1M
            while chunk := f.read(16 * 1024 * h_s.block_size):
                h_s.update(chunk)

        self.obj['chash'] = h_s.hexdigest()


    def update(self):
        self.obj['statinfo'] = os.stat(self.filepath)

        self.obj['isfile']   = os.path.isfile(self.filepath)
        self.obj['isdir']    = os.path.isdir(self.filepath)
        self.obj['islink']   = os.path.islink(self.filepath)
        self.obj['ismount']  = os.path.ismount(self.filepath)


    def print(self):
        print(self.obj)


async def test_example(loop):
    conn = await aiosqlite.connect('sqlite.db', loop=loop)
    cur = await conn.cursor()
    await cur.execute("SELECT 42;")
    r = await cur.fetchall()
    print(r)
    await cur.close()
    await conn.close()




def doit(fo):
    fo.update()
    fo.hash()
    fo.chash()
    #fo.print()

    return fo


from multiprocessing import Pool


async def main(args):
    mem = []

    print("... ->", args.path)

    for root, dirs, files in os.walk(args.path, topdown=False):
        for name in files:
            fo = FileObj(os.path.join(root, name))
            mem.append(fo)

        for name in dirs:
            fo = FileObj(os.path.join(root, name))
            mem.append(fo)

    # Deploy action in pool
    with Pool(args.procnum) as p:
        res = p.map(doit, mem)

    for r in res:
        r.print()


### MAIN
if __name__ == '__main__':
    args = argparsing(os.path.basename(__file__))

    # asyncio.run(aread())

    asyncio.run(main(args))

#    loop = asyncio.new_event_loop()
#    asyncio.set_event_loop(loop)
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(test_example(loop))

