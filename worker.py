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
import time

class DownloadWorker(threading.Thread):
    def __init__(self, lst, callback):
        threading.Thread.__init__(self)
        """
        self.url = url
        self.path = path
        self.patchfile = patchfile
        """
        self.callback = callback
        self.lst = lst
        self._run = True

    def run(self):
        retry = 3
        while (retry > 0):
            for e in self.lst:
                if (self._run):
                    try:
                        self.callback(e.url, e.abs_path, e)
                    except Exception as ex:
                        print("On %s: %s" % (e.url, ex))
                        break
                    retry = 1
                else:
                    break
            time.sleep(3)
            retry -= 1

    def stop(self):
        self._run = False
