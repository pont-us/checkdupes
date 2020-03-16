#!/usr/bin/env python3

"""
checkdupes: check duplicate files between directories

By Pontus Lurcock (pont@talvi.net), 2020. Released into the public domain.
"""

import argparse
import hashlib
import os

def main():
    parser = argparse.ArgumentParser(description="Check if all files in "
                                     "additional directory are also "
                                     "present in main directory.")
    parser.add_argument("main", type=str, help="main directory path")
    parser.add_argument("additional", type=str,
                        help="additional directory path")
    args = parser.parse_args()
    compare_directories(args.main, args.additional)


def compare_directories(main_dir, additional_dir):
    main_set = get_filehash_set(main_dir)
    additional_set = get_filehash_set(additional_dir)
    if main_set == additional_set:
        print("The directories contain the same files.")
    elif additional_set <= main_set:
        print("%s is a subset of %s." % (additional_dir, main_dir))
    else:
        print("The following files are in %s but not in %s:" %
              (additional_dir, main_dir))
        for filehash in additional_set - main_set:
            print(filehash.pathname)


def get_filehash_set(path):
    hash_set = set()
    for root, dirs, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                hash_set.add(FileHash(filepath))
    return hash_set


class FileHash:

    def __init__(self, pathname):
        self.pathname = pathname
        hasher = hashlib.sha512()
        with open(pathname, "rb") as fh:
            contents = fh.read()
        hasher.update(contents)
        self.hashcode = hasher.digest()

    def __eq__(self, other):
        return self.hashcode == other.hashcode

    def __hash__(self):
        return int.from_bytes(self.hashcode, byteorder="big")

    
if __name__ == "__main__":
    main()
