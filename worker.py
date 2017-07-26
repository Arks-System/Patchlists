#!/usr/bin/env python3
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
# pylint: disable=W0621
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0325
# pylint: disable=C0301

import os
import sys
import threading

class DownloadWorker(threading.Thread):
    def __init__(self, url, path, patchfile, callback):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path
        self.patchfile = patchfile
        self.callback = callback

    def run(self):
        self.callback()
