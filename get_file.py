#!/usr/bin/env python3
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
# pylint: disable=C0111
# pylint: disable=W0621
# pylint: disable=C0103
# pylint: disable=C0325

import hashlib
import requests

def hash(file):
    BLOCKS = 65536
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKS)
        while (len(buf) > 0):
            hasher.update(buf)
            buf = afile.read(BLOCKS)
    return (hasher.hexdigest().upper())

def build_patch(path, lst):
    pass
