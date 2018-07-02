#!/usr/bin/env python

# -*- encoding: utf-8

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
sample_dir = os.path.join(dir_name, 'Sample100')


def gen_sample100():
    if not os.path.exists(sample_dir):
        os.mkdir(sample_dir)
    for _file in os.listdir(dir_name):
        if not _file.startswith('Iteration'): continue
        filename = os.path.join(dir_name, _file)
        sample_file = os.path.join(sample_dir, _file[:4] + _file[-5] + "sample100.txt")
        shuf_cmd = "gshuf -n 100 %s | gsed 's/^/\t/' > %s" % (filename, sample_file)
        os.system(shuf_cmd)
        print("{} generated".format(sample_file))


# gen_sample100()

def count_estimated_label():
    for sample_ in sorted(os.listdir(sample_dir)):
        if not sample_.startswith('Iter'): continue
        sample_file = os.path.join(sample_dir, sample_)
        with open(sample_file) as f:
            label_list = []
            for line in f.readlines():
                label = line.split('\t')[0]
                label_list.append(label)
            prec = 1 - label_list.count('0') / 100
            prec_log_file = os.path.join(sample_dir, 'prec.log')
            os.system("echo iter%s: prec:%.2f >> %s" % (sample_[4], prec, prec_log_file))
            print('Finish counting %s' % sample_)


count_estimated_label()
