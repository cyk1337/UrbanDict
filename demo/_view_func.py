#!/usr/bin/env python

# -*- encoding: utf-8

'''
                      ______   ___  __
                     / ___\ \ / / |/ /
                    | |    \ V /| ' / 
                    | |___  | | | . \ 
                     \____| |_| |_|\_\
 ==========================================================================
@author: Yekun Chai

@license: School of Informatics, Edinburgh

@contact: s1718204@sms.ed.ac.uk

@file: _view_func.py

@time: 02/07/2018 11:37 

@desc：       
               
'''
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def find_all_entries(seg_url, ud):
    base_url = "https://www.urbandictionary.com"
    url = urljoin(base_url, seg_url)
    response = requests.get(url)
    if response.status_code != 200:
        print("No entry found!")
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    defid_nodes = soup.select('div.def-panel')
    word_nodes = soup.select('.word')
    defn_nodes = soup.select('div .meaning')

    for defid_nd, word_nd, defn_nd in zip(defid_nodes, word_nodes, defn_nodes):
        word = word_nd.get_text()
        if ' ' in word:
            print("Remove %s" % word)
            continue
        defid = defid_nd.get('data-defid')
        defn = defn_nd.get_text()
        row_ = dict()
        row_['defid'] = defid
        row_['word'] = word
        row_['defn'] = defn
        ud.append(row_)

    # recursively find next page link
    next_page = soup.select('#content div.pagination-centered ul.pagination a[rel="next"]')
    if len(next_page) > 0:
        for next_href in next_page:
            next_url = next_href.get('href')
            find_all_entries(next_url, ud)
    if len(ud) > 0:
        return ud


def search_UrbanDict(word):
    seg_url = "/define.php?term=%s" % word
    ud = []
    results = find_all_entries(seg_url, ud)
    return results


if __name__ == '__main__':
    r = search_UrbanDict('ur')
    print(r)
    print(len(r))
