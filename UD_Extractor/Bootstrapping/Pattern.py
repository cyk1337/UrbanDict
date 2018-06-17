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

@file: Pattern.py

@time: 12/06/2018 15:55 

@desc：       
               
'''

from _config import *
from nltk.tokenize import word_tokenize


class Pattern(object):
    def __init__(self, context, variant):
        self.ctx = context
        self.var = variant

        self.positive = 0
        self.negtive = 0
        self.unknown = 0
        self.confidence = 0

        self.pattern = list()
        self.context_before = list()
        self.context_after = list()
        self.PosTagPat = list()

        self.useBothCtx = useBothContext
        self.usePrevCtx = usePreviousContext
        self.useNextCtx = useNextContext
        self.usePosCtx = usePOS4Pattern

    def parse_context(self):
        # TODO: parse context according to config
        pass



    def __str__(self):
        return "{}".format(self.pattern)

    def __repr__(self):
        return "{}".format(self.pattern)