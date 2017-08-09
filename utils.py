#!/usr/bin/env python3
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
# pylint: disable=W0621
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0325
# pylint: disable=C0301

import os
import requests
import hashlib
import psutil

HEADERS = {"User-Agent": "AQUA_HTTP"}
LOCKFILE = "/tmp/patchlist.lock"

def hash_md5(file):
    BLOCKS = 65536
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKS)
        while (len(buf) > 0):
            hasher.update(buf)
            buf = afile.read(BLOCKS)
    return (hasher.hexdigest().upper())

def create_path(p):
    if (not os.path.exists(p)):
        os.makedirs(p)

def join_path(b, p):
    path = os.path.join(b, p)
    path = os.path.normpath(path)
    return (path)

def dl(url, path):
    r = requests.get(url, headers=HEADERS)
    if (r.status_code < 400):
        with open(path, "wb+") as f:
            f.write(r.content)
    return (r.status_code)

def get(url):
    r = requests.get(url, headers=HEADERS)
    print("GET %s (%d)" % (url, r.status_code))
    if (r.status_code >= 400):
        return (None)
    return (r.text)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield (l[i:i + n])

def lock():
    with open(LOCKFILE, "w+") as f:
        f.write(str(os.getpid()))

def unlock():
    os.unlink(LOCKFILE)

def is_locked():
    if (os.path.exists(LOCKFILE)):
        pid = 0
        with open(LOCKFILE, "r") as f:
            pid = int(f.read())
        if (pid in psutil.pids()):
            return (True)
        else:
            unlock()
    return (False)
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return (False)
    else:
        return (True)
    """
