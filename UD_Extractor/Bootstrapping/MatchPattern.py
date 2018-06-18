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

@file: MatchPattern.py

@time: 18/06/2018 19:10 

@desc：       
               
'''              

class MatchPattern(object):
    def __init__(self, pat_obj):
        self.pat = pat_obj
        self.match_seed_count = 0
        self.match_all_count = 0
        self.match = False

    def ctx_match(self, defn_sent):


        return