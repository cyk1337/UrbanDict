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

c=0

val_acc = np.array([0.9322, 0.9496, 0.9444])

# min count 20
var_map1 = np.array([7, 6, 6]) / 305
var_map2 = np.array([25, 16, 16])/ 305
var_map3 = np.array([26,20, 20])/ 305


c1 = pearsonr(val_acc, var_map1)[0]
c2 = pearsonr(val_acc, var_map2)[0]
c3 = pearsonr(val_acc, var_map3)[0]
c0 = (c1+c2+c3)/3
c+=c0
# v1 = np.corrcoef(val_acc, var_map1)[1,0]
# v2 = np.corrcoef(val_acc, var_map2)[1,0]
# v3 = np.corrcoef(val_acc, var_map3)[1,0]
print("Min count20, vec size50, avg:{:.4f}, c1:{:.4f}, c2:{:.4f}, c3{:.4f}".format(c0,c1,c2,c3))

# min count 5, size 50
var_map1 = np.array([7, 5, 4]) / 386
var_map2 = np.array([17, 13, 16])/ 386
var_map3 = np.array([24, 15, 19])/ 386
c1 = pearsonr(val_acc, var_map1)[0]
c2 = pearsonr(val_acc, var_map2)[0]
c3 = pearsonr(val_acc, var_map3)[0]
c0 = (c1+c2+c3)/3
c+=c0
print("Min count5, vec size50, avg:{:.4f}, c1:{:.4f}, c2:{:.4f}, c3{:.4f}".format(c0,c1,c2,c3))

# min count 5, size 50 remove #,@,link
var_map1 = np.array([7,6, 5]) / 386
var_map2 = np.array([19, 15, 18])/ 386
var_map3 = np.array([25, 17, 22])/ 386
c1 = pearsonr(val_acc, var_map1)[0]
c2 = pearsonr(val_acc, var_map2)[0]
c3 = pearsonr(val_acc, var_map3)[0]
c0 = (c1+c2+c3)/3
c+=c0
print("Min count5, vec size50, rm #@http, avg:{:.4f}, c1:{:.4f}, c2:{:.4f}, c3{:.4f}".format(c0,c1,c2,c3))

# min count 5, size 100
var_map1 = np.array([9, 6,  2]) / 386
var_map2 = np.array([19,11, 16])/ 386
var_map3 = np.array([26, 15, 23])/ 386
c1 = pearsonr(val_acc, var_map1)[0]
c2 = pearsonr(val_acc, var_map2)[0]
c3 = pearsonr(val_acc, var_map3)[0]
c0 = (c1+c2+c3)/3
c+=c0
print("Min count5, vec size100, avg:{:.4f}, c1:{:.4f}, c2:{:.4f}, c3{:.4f}".format(c0,c1,c2,c3))

# min count 5, size 100 remove #,@,link
var_map1 = np.array([9, 6, 5]) / 386
var_map2 = np.array([19, 13, 21])/ 386
var_map3 = np.array([27, 17, 27])/ 386
c1 = pearsonr(val_acc, var_map1)[0]
c2 = pearsonr(val_acc, var_map2)[0]
c3 = pearsonr(val_acc, var_map3)[0]
c0 = (c1+c2+c3)/3
c+=c0
print("Min count5, vec size100, rm #@http, avg:{:.4f}, c1:{:.4f}, c2:{:.4f}, c3{:.4f}".format(c0,c1,c2,c3))

print("Overall avg:{}".format(c/5))