#!/usr/bin/python
"""
Process Wikipedia to extract only article text, and preprocess it for use.
"""

import codecs
import nltk
import sys

import concatenate_corpus

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

if __name__ == '__main__':
    for l in concatenate_corpus.concatenate_main():
        l = l.strip().lower()
        if not l:
            continue
        if l.startswith(u"<doc id") or l == u"</doc>":
            continue
        for sent in sent_detector.tokenize(l):
            print ' '.join(nltk.word_tokenize(sent)).encode('utf-8')
