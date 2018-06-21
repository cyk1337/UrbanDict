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

@file: Seed.py

@time: 16/06/2018 14:07 

@desc：       
               
'''              
class Seed(object):
    def __init__(self, word, variant):
        self.word = word
        self.variant = variant

    def __repr__(self):
        return "({},{})".format(self.word, self.variant)

    def __str__(self):
        return "({}, {})".format(self.word, self.variant)

    def __eq__(self, other):
        return self.word==other.word and self.variant==other.variant