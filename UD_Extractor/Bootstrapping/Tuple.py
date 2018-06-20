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

@file: Tuple.py

@time: 18/06/2018 11:29 

@desc：       
               
'''
from collections import defaultdict
import math

from Bootstrapping.Seed import Seed

class Tuple(Seed):
    def __init__(self, word, variant):
        self.word = word
        self.variant = variant

        self.pattern_list = list()
        self.RlogF_ent_score = None

    def calc_RlogF_score(self):
        numerator = 0
        for pat in self.patterns:
            Fj = len(set(pat.tuples_list))
            numerator += math.log2(Fj+1)
        self.RlogF_ent_score = numerator / len(self.pattern_list)
