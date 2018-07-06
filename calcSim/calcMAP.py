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
import os
from gensim.models import Word2Vec
from numba import jit

glove50='/Volumes/Ed/embedding/glove50/vectors.txt'
glove_tweet_vocab = '/Volumes/Ed/embedding/glove50/vocab.txt'

cbow50='/Volumes/Ed/embedding/w2v50/cbow/cbow50_win5_min5.txt'
cbow_model='/Volumes/Ed/embedding/w2v50/cbow/cbow50_win5_min5.model'

sg50='/Volumes/Ed/embedding/w2v50/sg/sg50_win5_min5.txt'

gold_tup_file='gold/sample_gold.txt'

simpWiki_vocab = '/Volumes/Ed/data/mittens/simpwiki.txt.vocab'
formal_vocab_file = simpWiki_vocab

result_dir = 'result'

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

EXP_ = 'glove50'
_embedding, informal_vocab =load_embedding(glove50)

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

@jit
def evaluate_pair(tup, word_vectors, N=1000):
    # TODO: calculate the embedding cosine distance and return whether the rank of current exrtacted variant
    word = tup[0]
    variant = tup[1]
    var_vec = _embedding[word]
    # 1. embedding dict values to np matrix
    # print(word_vectors.shape)
    dst = np.dot(word_vectors, var_vec.T) / np.linalg.norm(word_vectors, axis=1) / np.linalg.norm(var_vec)
    word_ids = np.argsort(-dst)[1:N+1]
    # 2. calculate cosine similarity
    # 3. argsort
    # 4. find rank
    topN = [(informal_vocab[i], dst[i]) for i in word_ids]
    topN_words = [r[0] for r in topN]
    rank = -1
    if variant in topN_words:
        rank = topN_words.index(variant)
        # print(tup, rank)
    return rank

def evaluate_all_pairs():
    correct_cnt = 0
    top20_cnt = 0
    error_cnt = 0
    ranks = []
    exp_dir = os.path.join(result_dir, EXP_)
    os.system('mkdir -p %s' % exp_dir)
    top1_file = os.path.join(exp_dir, 'top1')
    top20_file = os.path.join(exp_dir, 'top20')
    f_top1 = open(top1_file, 'w')
    f_top20 = open(top20_file, 'w')
    word_vectors = np.array([v for v in _embedding.values()])
    for tup in variants:
        try:
            rank = evaluate_pair(tup, word_vectors, N=10000)
            if rank!= -1:
                ranks.append(rank)
            if int(rank) == 0:
                print("Top 1:", tup, rank)
                f_top1.write("{}\t{}\n".format(tup, rank))
                correct_cnt += 1
            if int(rank) < 20:
                top20_cnt += 1
                print("Top 20:", tup, rank)
                f_top20.write("{}\t{}\n".format(tup, rank))
        except:
            error_cnt += 1
            print("Error:", tup)
            continue

    print(ranks)
    print("%i pairs error" % error_cnt)
    print("%i pairs correct" % correct_cnt)
    print("%i pairs in top 20" % top20_cnt)

if __name__ == '__main__':
    evaluate_all_pairs()