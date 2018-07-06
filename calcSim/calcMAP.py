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

@file: calcMAP.py

@time: 06/07/2018 11:05 

@desc：       
               
'''
import numpy as np
from gensim.models import Word2Vec

glove50='/Volumes/Ed/embedding/glove50/vectors.txt'
glove_tweet_vocab = '/Volumes/Ed/embedding/glove50/vocab.txt'

cbow50='/Volumes/Ed/embedding/w2v50/cbow/cbow50_win5_min5.txt'
cbow_model='/Volumes/Ed/embedding/w2v50/cbow/cbow50_win5_min5.model'

sg50='/Volumes/Ed/embedding/w2v50/sg/sg50_win5_min5.txt'

gold_tup_file='gold/sample_gold.txt'

simpWiki_vocab = '/Volumes/Ed/data/mittens/simpwiki.txt.vocab'
formal_vocab_file = simpWiki_vocab


def load_embedding(embedding_path):
    embedding_index = dict()
    with open(embedding_path, encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = vector
    print("Load %s word vectors from pretrained file" % len(embedding_index))
    vocab = list(embedding_index.keys())
    return embedding_index, vocab


glove_embedding, informal_vocab =load_embedding(glove50)

with open(formal_vocab_file) as formal_vocab_f:
    formal_vocab = set([line.split()[0] for line in formal_vocab_f])

def filter_variant_tuple(tup_file):
    variants = []
    excluded_formal = 0
    excluded_informal = 0

    f = open(tup_file)
    for line in f:
        (informal, formal) = line.split()
        if formal not in formal_vocab:
            excluded_formal += 1
            continue
        if formal not in informal_vocab or informal not in informal_vocab:
            excluded_informal += 1
            continue
        variants.append((informal, formal))
    f.close()
    print("excluded formal = %i" % excluded_formal)
    print("excluded informal = %i" % excluded_informal)
    return variants

variants = filter_variant_tuple(gold_tup_file)
print("%i evaluation pairs" % len(variants))

def evaluate_pair(tup, N=1000):
    # TODO: calculate the embedding cosine distance and return whether the rank of current exrtacted variant
    # 1. embedding dict values to np matrix
    # 2. calculate cosine similarity
    # 3. argsort
    # 4. find rank
    pass

def evaluate_all_pairs():
    correct_cnt = 0
    top20_cnt = 0
    error_cnt = 0
    ranks = []
    for x in variants:
        try:
            rank = evaluate_pair(x, N=10000)
            ranks.append(rank)
            if int(rank) == 0:
                correct_cnt += 1
            if int(rank) < 20:
                top20_cnt += 1
        except:
            error_cnt += 1
            continue

    print(ranks)
    print("%i pairs error" % error_cnt)
    print("%i pairs correct" % correct_cnt)
    print("%i pairs in top 20" % top20_cnt)

if __name__ == '__main__':
    evaluate_all_pairs()