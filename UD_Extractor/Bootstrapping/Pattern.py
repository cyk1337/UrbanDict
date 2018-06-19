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
from ie_utils import detokenize
from nltk.tokenize import word_tokenize
import re


class Pattern(object):
    def __init__(self, ctx_bef, ctx_aft, **kwargs):

        self.ctx_bef = ctx_bef
        self.ctx_aft = ctx_aft

        self.tuples_list = []
        # self.tuples_list.append(tuple)

        # RlogF metric
        self.match_seed_count = 0
        self.match_all_count = 0

        # Snowball metric
        # self.positive = 0
        # self.negtive = 0
        # self.unknown = 0
        self.confidence = 0

        self.patterns = list()
        self.context_before = list()
        self.context_after = list()
        self.PosTagPat = list()

        self.useBothCtx = useBothContext
        self.usePrevCtx = usePreviousContext
        self.useNextCtx = useNextContext
        self.usePosCtx = usePOS4Pattern

        if useNextContext is False:
            self.repr = "%s <Var>" % (self.ctx_bef)
        else:
            self.repr = "%s <Var> %s" % (self.ctx_bef, self.ctx_aft)

    def ctx_match(self, defn_sent, word):
        # word = word.lower()
        bef = self.ctx_bef

        _bef = word_tokenize(self.ctx_bef)
        if '<BOS>' in _bef:
            tok_bef = [tok for tok in _bef if tok != '<BOS>']
            bef = detokenize(tok_bef)


        if useNextContext is False:
            aft = ''
        else:
            aft = self.ctx_aft
            _aft = word_tokenize(self.ctx_aft)
            if '<EOS>' in _aft:
                tok_aft = [tok for tok in _aft if tok != '<EOS']
                aft = detokenize(tok_aft)

        pat = re.compile(r"%s\s(?P<quote>(['\"]|``){0,1})(?P<Variant>\b\w+\b)[.,]{0,1}(?P=quote)%s" % (bef, aft))
        m = pat.search(defn_sent)

        if m is not None:
            var = m.group('Variant')
            pair = (word, var)

            if pair not in self.tuples_list:
                self.tuples_list.append(pair)

            print(defn_sent)
            print("Before: %s" % bef)
            print("Parsing pair: {}".format(pair))
            print('-'*80)

            return pair
        # else:
        #     print(defn_sent)
        #     print("Before: %s" % bef)
        #     print("Didn't match")
        #     print('-'*80)



    def __str__(self):
        return "{}".format(self.repr)

    def __repr__(self):
        return "{}".format(self.repr)


if __name__ == '__main__':
    pat = Pattern(ctx_bef="alternative spelling for", ctx_aft='')
    defn = 'alternative spelling for "mates" in text messaging and internet blogs.'
    pat.ctx_match(defn, word='m8')