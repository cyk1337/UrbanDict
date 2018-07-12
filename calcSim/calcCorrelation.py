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

@file: calcCorrelation.py

@time: 07/07/2018 21:23 

@desc：       
               
'''
import numpy as np
from scipy.stats import pearsonr
from scipy.stats.stats import spearmanr


# glove_w5, vocab size: 33622, formal vacab: simpWiki_vocab, tuple num: 238, correct: 7, top20: 24, top50: 30, top100:37
# cbow_w5, vocab size: 33567, formal vacab: simpWiki_vocab, tuple num: 238, correct: 12, top20: 34, top50: 42, top100:48
# sg_w5, vocab size: 33567, formal vacab: simpWiki_vocab, tuple num: 238, correct: 11, top20: 31, top50: 43, top100:50
#
# en_wiki
# =====
# glove_w5, vocab size: 33622, formal vacab: enWiki_vocab, tuple num: 245, correct: 7, top20: 24, top50: 30, top100:37
# cbow_w5, vocab size: 33567, formal vacab: enWiki_vocab, tuple num: 245, correct: 12, top20: 35, top50: 43, top100:50
# sg_w5, vocab size: 33567, formal vacab: enWiki_vocab, tuple num: 245, correct: 11, top20: 31, top50: 43, top100:50

glove_val_acc =0.934773
cbow_val_acc = 0.927526
sg_val_acc = 0.943991
val_acc = np.array([glove_val_acc, cbow_val_acc, sg_val_acc])

# vocab 50k
var_map1 = np.array([7, 12, 11]) / 238
var_map2 = np.array([24, 34, 31])/238
var_map3 = np.array([30, 42, 43])/ 238


c1 = pearsonr(val_acc, var_map1)[0]
c2 = pearsonr(val_acc, var_map2)[0]
c3 = pearsonr(val_acc, var_map3)[0]
# c0 = (c1+c2+c3)/3
# c+=c0
# v1 = np.corrcoef(val_acc, var_map1)[1,0]
# v2 = np.corrcoef(val_acc, var_map2)[1,0]
# v3 = np.corrcoef(val_acc, var_map3)[1,0]
# print("Min count20, vec size50, avg:{:.4f}, c1:{:.4f}, c2:{:.4f}, c3{:.4f}".format(c0,c1,c2,c3))
print("vocab 100, vec size100, c1:{:.4f}, c2:{:.4f}, c3:{:.4f}".format(c1,c2,c3))


s1 = spearmanr(val_acc, var_map1)[0]
s2 = spearmanr(val_acc, var_map2)[0]
s3 = spearmanr(val_acc, var_map3)[0]
print("vocab 100, vec size100, s1:{:.4f}, s2:{:.4f}, s3:{:.4f}".format(s1,s2,s3))
