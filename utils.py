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

HEADERS = {"User-Agent": "AQUA_HTTP"}

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
        print("GET %s (%d)" % (url, r.status_code))
    return (r.status_code)

def get(url):
    r = requests.get(url, headers=HEADERS)
    if (r.status_code >= 400):
        return (None)
    return (r.text)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield (l[i:i + n])