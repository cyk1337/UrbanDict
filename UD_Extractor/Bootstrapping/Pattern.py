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


class Pattern(object):
    def __init__(self, context):
        self.positive = 0
        self.negtive = 0
        self.unknown = 0
        self.confidence = 0

        self.pattern = list()
        self.context_before = list()
        self.context_after = list()
        self.PosTagPat = list()

    def _all_context(self):
        pass

    def __str__(self):
        return self.pattern

    def __repr__(self):
        return self.pattern