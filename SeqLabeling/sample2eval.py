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

@file: sample2eval.py

@time: 01/07/2018 12:56 

@desc：       
               
'''              

import os
from SL_config import *

_dir = "CRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx3"
dir_name = os.path.join(result_dir, _dir)
for _file in os.listdir(dir_name):
    if not _file.startswith('Iteration'): continue
    filename = os.path.join(dir_name,_file)
    shuf_cmd = 'gshuf -n 100 -o %s %s' % (filename, file)
    os.system(shuf_cmd)


