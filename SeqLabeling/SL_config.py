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

@file: _config.py

@time: 25/06/2018 22:59 

@desc：       
               
'''              

import os
from nltk.corpus import stopwords
# ------------------------
# extraction config
# ------------------------


work_dir = os.path.dirname(__file__)

data_dir = os.path.join(work_dir, 'data')
POS_DATA = os.path.join(data_dir, 'pos.csv')
NEG_DATA = os.path.join(data_dir, 'neg.csv')

IN_SIGN = 'I'
OUT_SIGN = 'O'


model_dir = os.path.join(work_dir, 'Model')

TEST_SET_FRAC = 0.2
L1_penalty = 0.1
L2_penalty = 0.1
MAX_ITER = 2000
CRF_MODEL = 'CRF_L1{%s}_L2{%s}_Iter%s.model' % (L1_penalty, L2_penalty,MAX_ITER)
MODEL_FILE = os.path.join(model_dir, CRF_MODEL)

from _utils import timeit

SEED = 2018