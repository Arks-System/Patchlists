#!/usr/bin/env python3

import re
import os
import sys

import shutil

from datetime import *

from stat import *

BASEDIR = os.path.abspath(os.path.dirname(__file__))
WORKING = "%s/patch_prod/" % (BASEDIR)


if (__name__ == "__main__"):
    r = re.compile(r'^v[0-9]+_rc_[0-9]+_[0-9A-F]+$')

    if (os.path.exists(WORKING)):
        a = [ x for x in os.listdir(WORKING) if r.match(x) != None ]
    else:
        sys.exit(0)

    patches = []
    for e in a:
        s = os.stat(os.path.join("./patch_prod/", e))[ST_MTIME]
        dt = datetime.fromtimestamp(s)
        #print("%s\t(%s)" % (e, dt))
        patches.append({"folder": e, "timestamp": s, "datetime": dt})
    st = sorted(patches, key=lambda k: k["timestamp"])
    if (len(st) > 1):
        print("Keeping last (%s, %s)" % (st[-1]["folder"], st[-1]["datetime"]))
        for e in reversed(st[:len(st) - 1]):
            path = "%s%s" % (WORKING, e["folder"])
            print("Removing: %s\t%s (%d)" % (path, e["datetime"], e["timestamp"]))
            if (os.path.exists(path)):
                shutil.rmtree(path)
    elif (len(st) == 1):
        print("Keeping last (%s, %s)" % (st[0]["folder"], st[0]["datetime"]))
    else:
        print("No folders...")
