#!/usr/bin/env python

#-*- encoding: utf-8 

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

@file: ie_utils.py

@time: 03/06/2018 23:57 

@desc：       
               
'''

from _config import *

import pickle, os, string

def dump_pkl(obj, filename):
    if not os.path.exists(pkl_dir):
        os.mkdir(pkl_dir)
    filepath = os.path.join(pkl_dir, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def load_pkl(filename):
    if not os.path.exists(pkl_dir):
        os.mkdir(pkl_dir)
    filepath = os.path.join(pkl_dir, filename)
    with open(filepath, 'rb') as f:
        obj = pickle.load(f)
    return obj


def days_hours_mins_secs(td):
    return "{}d,{}h,{}m,{}s".format(td.days, td.seconds//3600, (td.seconds//60)%60, td.seconds%60)


def detokenize(tokens):
    # TODO: tok 'text' might be => tok'text ', if adding condition -> not i.startswith("'")
    # "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()
    sent = "".join([" " + i if i not in string.punctuation else i for i in tokens]).strip()
    return sent


def iterative_levenshtein(s, t):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    rows = len(s) + 1
    cols = len(t) + 1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row - 1][col] + 1,  # deletion
                                 dist[row][col - 1] + 1,  # insertion
                                 dist[row - 1][col - 1] + cost)  # substitution
    # for r in range(rows):
    #     print(dist[r])

    return dist[row][col]

def normalized_levenshtein(s, t):
    return iterative_levenshtein(s, t)/(len(s)+len(t))