#!/usr/bin/env python

# -*- encoding: utf-8

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
from numba import jit
import pandas as pd

# glove50 = '/Volumes/Ed/embedding/glove50/vectors.txt'
# glove100 = '/Volumes/Ed/embedding/glove100/vectors.txt'
# glove_tweet_vocab = '/Volumes/Ed/embedding/glove50/vocab.txt'
#
# cbow50 = '/Volumes/Ed/embedding/w2v50/cbow/cbow50_win5_min5.txt'
# cbow100 = '/Volumes/Ed/embedding/w2v100/cbow/cbow100_win5_min5.txt'
#
# sg50 = '/Volumes/Ed/embedding/w2v50/sg/sg50_win5_min5.txt'
# sg100 = '/Volumes/Ed/embedding/w2v100/sg/sg100_win5_min5.txt'
#
# # min count 20
# glove50_min20 = '/Volumes/Ed/embedding/glove50_min20/tweet_vectors_min20.txt.txt'
#
# sg50_min20 = '/Volumes/Ed/embedding/w2v50_min20/sg/sg50_win5_min20.txt'
# cbow50_min20 = '/Volumes/Ed/embedding/w2v50_min20/cbow/cbow50_win5_min20.txt'

# EXP_ = ['sg50', 'sg100', 'cbow50', 'cbow100', 'glove50', 'glove100', 'glove50_min20', 'sg50_min20','cbow50_min20']
# embedding_path = [sg50, sg100, cbow50, cbow100, glove50, glove100, glove50_min20, sg50_min20, cbow50_min20]

gold_tup_file = 'gold/sample_gold.txt'

simpWiki_vocab = '/Volumes/Ed/data/formal/simpwiki_vocab.txt'
enWiki_vocab = '/Volumes/Ed/data/formal/enwiki_vocab.txt'

formal_vocab = ['simpWiki_vocab', 'enWiki_vocab']
formal_vocab_paths = [simpWiki_vocab, enWiki_vocab]

result_dir = 'result'
os.system('mkdir -p %s' % result_dir)

#########################
# settings
#########################
_wiki_index = 0
Formal_vacab = formal_vocab[_wiki_index]
formal_vocab_file = formal_vocab_paths[_wiki_index]

# glove_w5 = '/Volumes/Ed/embedding/w5/tweet_V50000_w5_vectors.txt'
# cbow_w5 = '/Volumes/Ed/embedding/w5/cbow100_win5_v50000.txt'
# sg_w5 = '/Volumes/Ed/embedding/w5/sg100_win5_v50000.txt'
# EXP_ = ['glove_w5', 'cbow_w5', 'sg_w5']
# embedding_path = [glove_w5, cbow_w5, sg_w5]

glove_w5_v10k = '/Volumes/Ed/embedding/w5_v10k/tweet_V10000_w5_vectors.txt'
cbow_w5_v10k = '/Volumes/Ed/embedding/w5_v10k/cbow100_win5_v10000.txt'
sg_w5_v10k = '/Volumes/Ed/embedding/w5_v10k/sg100_win5_v10000.txt'

# EXP_ = ['glove_w5_v10k', 'sg_w5_v10k', 'cbow_w5_v10k']
# embedding_path = [glove_w5_v10k, sg_w5_v10k, cbow_w5_v10k]

glove_w5_min100 ='/Volumes/Ed/embedding/w5_min100/glove/tweet_min100_w5_vectors.txt'
fasttext_w5_min100 ='/Volumes/Ed/embedding/w5_min100/fasttext/fasttext_min100_w5.vec'
sg_w5_min100 ='/Volumes/Ed/embedding/w5_min100/sg/sg100_win5_minCount100.txt'
cbow_w5_min100 ='/Volumes/Ed/embedding/w5_min100/cbow/cbow100_win5_minCount100.txt'
EXP_ = ['glove_w5_min100', 'fasttext_w5_min100','sg_w5_min100', 'cbow_w5_min100']
embedding_path = [glove_w5_min100,fasttext_w5_min100, sg_w5_min100, cbow_w5_min100]


