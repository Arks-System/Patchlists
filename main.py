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
import time
import queue
import threading
import requests

import utils
import worker

HEADERS = {"User-Agent": "AQUA_HTTP"}
BASEURL = "http://patch01.pso2gs.net/patch_prod/patches/"
MANAGEMENT = "management_beta.txt"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
PATCHLISTS = {"MasterURL": "", "PatchURL": ""}

Lock = threading.Lock()

class PatchFile:
    def __init__(self, l):
        self.filename = os.path.basename(l[0])
        self.path = l[0]
        self.folder = os.path.dirname(l[0])
        self.hash = l[1]
        self.size = int(l[2])
        if (len(l) > 4):
            self.g = True
        else:
            self.g = False
        self.flags = "\t".join(l[3:])
        self.setbase(l[3])
        self.abs_path = utils.join_path(BASEDIR, l[0])
        self.abs_path = "%s/%s" % (os.path.abspath(PATCHLISTS[self.list].replace("http://download.pso2.jp/", "")), self.path)

    def setbase(self, f):
        self.location = f
        if (self.location == 'm'):
            self.url = "%s%s" % (PATCHLISTS["MasterURL"], self.path)
            self.list = "MasterURL"
        elif (self.location == 'p'):
            self.url = "%s%s" % (PATCHLISTS["PatchURL"], self.path)
            self.list = "PatchURL"

    def __repr__(self):
        s = "%s\t%s\t%d\t%s" % (self.path, self.hash, self.size, self.flags)
        return (s)

def get(url):
    r = requests.get(url, headers=HEADERS)
    return (r.text)

def build_list(l):
    lst = []
    for e in l.split('\n'):
        e = e.strip().split('\t')
        if (len(e) < 2):
            continue
        #print(e)
        fle = PatchFile(e)
        lst.append(fle)
    return (lst)

def get_management():
    url = "%s%s" % (BASEURL, MANAGEMENT)
    lst = {}

    r = requests.get(url, headers=HEADERS)
    print("GET %s (%d)" % (url, r.status_code))
    if (r.status_code < 400):
        #print(r.text)

        path = os.path.join(BASEDIR, url.replace("http://patch01.pso2gs.net/", ""))
        path = os.path.normpath(path)
        if (not os.path.exists(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, "wb+") as f:
            f.write(r.content)

        for e in r.text.split('\n'):
            e = e.strip().split('=')
            if (len(e) > 1):
                if (e[0] in ["MasterURL", "PatchURL"]):
                    PATCHLISTS[e[0]] = e[1]
                    lst[e[0]] = e[1]
        for e in r.text.split('\n'):
            e = e.strip().split('=')
            if (len(e) > 1):
                if (e[0] in ["PatchURL"]):
                    lst["patchlist"] = build_list(get("%s/patchlist.txt" % (e[1])))
    return (lst)

def sync_retrieve_files(url, path, patchfile):
    """
    print(url)
    print(path)
    print(patchfile)
    sys.exit(1)
    """
    #####
    if (os.path.exists(path) and utils.hash_md5(path) == patchfile.hash):
        print("GET {%s}%s (%.3fMB) OK" % (patchfile.list.replace("URL", "Base"), patchfile.path, float(patchfile.size) / 1024 / 1024))
    else:
        with Lock:
            utils.create_path(os.path.dirname(path))

        r = requests.get(url, headers=HEADERS)
        print("GET {%s}%s (%.3fMB) %d" % (patchfile.list.replace("URL", "Base"), patchfile.path, float(patchfile.size) / 1024 / 1024, r.status_code))
        if (r.status_code < 400):
            with open(path, "wb+") as f:
                f.write(r.content)

if (__name__ == "__main__"):
    print("Retrieving Management file")
    manag = get_management()
    for key, val in PATCHLISTS.items():
        if (key in ["MasterURL", "PatchURL"]):
            p = utils.join_path(BASEDIR, val.replace("http://download.pso2.jp/", ""))
            if (not os.path.exists(p)):
                utils.create_path(p)
                print("Creating %s folder: %s" % (key, p))
            utils.dl("%spatchlist.txt" % (val), utils.join_path(p, "patchlist.txt"))
    print("Retrieving files")
    total = len(manag["patchlist"])
    current = 0

    """Threading"""
    threads = []
    max_threads = 4

    #for i in range(0, len(manag["patchlist"]) / max_threads, max_threads):
        #current += 1
        #path = utils.join_path(PATCHLISTS[e.list].replace("http://download.pso2.jp", ""), e.path)
    p = manag["patchlist"]
    lst = []

    step = int(len(p) / max_threads) + 1
    for i in range(0, len(manag["patchlist"]), step):
        lst.append(manag["patchlist"][i:i + step])
        pass

    for i in range(max_threads):
        """Threading"""
        #url = "%s%s" % (PATCHLISTS[e.list], e.path)
        #path = "%s%s" % (BASEDIR, path)

        #lst = utils.chunks(manag["patchlist"], int(len(p) / max_threads) + int(len(p) % max_threads))
        """
        if ((current - 1) % max_threads == 0 and current - 1 != 0):
            for t in threads:
                t.join()
            threads = []
        """
        work = worker.DownloadWorker(lst[i], sync_retrieve_files)
        work.start()
        threads.append(work)
    for t in threads:
        t.join()
        """
        print("[%d/%d]" % (current, total), end=' ')
        sync_retrieve_files("%s%s" % (PATCHLISTS[e.list], e.path), "%s%s" % (BASEDIR, path), e)
        """
