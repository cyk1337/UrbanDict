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
UNLABEL_DATA = os.path.join(data_dir, 'unlabel.csv')

silver_dir = os.path.join(data_dir, 'silver')


result_dir = os.path.join(work_dir, 'SL_result')
eval_dir = os.path.join(result_dir, 'eval')

ERR_LOG = os.path.join(result_dir, 'err.log')
log_dir = os.path.join(result_dir, 'log')

IN_SIGN = 'I'
OUT_SIGN = 'O'


model_dir = os.path.join(work_dir, 'Model')

# split test set fraction
TEST_SET_FRAC = 0.2

SELF_ITERATION = 5
START_ITER_NUM = 0

L1_penalty = 2.35
L2_penalty = 0.08
MAX_ITER = 200
ALGORITHM = 'lbfgs' # {‘lbfgs’, ‘l2sgd’, ‘ap’, ‘pa’, ‘arow’}


from _utils import timeit

SEED = 2018


FEAT_CTX_SIZE = 3

CRF_THRESHOLD = 0.8

CRF_MODEL = 'CRF_%s_Iter%s_L1{%s}_L2{%s}_ctx%s_conf%s' % (ALGORITHM,MAX_ITER, L1_penalty, L2_penalty,FEAT_CTX_SIZE, CRF_THRESHOLD)

# use subset of sample to run code
TEST_MODE = False



