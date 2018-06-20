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

