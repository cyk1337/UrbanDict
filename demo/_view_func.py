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
import spacy
from sklearn.externals import joblib

import sys
sys.path.append('../')
from SeqLabeling.CRF import SelfTrainCRF

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


def extract_variant_spelling(results, model):
    nlp = spacy.load('en')
    label_results = []
    variant_list = []
    for term in results:
        defn = term['defn'].lower()
        term['label_index'] =[]
        doc = nlp(defn, disable=['parser', 'ner', 'textcat'])
        term['toks'] = [w.text for w in doc]
        crf_path = "/Users/yekun/Documents/CODE_/UrbanDict/SeqLabeling/Model/CRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx3/%sCRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx3.model"
        if model.startswith('crf'):
            crf = joblib.load(crf_path % model[-1])
            self_obj = SelfTrainCRF()
            sent_obj = [(w,) for w in doc]
            xseq = self_obj.extract_features(sent_obj)
            y_pred = crf.predict_single(xseq)
            if "I" in y_pred:
                pos_index_list = [pos_indice for pos_indice, y_ in enumerate(y_pred) if y_ == "I"]
                for pos_indice in pos_index_list:
                    pos_prob = crf.predict_marginals_single(xseq)[pos_indice]["I"]
                    if pos_prob > 0.8:
                        term['label_index'].append(pos_indice)
                        variant = term['toks'][pos_indice]
                        variant_list.append(variant)
                        print("Pair: (%s, %s)" % (term['word'],variant))

            label_results.append(term)
    variant_list = list(set(variant_list))
    return label_results, variant_list


def search_UrbanDict(word, model):
    seg_url = "/define.php?term=%s" % word
    ud = []
    results = find_all_entries(seg_url, ud)
    if results is not None:
        label_results, variant_list = extract_variant_spelling(results, model)
        return label_results, variant_list
    else:
        return None, None


if __name__ == '__main__':
    r = search_UrbanDict('ur','crf1')
    # print(r)
    print(len(r))
