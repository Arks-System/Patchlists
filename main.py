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
import signal

import shutil

import utils
import worker

HEADERS = {"User-Agent": "AQUA_HTTP"}
BASEURL = "http://patch01.pso2gs.net/patch_prod/patches/"
MANAGEMENT = "management_beta.txt"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
PATCHLISTS = {"MasterURL": "", "PatchURL": ""}
MIRROR_URL = "https://patch.arks-system.eu/"

Lock = threading.Lock()
threads = []

class PatchFile:
    def __init__(self, l):
        if (len(l) <= 3):
            self.filename = os.path.basename(l[0])
            self.path = l[0]
            self.folder = os.path.dirname(l[0])
            self.hash = l[2]
            self.size = int(l[1])
            self.g = False
            self.flags = "p"
            self.setbase("p")
        else:
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
        self.abs_path = "%s/%s" % (os.path.abspath(PATCHLISTS[self.list].replace("http://aws-download.pso2.jp/", "")), self.path)
        self.old_path = utils.join_path("%s/%s" % (BASEDIR, "patch_prod/patches"), self.path)

    def setbase(self, f):
        self.location = f
        if (self.location == 'm'):
            self.url = "%s%s" % (PATCHLISTS["MasterURL"], self.path)
            self.list = "MasterURL"
        elif (self.location == 'p'):
            self.url = "%s%s" % (PATCHLISTS["PatchURL"], self.path)
            self.list = "PatchURL"

    def get_oldlisting(self):
        s = "%s\t%d\t%s\t%s" % (self.path, self.size, self.hash, self.flags)
        return (s)

    def __repr__(self):
        s = "%s\t%s\t%d\t%s" % (self.path, self.hash, self.size, self.flags)
        return (s)

def get(url):
    r = requests.get(url, headers=HEADERS)
    return (r.text)

def build_list(l):
    lst = []
    if (l == None):
        return (lst)
    for e in l.split('\n'):
        e = e.strip().split('\t')
        if (len(e) < 2):
            continue
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
                    lst["patchlist"] = build_list(get("%spatchlist.txt" % (e[1])))
                    lst["patchlist_always"] = build_list(get("%spatchlist_always.txt" % (e[1])))
                    lst["launcherlist"] = build_list(get("%slauncherlist.txt" % (e[1])))
    return (lst)

def write_management():
    url = "%s%s" % (BASEURL, MANAGEMENT)
    path = os.path.join(BASEDIR, url.replace("http://patch01.pso2gs.net/", ""))
    path = os.path.normpath(path)

    print(path)
    if (not os.path.exists(os.path.dirname(path))):
        os.makedirs(os.path.dirname(path))
    r = requests.get(url, headers=HEADERS)
    if (r.status_code >= 400):
        raise Exception("Could not get management for writing")
    with open(path, "wb+") as f:
        data = r.content
        try:
            data = data.replace(b"http://aws-download.pso2.jp/", MIRROR_URL.encode('us-ascii'))
            print("  %s will be used as 'MIRROR_URL'" % (MIRROR_URL))
            transurl = "TranslationURL=%spatch_prod/translation/\r\n" % (MIRROR_URL)
            print("  Appending Translation URL: %s" % (transurl.replace("\r\n", "")))
            data += transurl.encode('us-ascii')
        except NameError as e:
            print("  http://aws-download.pso2.jp/ will be used as 'MIRROR_URL'")
        print(data.decode("us-ascii"), end="")
        f.write(data)

def is_up_to_date(f, p):
    return ((os.path.exists(p.old_path) and utils.hash_md5(p.old_path) == p.hash) or (os.path.exists(f) and utils.hash_md5(f) == p.hash))