def load_embedding(i, embedding_path):
    embedding_index = dict()
    with open(embedding_path, encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            if word.isdigit(): continue
            if word.startswith('@') or word.startswith('#') or word.startswith('http'):
                continue
            vector = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = vector
    print("Load %s %s word vectors from pretrained file" % (len(embedding_index), EXP_[i]))
    vocab = list(embedding_index.keys())
    return embedding_index, vocab


def filter_variant_tuple(tup_file, formal_vocab, informal_vocab):
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
    return list(set(variants))


def evaluate_pair(tup, word_vectors, _embedding, informal_vocab, N=1000):
    # TODO: calculate the embedding cosine distance and return whether the rank of current exrtacted variant
    word = tup[0]
    variant = tup[1]
    var_vec = _embedding[word]
    # 1. embedding dict values to np matrix
    # print(word_vectors.shape)
    dst = np.dot(word_vectors, var_vec.T) / np.linalg.norm(word_vectors, axis=1) / np.linalg.norm(var_vec)
    word_ids = np.argsort(-dst)[1:N + 1]
    # 2. calculate cosine similarity
    # 3. argsort
    # 4. find rank
    topN = [(informal_vocab[i], dst[i]) for i in word_ids]
    topN_words = [r[0] for r in topN]
    rank = -1
    if variant in topN_words:
        rank = topN_words.index(variant)
        print(topN_words[:20])
        # print(tup, rank)
    return rank


def evaluate_all_pairs(i):
    correct_cnt = 0
    top20_cnt = 0
    top50_cnt = 0
    top100_cnt = 0
    error_cnt = 0
    # ranks = []
    # result_all = os.path.join(result_dir, 'results.txt')
    result_all = 'results.txt'
    exp_dir = os.path.join(result_dir, EXP_[i])
    os.system('mkdir -p %s' % exp_dir)
    top1_file = os.path.join(exp_dir, 'top1.txt')
    top20_file = os.path.join(exp_dir, 'top20.txt')
    top50_file = os.path.join(exp_dir, 'top50.txt')
    top100_file = os.path.join(exp_dir, 'top100.txt')
    f_top1 = open(top1_file, 'w')
    f_top20 = open(top20_file, 'w')
    f_top50 = open(top50_file, 'w')
    f_top100 = open(top100_file, 'w')

    print('*' * 80 + '\n' + 'Starting to evaluate %s ...' % EXP_[i])
    _embedding, informal_vocab = load_embedding(i, embedding_path[i])

    with open(formal_vocab_file) as formal_vocab_f:
        formal_vocab = set([line.split()[0] for line in formal_vocab_f])
    word_vectors = np.array([v for v in _embedding.values()])

    variants = filter_variant_tuple(gold_tup_file, formal_vocab, informal_vocab)
    print("%i evaluation pairs" % len(variants))
    # file = 'selected_pair/%s_pair.csv' % EXP_[i]
    # d = [(w, v, _embedding[w], _embedding[v]) for w,v in variants]
    # df = pd.DataFrame.from_records(d, columns=['w','v', 'w_vec', 'v_vec'])
    # df.to_csv(file)
    # return 0
    for tup in variants:
        try:
            rank = evaluate_pair(tup, word_vectors, _embedding, informal_vocab, N=1000)
            if rank == -1:
                continue
            if 0 <= int(rank) < 100:
                top100_cnt += 1
                print("-" * 80 + "\n" + "{}th top 100:".format(top100_cnt), tup, rank)
                print("{}\t{}".format(tup, rank), file=f_top100)
            if 0 <= int(rank) < 50:
                top50_cnt += 1
                print("{}th top 50:".format(top50_cnt), tup, rank)
                print("{}\t{}".format(tup, rank), file=f_top50)
            if 0 <= int(rank) < 20:
                top20_cnt += 1
                print("{}th top 20:".format(top20_cnt), tup, rank)
                print("{}\t{}".format(tup, rank), file=f_top20)
            if int(rank) == 0:
                print("{}th top 1:".format(correct_cnt), tup, rank)
                print("{}\t{}".format(tup, rank), file=f_top1)
                correct_cnt += 1

        except Exception as e:
            error_cnt += 1
            print("Error:", e, tup)
            continue
    f_top1.close()
    f_top20.close()
    f_top50.close()
    f_top100.close()
    # print(ranks)
    print("%i pairs error" % error_cnt)
    print("%i pairs correct" % correct_cnt)
    print("%i pairs in top 20" % top20_cnt)
    print("%i pairs in top 50" % top50_cnt)
    print("%i pairs in top 100" % top100_cnt)
    with open(result_all, 'a') as f:
        f.write('%s, vocab size: %s, formal vacab: %s, tuple num: %s, correct: %s, top20: %s, top50: %s, top100:%s\n' % (
            EXP_[i], len(_embedding), Formal_vacab, len(variants), correct_cnt, top20_cnt, top50_cnt, top100_cnt))


if __name__ == '__main__':
    for i in range(len(EXP_)):
        evaluate_all_pairs(i)
    # evaluate_all_pairs(-1)
