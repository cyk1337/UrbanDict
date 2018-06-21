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
        super(Tuple, self).__init__(word, variant)
        # self.word = word
        # self.variant = variant
        self.defid_list = []

        self.pattern_list = list()
        self.RlogF_ent_score = None
        self.numerator = None
        self.denom = None

    def calc_RlogF_score(self):
        numerator = 0
        Fj_list = []
        for pat in self.pattern_list:
            # Fj = len(set(pat.tuples_list))
            Fj = pat.match_seed_count
            numerator += math.log2(Fj+1)
            Fj_list.append(Fj)
        self.numerator= Fj_list
        self.denom = len(self.pattern_list)
        self.RlogF_ent_score = numerator / len(self.pattern_list)

    def __str__(self):
        if self.RlogF_ent_score is not None:
            return "({}, {})\t{}".format(self.word, self.variant,self.RlogF_ent_score)
        else:
            return "({}, {})".format(self.word, self.variant)

if __name__ == '__main__':
    t = Tuple(1,2)
    t2 = Tuple(1,2)
    print(t in [t2])
    from eval import save_iter

    save_iter(1, [t,t2], 'test', exp_name='test')

