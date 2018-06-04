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

from .settings import *

import pickle, os

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