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
import math
from collections import defaultdict

from Bootstrapping.Seed import Seed
from _config import *


class Tuple(Seed):
    def __init__(self, word, variant):
        super(Tuple, self).__init__(word, variant)
        # self.word = word
        # self.variant = variant
        self.defid_list = []

        self.overallscore=None
        self.score_dict = defaultdict(float)
        self.threshold = None

        self.pattern_list = list()

        self.RlogF_ent_score = None
        self.numerator = None
        self.denom = None

        self.confidence = 0
        self.confidence_simple = 0

        # threshold
        self.RlogF_threshold = 1
        self.conf_threshold = 0

    def _calc_RlogF_score(self):
        """
        # Basilisk 2002,
         https://aclanthology.info/pdf/W/W02/W02-1028.pdf
        """
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

    def _calc_RlogF_score_improved(self):

        numerator = 0
        Fj_list = []
        for pat in self.pattern_list:
            # Fj = len(set(pat.tuples_list))
            Fj = pat.match_seed_count
            numerator += math.log2(Fj + 1)
            Fj_list.append(Fj)
        self.numerator = Fj_list
        self.denom = len(self.pattern_list)
        self.RlogF_ent_score = numerator / len(self.pattern_list)
        self.RlogF_ent_score *= math.log2(len(self.defid_list)+1)


    def _calc_snowball_conf_simple(self):
        """
            # Snowball 2000, defn 4
            ftp://ftp.cse.buffalo.edu/users/azhang/disc/disc01/cd1/out/papers/dl/p85-agichtein.pdf
        """
        conf = 1
        for p in self.pattern_list:
            conf *= (1-p.confidence)
        self.confidence_simple = 1- conf

    def calc_tuple_score(self):
        if USE_RlogF is True:
            self.threshold = self.RlogF_threshold
            self._calc_RlogF_score()
            self.score_dict['RlogF']=self.RlogF_ent_score
            self.overallscore = self.score_dict['RlogF']
        elif USE_RlogF_IMPROVE is True:
            self.threshold = self.RlogF_threshold
            self._calc_RlogF_score()
            self.score_dict['RlogF_improved']=self.RlogF_ent_score
            self.overallscore = self.score_dict['RlogF_improved']
        elif USE_SNOWBALL_SIMPLE is True:
            self.threshold = self.conf_threshold
            self._calc_snowball_conf_simple()
            self.score_dict['Snowball_simple'] = self.confidence_simple
            self.overallscore  = self.score_dict['Snowball_simple']



    def __str__(self):
        if self.overallscore is not None:
            return "({}, {})\t{}\t {}".format(self.word, self.variant,self.overallscore, self.defid_list)
        else:
            return "({}, {})".format(self.word, self.variant)

if __name__ == '__main__':
    # t = Tuple(1,2)
    # t2 = Tuple(1,2)
    # print(t in [t2])
    # from eval import save_iter
    #
    # save_iter(1, [t,t2], 'test', exp_name='test')
    from eval import load_iter
    t_list = load_iter(0, 'tup.pkl')
    for t in t_list:
        print(t.defid_list, t.pattern_list, t)

