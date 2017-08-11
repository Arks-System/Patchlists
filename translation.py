#!/usr/bin/env python3

import os
import sys
from stat import *

import utils

BASEDIR = os.path.abspath(os.path.dirname(__file__))
WORKING = "%s/patch_prod/translation/" % (BASEDIR)
PATCHLIST = "%s/patchlist.txt" % (WORKING)

IGNORE = [
        "version.ver",
        "gameversion.ver.pat",
        "patchlist.txt"
        ]

class Translationlist:
    def __init__(self, path):
        self.path = path.replace(WORKING, "")
        self.hash = utils.hash_md5(path)
        self.size = os.stat(path)[ST_SIZE]
        self.flags = "p"

    def __repr__(self):
        s = "%s\t%s\t%d\t%s" % (self.path, self.hash, self.size, self.flags)
        return (s)

if (__name__ == "__main__"):
    translist = []

    if (not os.path.exists(WORKING)):
        print("mkdir %s" % (WORKING))
        os.makedirs(WORKING)

    print("Building patchlist")
    for root, dirs, fls in os.walk(WORKING):
        for f in fls:
            if (f in IGNORE):
                continue
            t = Translationlist(os.path.join(root, f))
            print(t)
            translist.append(t)

    print("\nSaving %s" % (PATCHLIST))
    with open(PATCHLIST, "w+") as f:
        for p in translist:
            print(p, file=f)
