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

@file: Definition.py

@time: 16/06/2018 14:07 

@desc：       
               
'''
from _config import *

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re

class Definition(object):
    def __init__(self, word, variant, defn_sent, defid, config=None):
        self.word = word
        self.variant = variant
        self.tuple = (word, variant)
        self.defid = defid

        self.defn_sent = defn_sent
        self.ctx_bef = []
        self.ctx_aft = []

        self.stopwords = stopwords.words('english')

        self.useBothCtx = useBothContext
        self.usePrevCtx = usePreviousContext
        self.useNextCtx = useNextContext
        self.usePosCtx = usePOS4Pattern
        self.match_seed = None
        self.parse_ctx()

    def parse_ctx(self):
        matches = []
        regex_quote = re.compile(r"(?P<quote>['\"])(?P<Variant>\b%s\b)[.]{0,1}(?<!\\)(?P=quote)" % self.variant)
        for m in re.finditer(regex_quote, self.defn_sent):
            matches.append(m)

        if len(matches) == 1:
            self.match_seed = True
            var_span = matches[0].span("Variant")
            start_quote = matches[0].start("quote")
            end_quote = matches[0].end("Variant")+1
            start = 0
            before = word_tokenize(self.defn_sent[start:start_quote])
            after = word_tokenize(self.defn_sent[end_quote+1:])

            if '.' in before:
                ctx_bef = " ".join(before).split('.')[-1:]
            if '.' in after:
                ctx_aft = " ".join(after).split('.')[:1]

            # if length less than ctx window size, pad with <BOS>
            BEF_EMPTY = CONTEXT_WINDOW_SIZE - len(before)
            if not BEF_EMPTY>0:
                ctx_bef = before[-CONTEXT_WINDOW_SIZE:]
            else:
                ctx_bef = ['<BOS>']*BEF_EMPTY + before
            # if length less than ctx window size, pad with <EOS>
            AFT_EMPTY = CONTEXT_WINDOW_SIZE - len(after)
            if not AFT_EMPTY>0:
                ctx_aft = after[:CONTEXT_WINDOW_SIZE]
            else:
                ctx_aft = after + ['<EOS>']*AFT_EMPTY

            ctx_bef = " ".join(ctx_bef)
            ctx_aft = " ".join(ctx_aft)

            # TODO: remove stopwords in context
            self.ctx_bef = ctx_bef
            self.ctx_aft = ctx_aft

            # print(self.ctx_bef)
            # print(self.ctx_aft)


if __name__ == '__main__':
    defn_sent =  'misspelling \'the.\'.'
    word = 'teh'
    variant = 'the'
    defid = 11272
    defn = Definition(word, variant, defn_sent, defid)
    defn.parse_ctx()
