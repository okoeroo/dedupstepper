#!/usr/bin/env python3

import os
import hashlib
import uuid
from dataclasses import dataclass, field


def generate_obj_id() -> str:
    return uuid.uuid4().hex


def calc_hash_file(path: str) -> str:
    if os.path.exists(path) and os.path.isfile(path):
        h_s = hashlib.sha256()

        try:
            with open(path, mode='rb') as f:
                # SHA256 blocksize is 64
                # Thus, 16 * 1024 * 64 = 1M
                while chunk := f.read(16 * 1024 * h_s.block_size):
                    h_s.update(chunk)

            return h_s.hexdigest()
        except PermissionError as e:
            print(f"Error: Permission error for path \"{path}\"")
            return None

        except Exception as e:
            print(f"Error: Generic/unknown error \"{str(e)}\" for path \"{path}\"")
            return None

    else:
        return None


@dataclass
class DataObj:
    filepath: str
    id: str = field(default_factory=generate_obj_id)
    basename: str = None
    dirname: str = None
    exists: int = None
    ext: str = None
    isdir: int = None
    isfile: int = None
    islink: int = None
    ismount: int = None
    size: int = None
    # statinfo:

    def __post_init__(self):
        self.basename   = os.path.basename(self.filepath)
        self.dirname    = os.path.dirname(self.filepath)
        self.exists     = os.path.exists(self.filepath)
        self.ext        = os.path.splitext(self.basename)[1]
        self.isdir      = os.path.isdir(self.filepath)
        self.isfile     = os.path.isfile(self.filepath)
        self.islink     = os.path.islink(self.filepath)
        self.ismount    = os.path.ismount(self.filepath)
        self.size       = os.path.getsize(self.filepath)
        self.statinfo   = os.stat(self.filepath)

        # Will take actual time and work to do.
        self.hash       = calc_hash_file(self.filepath)
