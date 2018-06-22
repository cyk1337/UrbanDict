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

@file: data_loader.py

@time: 22/06/2018 18:52 

@desc：       
               
'''
import numpy as np
import pandas as pd

from .settings import *

def load_imdb():
    ## train data
    train_data = pd.read_csv(train_csv)
    X_train = train_data['tweets']
    y_train = train_data['label']
    ## val data
    val_data = pd.read_csv(val_csv)
    X_val = val_data['tweets']
    y_val = val_data['label']
    return (X_train, y_train), (X_val, y_val)


def load_test():
    # test data
    test_data = pd.read_csv(test_csv)
    X_test = test_data['tweets']
    y_test = test_data['label']
    return (X_test, y_test)


def load_pretrained_model(embedding_path):
    # encoding method 1: load pre-trained embedding
    # build mapping for pretrained models
    # dict {word->vector}
    # ====================
    embedding_index = dict()
    with open(embedding_path, encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            if word.isdigit(): continue
            vector = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = vector
    print("Found %s word vectors" % len(embedding_index))
    return embedding_index