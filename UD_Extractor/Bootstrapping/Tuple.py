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

@time: 16/06/2018 14:07 

@desc：       
               
'''              
class Tuple(object):
    def __init__(self, word, variant, defn_sent, ctx_bef, ctx_aft, defid=None, config=None):
        self.word = word
        self.variant = variant

        self.defid = defid

        self.defn_sent = defn_sent
        self.ctx_bef = ctx_bef
        self.ctx_aft = ctx_aft


