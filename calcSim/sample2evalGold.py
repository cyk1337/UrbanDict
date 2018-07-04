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

@file: sample2evalGold.py

@time: 04/07/2018 19:05 

@desc：       
               
'''
import pandas as pd
import os

# silver_file = '/Users/yekun/Documents/CODE_/UrbanDict/SeqLabeling/data/silver/CRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx4_conf0.9/0pos.csv'
#
# gold_samp_df = pd.read_csv(silver_file, sep='\t')
#
# sample_df = gold_samp_df.sample(1500)
#
# sample_df.to_csv('sample1500', sep='\t', index=False, header=False)

filename = ''
sample_file = ''
shuf_cmd = "gshuf -n 1500 %s | gsed 's/^/\t/' > %s" % (filename, sample_file)
os.system(shuf_cmd)