def sync_retrieve_files(url, path, patchfile):
    if (not is_up_to_date(path, patchfile)):
        #print("CHK {%s}%s (%.3fMB) OK" % (patchfile.list.replace("URL", "Base"), patchfile.path, float(patchfile.size) / 1024 / 1024))
        with Lock:
            utils.create_path(os.path.dirname(path))
        r = requests.get(url, headers=HEADERS)
        print("GET {%s}%s (%.3fMB) %d" % (patchfile.list.replace("URL", "Base"), patchfile.path, float(patchfile.size) / 1024 / 1024, r.status_code))
        if (r.status_code < 400):
            with open(path, "wb+") as f:
                f.write(r.content)
    #else:
        #print("CHK {%s}%s (%.3fMB) OK" % (patchfile.list.replace("URL", "Base"), patchfile.path, float(patchfile.size) / 1024 / 1024))

def thread_pool(p):
    lst = []

    print(" > ", end="")
    print(len(p))
    step = int(len(p) / max_threads) + 1
    for i in range(0, len(p), step):
        lst.append(p[i:i + step])

    for i in range(max_threads):
        if (i >= len(lst)):
            #print("BREAK")
            break
        work = worker.DownloadWorker(lst[i], sync_retrieve_files)
        work.start()
        threads.append(work)
    signal.signal(signal.SIGINT, signal_handler)
    for t in threads:
        t.join()
"""
def publish_repository(path, patchfile):
    for e in patchfile:
        if (not os.path.exists(os.path.dirname(e.old_path))):
            utils.create_path(os.path.dirname(e.old_path))
        if (os.path.exists(e.abs_path)):
            if (os.path.exists(e.old_path)):
                os.unlink(e.old_path)
            shutil.copy(e.abs_path, e.old_path)
            print("Publishing %s" % (e.path))
"""
def signal_handler(signal, frame):
    for t in threads:
        if (t.is_alive()):
            t.stop()
            t.join()
    print("Exiting...")
    sys.exit(1)

if (__name__ == "__main__"):
    lsts = ["patchlist.txt", "launcherlist.txt", "patchlist_always.txt"]
    if (utils.is_locked()):
        print("Application already running", file=sys.stderr)
    utils.lock()
    print("Retrieving Management file")
    
    manag = get_management()
    for key, val in PATCHLISTS.items():
        if (key in ["MasterURL", "PatchURL"]):
            p = utils.join_path(BASEDIR, val.replace("http://aws-download.pso2.jp/", ""))
            if (not os.path.exists(p)):
                utils.create_path(p)
                print("Creating %s folder: %s" % (key, p))
            for e in lsts:
                if (utils.dl("%s%s" % (val, e), utils.join_path(p, e)) < 400):
                    print("GET %s" % (e))
    print("Retrieving files")

    max_threads = 4
    for key, val in manag.items():
        if (not key in ["PatchURL", "TranslationURL", "MasterURL"]):
            print("Setting pool for %s" % (key))
            thread_pool(val)

    print("\nRetrieving version")
    for e in [manag["PatchURL"], manag["MasterURL"], "http://aws-download.pso2.jp/patch_prod/patches/"]:
        versionfile = os.path.join(os.path.dirname("%s%s" % (BASEDIR, e.replace("http://aws-download.pso2.jp", ""))), "version.ver")
        gameversionfile = os.path.join(os.path.dirname("%s%s" % (BASEDIR, e.replace("http://aws-download.pso2.jp", ""))), "gameversion.ver.pat")
        if (utils.dl("%sversion.ver" % (e), versionfile) < 400):
            with open(versionfile, "r") as f:
                print("%sversion.ver: %s" %(e.replace("http://aws-download.pso2.jp/patch_prod/", ""), f.read().replace("\n", "")))
        if (utils.dl("%sgameversion.ver.pat" % (e), gameversionfile) < 400):
            with open(versionfile, "r") as f:
                print("%sgameversion.ver.pat: %s" %(e.replace("http://aws-download.pso2.jp/patch_prod/", ""), f.read().replace("\n", "")))
    
    print("Writing management to disk")
    write_management()
    print("PSO2 can now be updated from this mirror")
    utils.unlock()
