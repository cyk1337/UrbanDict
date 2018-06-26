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

work_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.join(work_dir, 'data')
POS_DATA = os.path.join(data_dir, 'pos.csv')
NEG_DATA = os.path.join(data_dir, 'neg.csv')