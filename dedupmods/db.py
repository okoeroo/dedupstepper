#!/usr/bin/env python3

import sqlite3
from dedupmods import dataobj


class FileObjDB:
    def __init__(self, db_path, initdb=True):
        self.db_path        = db_path
        self.initdb_on_init = initdb
        self.is_initiated   = False

        if self.initdb_on_init:
            self.initdb()


    def initdb(self):
        self.conn   = sqlite3.connect(self.db_path)
        # self.cur    = self.conn.cursor()
        self.create_tables()

        self.is_initiated = True


    def create_tables(self):
        # Get a cursor
        cur = self.conn.cursor()

        # Not adding fields 'exists' and 'statinfo'
        cur.execute('''CREATE TABLE IF NOT EXISTS fileobjs
                                    (   id TEXT PRIMARY KEY,
                                        filepath TEXT UNIQUE,
                                        ext TEXT,
                                        isdir TINYINT UNSIGNED,
                                        isfile TINYINT UNSIGNED,
                                        islink TINYINT UNSIGNED,
                                        ismount TINYINT UNSIGNED,
                                        size BIGINT UNSIGNED,
                                        hash TEXT
                                    )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS collisions
                                    (   hash TEXT PRIMARY KEY
                                    )''')


    def check_if_hash_already_present(self, hsh):
        if not self.is_initiated:
            self.initdb()

        # Get a cursor
        cur = self.conn.cursor()

        sql = '''SELECT hash
                   FROM collisions
                  WHERE hash = ?'''

        try:
            data = (hsh, )
            cur.execute(sql, data)

            rows = cur.fetchall()
            return len(rows) > 0

        except Exception as e:
            print(f"Error: check_if_hash_already_present(): {e}")
            return False


    def store_collision_by_hash(self, hsh: str) -> None:
        if not self.is_initiated:
            self.initdb()

        if self.check_if_hash_already_present(hsh):
            return

        # Get a cursor
        cur = self.conn.cursor()

        sql = '''INSERT INTO collisions(hash) VALUES (?)'''

        data = (hsh,)
        cur.execute(sql, data)
        self.conn.commit()


    def search_for_and_and_store_collisions(self):
        if not self.is_initiated:
            self.initdb()

        # Get a cursor
        cur = self.conn.cursor()

        # Select hash, group by hash and where a collision is more then 1
        # (like, twice or more)

        sql = '''SELECT hash
                   FROM fileobjs
               GROUP BY hash
                 HAVING COUNT(*)>1'''

        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            self.store_collision_by_hash(row[0])


    def fetch_collision_data(self):
        if not self.is_initiated:
            self.initdb()

        # Get a cursor
        cur = self.conn.cursor()

        fileobjs = []

        sql = '''SELECT hash
                   FROM collisions'''

        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            r_objs = self.query_fileobjs_by_hash(row[0])
            fileobjs += r_objs

        return fileobjs


    def query_fileobjs_by_hash(self, hsh: str):
        if not self.is_initiated:
            self.initdb()

        # Get a cursor
        cur = self.conn.cursor()

        fileobjs = []

        sql = '''SELECT
                        filepath,
                        id, ext,
                        isdir, isfile, islink, ismount,
                        size, hash
                   FROM fileobjs
                  WHERE hash = ?'''

        data = (hsh, )

        cur.execute(sql, data)

        rows = cur.fetchall()
        for row in rows:
            obj = dataobj.DataObj(filepath=row[0],
                                  id=row[1],
                                  isdir=row[2],
                                  isfile=row[3],
                                  islink=row[4],
                                  ismount=row[5],
                                  size=row[6],
                                  hash=row[7])
            fileobjs.append(obj)

        return fileobjs


    def check_if_path_already_present(self, obj):
        if not self.is_initiated:
            self.initdb()

        # Get a cursor
        cur = self.conn.cursor()

        if obj is None:
            raise Exception("Obj is None")

        sql = '''SELECT id
                   FROM fileobjs
                  WHERE filepath = ?'''

        try:
            data = (obj.filepath, )
            cur.execute(sql, data)

            rows = cur.fetchall()
            return len(rows) > 0

        except Exception as e:
            print(f"Error: check_if_path_already_present(): {e}")
            return False


    def store_file_obj(self, obj):
        if not self.is_initiated:
            self.initdb()

        # Check if file path already traversed and stored
        if self.check_if_path_already_present(obj):
            return


        # Get a cursor
        cur = self.conn.cursor()

        if obj is None:
            raise Exception("Obj is None")

        sql = '''INSERT INTO  fileobjs (
                                filepath,
                                id, ext,
                                isdir, isfile, islink, ismount,
                                size, hash)
                        VALUES (?,
                                ?, ?,
                                ?, ?, ?, ?,
                                ?, ?
                            )'''

        try:
            data = (obj.filepath,
                    obj.id,         obj.ext,
                    obj.isdir,      obj.isfile, obj.islink, obj.ismount,
                    obj.size,       obj.hash)

            cur.execute(sql, data)
            self.conn.commit()

        except Exception as e:
            print(f"Error: store_file_obj(): {e}")

