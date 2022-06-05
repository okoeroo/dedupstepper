#!/usr/bin/env python3

import aiosqlite
import sqlite3


class FileObjDB:
    def __init__(self, db_file):
        self.conn   = sqlite3.connect(db_file)
        self.cur    = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        # Not adding fields 'exists' and 'statinfo'
        self.cur.execute('''CREATE TABLE IF NOT EXISTS fileobjs
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

        self.cur.execute('''CREATE TABLE IF NOT EXISTS collisions
                                    (   hash TEXT PRIMARY KEY
                                    )''')

    def store_collision_by_hash(self, hsh: str) -> None:
        sql = '''INSERT INTO collisions(hash) VALUES (?)'''

        data = (hsh,)
        self.cur.execute(sql, data)
        self.conn.commit()


    def search_for_and_and_store_collisions(self):
        sql = '''SELECT hash
                   FROM fileobjs
               GROUP BY hash
                 HAVING COUNT(*)>2'''

        self.cur.execute(sql)

        rows = self.cur.fetchall()
        for row in rows:
            print(row[0])
            self.store_collision_by_hash(row[0])


    def fetch_collision_data(self):
        sql = '''SELECT hash
                   FROM collisions'''

        self.cur.execute(sql)

        rows = self.cur.fetchall()
        for row in rows:
            print(row[0])
            self.query_fileobjs_by_hash(row[0])


    def query_fileobjs_by_hash(self, hsh: str):
        sql = '''SELECT hash, size, filepath
                   FROM fileobjs
                  WHERE hash = ?'''

        data = (hsh, )

        self.cur.execute(sql, data)

        rows = self.cur.fetchall()
        for row in rows:
            print(row)



    def store_file_obj(self, obj):
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

        data = (obj.filepath,
                obj.id,         obj.ext,
                obj.isdir,      obj.isfile, obj.islink, obj.ismount,
                obj.size,       obj.hash)

        self.cur.execute(sql, data)
        self.conn.commit()

