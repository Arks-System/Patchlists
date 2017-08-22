#!/usr/bin/env python3

import re
import os
import sys
from datetime import *

from stat import *

r = re.compile(r'^v[0-9]+_rc_[0-9]+_[0-9A-F]+$')
a = [ x for x in os.listdir("./patch_prod/") if r.match(x) != None ]

print(tzinfo)

for e in a:
    s = os.stat(os.path.join("./patch_prod/", e))[ST_MTIME]
    dt = datetime.fromtimestamp(s)
    print("%s (%s)" % (e, dt))
