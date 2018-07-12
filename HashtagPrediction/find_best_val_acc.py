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

@file: find_best_val_acc.py

@time: 12/07/2018 13:00 

@desc：       
               
'''              
from settings import *
import os
import pandas as pd


for _dir in os.listdir(history_dir):
    if not _dir.startswith('CNN'): continue
    df_max = pd.DataFrame()
    exp_dir = os.path.join(history_dir, _dir)
    for file in os.listdir(exp_dir):
        if not file.endswith('csv'): continue
        hist_file = os.path.join(exp_dir, file)
        df = pd.read_csv(hist_file, index_col=0)
        df_line = df.loc[df['val_acc'].idxmax(), :]
        df_line['name']=file
        df_max = df_max.append(df_line,ignore_index=True)
    cols = df_max.columns.tolist()
    col = [cols[2]] + cols[:2] + cols[3:]
    max_glob = df_max.loc[df_max['val_acc'].idxmax(), :][col]
    max_res_file = os.path.join(history_dir, 'total.txt')
    line = " ".join(max_glob.to_string().split())
    with open(max_res_file, 'a') as f:
        f.write(line+'\n')