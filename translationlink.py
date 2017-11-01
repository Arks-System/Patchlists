#!/usr/bin/env python

import os
import sys
import requests

from bs4 import BeautifulSoup

BASE="https://pso2.acf.me.uk/Manual/"

def get_url_from_page(src):
    url = []
    soup = BeautifulSoup(src, 'html.parser').find("table")
    soup = soup.find_all('a')

    for e in soup:
        url.append(e['href'])

    return (url)

if (__name__ == "__main__"):
    r = requests.get(BASE)
    if (r.status_code == 200):
        url = get_url_from_page(r.text)
        if (len(url) > 0):
            print(url[0])
    #else:
        #print(r.status_code)
