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

@file: trainW2V.py

@time: 02/07/2018 23:20 

@desc：       
               
'''
import os, multiprocessing
from gensim.models.word2vec import Word2Vec, LineSentence

w2v_dir = os.path.dirname(os.path.abspath(__file__))


data_dir = '/Volumes/Ed/data/tweet'
data_file = os.path.join(data_dir, 'en_2G')


# def data_generator(data_file):
#     with open(data_file) as f:
#         for line in f.readlines():
#             yield line.split()
import argparse

parser = argparse.ArgumentParser(description='Give max vocab size of w2v: ')
parser.add_argument('--MaxVocab', type=int, default=1000)
args = parser.parse_args()
max_final_vocab= args.MaxVocab
size = 100
window = 5
# min_count=5
# min_count=20

sg_file = os.path.join(w2v_dir, 'sg%s_win%s_v%s' % (size, window, max_final_vocab))

cbow_file = os.path.join(w2v_dir, 'cbow%s_win%s_v%s' % (size, window, max_final_vocab))

print('Training w2v, win %s, vector size %s, max vocab size %s' % (window, size, max_final_vocab))

def train_sg():
    sg_model = Word2Vec(sentences=LineSentence(data_file), size=size, window=window, max_final_vocab=max_final_vocab, sg=1, workers=max(1, multiprocessing.cpu_count() - 1))

    sg_model.save(sg_file+'.model')
    sg_model.wv.save_word2vec_format(sg_file+'.txt')


def train_cbow():
    cbow_model = Word2Vec(sentences=LineSentence(data_file), size=size, window=window, max_final_vocab=max_final_vocab, sg=0, workers=max(1, multiprocessing.cpu_count() - 1))

    cbow_model.save(cbow_file + '.model')
    cbow_model.wv.save_word2vec_format(cbow_file+'.txt')

if __name__ == '__main__':
    train_cbow()
    train_sg()

    # wv = Word2Vec.load(cbow_file + '.model')
    # x = wv.most_similar('queen')
    # print(x)