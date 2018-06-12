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

# ------------------------
# extraction config
# ------------------------

work_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.join(work_dir, 'data')
SEED_FILE = os.path.join(data_dir, 'seed.txt')

pkl_dir = os.path.join(work_dir, 'pkl')


#***use all the context from the start
enableAllContext=False

#***use context on the left
usePreviousContext= True

CONTEXT_WINDOW_SIZE = 4

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