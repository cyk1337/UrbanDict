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
import re, math


class Pattern(object):
    def __init__(self, ctx_bef, ctx_aft, **kwargs):

        self.ctx_bef = ctx_bef
        self.ctx_aft = ctx_aft

        self.tuples_list = []
        # self.tuples_list.append(tuple)

        self.scores = []

        # RlogF metric
        self.match_seed_count = 0
        self.match_tot_count = 0
        # self.match_dupl_count = 0
        self.RlogF_score = -1

        # Snowball metric
        # self.positive = 0
        # self.negtive = 0
        # self.unknown = 0
        self.confidence = None

        # self.patterns = list()
        # self.context_before = list()
        # self.context_after = list()
        self.PosTagPat = list()

        self.useBothCtx = useBothContext
        self.usePrevCtx = usePreviousContext
        self.useNextCtx = useNextContext
        self.usePosCtx = usePOS4Pattern

        if useNextContext is False:
            self.repr = "%s <Var>" % (self.ctx_bef)
        else:
            self.repr = "%s <Var> %s" % (self.ctx_bef, self.ctx_aft)


    def ctx_match(self, defn_sent, word, seeds_list):
        # word = word.lower()
        bef = self.ctx_bef

        _bef = word_tokenize(self.ctx_bef)
        if BEGIN_OF_SENT in _bef:
            tok_bef = [tok for tok in _bef if tok != BEGIN_OF_SENT]
            bef = detokenize(tok_bef)
        if '(' in _bef and ')' not in _bef:
            bef = detokenize(tok_bef).replace('(', '\(')


        if useNextContext is False:
            aft = ''
        else:
            aft = self.ctx_aft
            _aft = word_tokenize(self.ctx_aft)
            if END_OF_SENT in _aft:
                tok_aft = [tok for tok in _aft if tok != END_OF_SENT]
                aft = detokenize(tok_aft)

        try:
            pat = re.compile(r"%s\s(?P<quote>['\"]?)(?P<Variant>[\w-]+)[.,]?(?P=quote)%s" % (bef, aft))
        except:
            return
        m = pat.search(defn_sent.lower())

        if m is not None:
            var = m.group('Variant').lower()
            # TODO: rule `way of spelling` the name "xx", also require compute word similarity if possible
            # if var in stopwords:
            #     # Allow for 3 tokens between quote and pattern ctx
            #     pat_ = re.compile(r"%\s(\w+|\s){0,6}(?P<q>(['\"]|``))(?P<Variant>[\w-]+)(?P=q)%s" % (bef, aft))
            #     m_ = pat_.search(defn_sent)
            #     if m_ is not None:
            #         var = m_.group('Variant').lower()
            pair = (word, var)
            # self.match_dupl_count += 1
            self.match_tot_count += 1

            if pair not in self.tuples_list:
                self.tuples_list.append(pair)

            if pair in seeds_list:
                self.match_seed_count += 1
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

    def calc_pattern_RlogF_score(self):
        if self.match_seed_count >0 and self.match_tot_count>0:
            self.RlogF_score = (self.match_seed_count/self.match_tot_count) * math.log2(self.match_seed_count)


    def __eq__(self, other):
        if useNextContext is False and self.ctx_bef == other.ctx_bef:
            return True
        if useNextContext is True and self.ctx_bef == other.ctx_bef and self.ctx_aft == other.ctx_aft:
            return True
        else:
            return False

    def __str__(self):
        return "{}".format(self.repr)

    def __repr__(self):
        return "{}".format(self.repr)



if __name__ == '__main__':
    pat = Pattern(ctx_bef="alternative spelling for", ctx_aft='')
    pat2 = Pattern(ctx_bef="alternative spelling for", ctx_aft='')
    # defn = 'alternative spelling for "mates" in text messaging and internet blogs.'
    # pat.ctx_match(defn, word='m8')
    print(pat in [pat2])