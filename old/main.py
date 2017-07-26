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
import requests

import get_file

HEADERS = {"User-Agent": "AQUA_HTTP"}
BASEURL = "http://patch01.pso2gs.net/patch_prod/patches/"
MANAGEMENT = "management_beta.txt"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
PATCHLISTS = {"MasterURL": "", "PatchURL": ""}

class DownloadWorker(threading.Thread):
    def __init__(self, url, path, patchlist, current, total):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path
        self.patchlist = patchlist
        self.current = current
        self.total = total

    def run(self):
        r = requests.get(self.url, headers=HEADERS)
        e = self.patchlist
        if (r.status_code < 400):
            #print("[%d/%d]" % (current, total), end=' ')
            print("[%d/%d] GET %s (%s) (%.3fMb) %d" % (self.current, self.total, e.filename, e.location, float(e.size) / 1024 / 1024, r.status_code), end='\n')
            with open(self.path, 'wb+') as f:
                f.write(r.content)

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

    print("GET %s" % (url))
    r = requests.get(url, headers=HEADERS)
    if (r.status_code < 400):
        print("Status: %d" % (r.status_code))
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
        for e in r.text.split('\n'):
            e = e.strip().split('=')
            if (len(e) > 1):
                #print("%s: %s" % (e[0], e[1]))
                if (e[0] in ["MasterURL", "PatchURL"]):
                    lst[e[0]] = {"url": e[1]}
                    lst[e[0]]["patchlist"] = build_list(get("%s/patchlist.txt" % (e[1])))
    return (lst)

def build_repository(k, l, p):
    print("%s: %s" %(k, path))
    current = 0
    i = 0
    total = len(l)

    threads = []
    max_threads = 128
    #for i in len(l):
    while (i < len(l)):
        e = l[i]
        current += 1
        if (k == "MasterURL"):
            e.setbase("m")
        if (e.list != k):
            continue

        abs_path = os.path.join(p, e.path)
        abs_path = os.path.normpath(abs_path)
        if (not os.path.exists(abs_path) or get_file.hash(abs_path) != e.hash):
            if (not os.path.exists(os.path.dirname(abs_path))):
                os.makedirs(os.path.dirname(abs_path))

        if (i % max_threads == 0 and i != 0):
            for t in threads:
                t.join()
            threads = []

        worker = DownloadWorker(e.url, abs_path, e, i + 1, total)
        worker.start()
        threads.append(worker)

        i += 1
        """
            #print(abs_path)
            #print("[%d/%d]" % (current, total), end=' ')
            #print("GET %s (%s) (%.3fMb)" % (e.filename, e.location, float(e.size) / 1024 / 1024), end=' ')

            #print(PATCHLISTS[e.list])

            r = requests.get(e.url, headers=HEADERS)
            print("%d" % (r.status_code))
            if (r.status_code < 400):
                with open(abs_path, 'wb+') as f:
                    f.write(r.content)
            #print(" (%d)" % (r.status_code))
        """

if (__name__ == "__main__"):
    lst = get_management()

    for key, val in lst.items():
        url = "%spatchlist.txt" % (val['url'])
        path = os.path.join(BASEDIR, val['url'].replace("http://download.pso2.jp/", ""))
        path = os.path.normpath(path)
        print(path)
        if (not os.path.exists(path)):
            os.makedirs(path)
        with open("%s/patchlist.txt" % (path), 'wb+') as f:
            print("GET %s" % (url))
            r = requests.get(url, headers=HEADERS)
            print(r.status_code)
            f.write(r.content)
        print("Building repository")
        build_repository(key, val["patchlist"], path)



"""
TODO:

1. Download MasterURL: http://download.pso2.jp/patch_prod/v41000_rc_85_masterbase/patches/patchlist.txt
2. Download PatchURL: http://download.pso2.jp/patch_prod/v50001_rc_28_583F1C31/patches/patchlist.txt
3. Create file list: Patch > Master
4. Download files
5. Publish files
"""
