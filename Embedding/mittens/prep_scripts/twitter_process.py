#!/usr/bin/python
"""
Process Twitter to extract only English text, and preprocess it for use.
"""

import sys
import concatenate_corpus
import twokenize # https://github.com/myleott/ark-twokenize-py

if __name__ == '__main__':
    for line in concatenate_corpus.concatenate_main():
        toks = line.split('\t')
        if len(toks) <= 6:
            continue
        lang = toks[-6]
        txt = toks[2]
        if lang == 'en':
            print ' '.join(twokenize.tokenize(txt)).lower()
