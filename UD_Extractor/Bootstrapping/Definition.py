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
from ie_utils import detokenize
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
import re

class Definition(object):
    def __init__(self, word, variant, defn_sent, defid, config=None):
        self.word = word
        self.variant = variant
        self.tuple = (word, variant)
        self.defid = defid

        # self.defn_sent = " ".join(word_tokenize(defn_sent.lower())) # need to deal with space between quote and token
        self.defn_sent = defn_sent.lower()
        self.ctx_bef = None
        self.ctx_aft = None

        self.stopwords = stopwords

        self.useBothCtx = useBothContext
        self.usePrevCtx = usePreviousContext
        self.useNextCtx = useNextContext
        self.usePosCtx = usePOS4Pattern
        self.match_seed = None
        self.isCtxValid = None
        self.isLeftCtxValid = None
        self.isRightCtxValid = None

        self.parse_ctx()

    def parse_ctx(self):
        matches = []
        # regex_quote = re.compile(r"(?P<quote>['\"])(?P<Variant>\b%s\b)[.]{0,1}(?P=quote)" % self.variant)
        regex_quote = re.compile(r"(?P<quote>['\"])(?P<Variant>\b%s\b)[.,]?(?P=quote)" % self.variant)
        # regex_no_quote = re.compile(r"(?P<Variant>\b%s\b)[.]{0,1}" % self.variant)

        for m in re.finditer(regex_quote, self.defn_sent):
            matches.append(m)

        if len(matches) >= 1:
            self.match_seed = True
            var_span = matches[0].span("Variant")
            start_quote = matches[0].start("quote")
            if self.defn_sent[var_span[1]] in ["'", '"']:
                end_quote = var_span[1]+1
            else:
                end_quote = var_span[1]+2
            start = 0
            before = word_tokenize(self.defn_sent[start:start_quote])
            after = word_tokenize(self.defn_sent[end_quote:])

            # If input is multiple sents
            # if '.' in before:
            #     ctx_bef = " ".join(before).split('.')[-1:]
            # if '.' in after:
            #     ctx_aft = " ".join(after).split('.')[:1]

            # if length less than ctx window size, pad with <BOS>
            BEF_EMPTY = CTX_PREV_SIZE - len(before)
            if BEF_EMPTY<=0:
                ctx_bef = before[-CTX_PREV_SIZE:]
            else:
                ctx_bef = [BEGIN_OF_SENT]*BEF_EMPTY + before
            # if length less than ctx window size, pad with <EOS>
            AFT_EMPTY = CTX_NEXT_SIZE - len(after)
            if AFT_EMPTY<=0:
                ctx_aft = after[:CTX_NEXT_SIZE]
            else:
                ctx_aft = after + [END_OF_SENT]*AFT_EMPTY

            ctx_bef = detokenize(ctx_bef)
            ctx_aft = detokenize(ctx_aft)

            # TODO: remove stopwords in context
            self.ctx_bef = ctx_bef
            self.ctx_aft = ctx_aft

            self._count_stopwords_in_ctx()
            if self.isCtxValid:
                print('-' * 80)
                print(self.defn_sent)
                print("Before Ctx: %s" % self.ctx_bef)
                print("After Ctx: %s" % self.ctx_aft)

                # regex_no_quote = re.compile(r"(?P<Variant>\b%s\b)[.]{0,1}" % self.variant)

            for m in re.finditer(regex_quote, self.defn_sent):
                matches.append(m)

        else:
            print("sentence: %s"% self.defn_sent)
            regex_no_quote = re.compile(r"(?P<Variant>\b%s\b)[.]?" % self.variant)
            matches = []
            for m in re.finditer(regex_no_quote, self.defn_sent):
                matches.append(m)
            if len(matches) >= 1:
                self.match_seed = True
                var_span = matches[0].span("Variant")
                start_quote = var_span[0]
                end_quote = var_span[1]
                start = 0
                before = word_tokenize(self.defn_sent[start:start_quote])
                after = word_tokenize(self.defn_sent[end_quote:])

                # If input is multiple sents
                # if '.' in before:
                #     ctx_bef = " ".join(before).split('.')[-1:]
                # if '.' in after:
                #     ctx_aft = " ".join(after).split('.')[:1]

                # if length less than ctx window size, pad with <BOS>
                BEF_EMPTY = CTX_PREV_SIZE - len(before)
                if not BEF_EMPTY > 0:
                    ctx_bef = before[-CTX_PREV_SIZE:]
                else:
                    ctx_bef = [BEGIN_OF_SENT] * BEF_EMPTY + before
                # if length less than ctx window size, pad with <EOS>
                AFT_EMPTY = CTX_NEXT_SIZE - len(after)
                if not AFT_EMPTY > 0:
                    ctx_aft = after[:CTX_NEXT_SIZE]
                else:
                    ctx_aft = after + [END_OF_SENT] * AFT_EMPTY

                # ctx_bef = " ".join(ctx_bef)
                # ctx_aft = " ".join(ctx_aft)
                ctx_bef = detokenize(ctx_bef)
                ctx_aft = detokenize(ctx_aft)

                # TODO: remove stopwords in context
                self.ctx_bef = ctx_bef
                self.ctx_aft = ctx_aft

                self._count_stopwords_in_ctx()
                if self.isCtxValid:
                    print('-' * 80)
                    print(self.defn_sent)
                    print("Before Ctx: %s" % self.ctx_bef)
                    print("After Ctx: %s" % self.ctx_aft)


    def _count_stopwords_in_ctx(self):

        count_bef = 0
        tok_bef = word_tokenize(self.ctx_bef)
        for ctx_tok in tok_bef:
            if ctx_tok in self.stopwords:
                count_bef += 1

        # if count_bef != 0 and count_bef/CTX_SIZE>.6:
        if count_bef != 0 and count_bef == len(tok_bef):
            print("Remove before ctx: %s" % self.ctx_bef)
            if useNextContext is False:
                self.isLeftCtxValid = False
            self.isCtxValid = False
        else:
            self.isCtxValid = True
            self.isLeftCtxValid = True

        # context 'NN' constraint
        # if 'NN' not in [tag_pair[1] for tag_pair in pos_tag(tok_bef)]:
        #     self.isCtxValid = False

        if useNextContext is False:
            return

        count_aft = 0
        tok_aft = word_tokenize(self.ctx_aft)
        for ctx_tok in tok_aft:
            if ctx_tok in self.stopwords:
                count_aft += 1

        # if count_aft != 0 and count_aft/CTX_SIZE>.6:
        if count_aft != 0 and count_aft == len(tok_aft):
            print("Remove after ctx: %s" % self.ctx_aft)
            self.isRightCtxCtxValid = False
        else:
            self.isRightCtxValid = True

if __name__ == '__main__':
    defn_sent =  'alternative spelling for "mates" in text messaging and internet blogs.'
    word = 'mates'
    variant = 'm8'
    defid = 11272
    defn = Definition(word, variant, defn_sent, defid)
    # defn.parse_ctx()
