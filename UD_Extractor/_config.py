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

@time: 12/06/2018 16:19 

@desc：       
               
'''

import os
from nltk.corpus import stopwords
# ------------------------
# extraction config
# ------------------------

work_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.join(work_dir, 'data')
SEED_FILE = os.path.join(data_dir, 'seed.txt')

VALID_FILE = os.path.join(data_dir, 'spelling_variants_valid.txt')
VAL_pkl = os.path.join(data_dir, 'val_rec.pkl')

pkl_dir = os.path.join(work_dir, 'pkl')

iter_dir = os.path.join(work_dir, 'iter_result')
prec_dir = os.path.join(iter_dir, 'prec')
rec_dir = os.path.join(iter_dir, 'rec')

Bootstrap_dir = os.path.join(iter_dir, 'Bootstrap')


BEGIN_OF_SENT = 'BOS'
END_OF_SENT = 'EOS'

MAX_ITER = 5

# nltk word_tokenize usually transforms the double quote " to two forward quotes `` and backward quotes ''
stopword_list = stopwords.words('english')
# stopword_list.remove('of')
stopwords = stopword_list + ['``',"''",'(',')','"',"'","'re",BEGIN_OF_SENT,END_OF_SENT]

#***use all the context from the start
useBothContext=True
# enableAllContext=False

#***use context on the left
usePreviousContext= True

CTX_PREV_SIZE = 3
CTX_NEXT_SIZE = 1

#***use context on the right
useNextContext = False

#***the context should be at least this long
minWindow4Pattern = 2

#***the context can be at most this long
maxWindow4Pattern = 4

#***use POS tag restriction for the target phrase
usePOS4Pattern = False

#***remove all adjectives from the text
removeAdjPattern = False

# minimum number of patterns that generated a tuple so that tuple can be used in the clustering phase
min_pattern_support=2

