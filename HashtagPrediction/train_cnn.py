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

@file: train_cnn.py

@time: 23/06/2018 13:21

@desc：

'''
# !/usr/bin/env python

# encoding: utf-8


from settings import *

import numpy as np

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Dropout, Embedding, Conv1D, MaxPooling1D, Activation, Flatten, Reshape
from keras.utils.np_utils import to_categorical

from data_loader import load_tweets, load_pretrained_model
from plot_fit import plot_fit, visialize_model, save_history, plot_all_history
import os

# embedding_name = ['glove50', 'sg50','cbow50', 'glove100','sg100', 'cbow100']
# embedding_path = [glove50, sg50, cbow50, glove100, sg100, cbow100]

# embedding_name = ['glove_w5', 'sg_w5', 'cbow_w5']
# embedding_path = [glove_w5, sg_w5, cbow_w5]

# v10k
# embedding_name = ['glove_w5_v10k', 'sg_w5_v10k', 'cbow_w5_v10k']
# embedding_path = [glove_w5_v10k, sg_w5_v10k, cbow_w5_v10k]

dname = './min200'

glove100_w5_min200 = os.path.join(dname, 'glove', 'glove100_min200_w5_vectors.txt')
glove200_w5_min200 = os.path.join(dname, 'glove', 'glove200_min200_w5_vectors.txt')
glove100_w10_min200 = os.path.join(dname, 'glove', 'glove100_min200_w10_vectors.txt')
glove200_w10_min200 = os.path.join(dname, 'glove', 'glove200_min200_w10_vectors.txt')
glove100_w15_min200 = os.path.join(dname, 'glove', 'glove100_min200_w15_vectors.txt')
glove200_w15_min200 = os.path.join(dname, 'glove', 'glove200_min200_w15_vectors.txt')

sg100_w5_min200 = os.path.join(dname, 'w2v', 'sg100_win5_minCount200.txt')
sg200_w5_min200 = os.path.join(dname, 'w2v', 'sg200_win5_minCount200.txt')
sg100_w10_min200 = os.path.join(dname, 'w2v', 'sg100_win10_minCount200.txt')
sg200_w10_min200 = os.path.join(dname, 'w2v', 'sg200_win10_minCount200.txt')
sg100_w15_min200 = os.path.join(dname, 'w2v', 'sg100_win15_minCount200.txt')
sg200_w15_min200 = os.path.join(dname, 'w2v', 'sg200_win15_minCount200.txt')

cbow100_w5_min200 = os.path.join(dname, 'w2v', 'cbow100_win5_minCount200.txt')
cbow200_w5_min200 = os.path.join(dname, 'w2v', 'cbow200_win5_minCount200.txt')
cbow100_w10_min200 = os.path.join(dname, 'w2v', 'cbow100_win10_minCount200.txt')
cbow200_w10_min200 = os.path.join(dname, 'w2v', 'cbow200_win10_minCount200.txt')
cbow100_15_min200 = os.path.join(dname, 'w2v', 'cbow100_win15_minCount200.txt')
cbow200_15_min200 = os.path.join(dname, 'w2v', 'cbow200_win15_minCount200.txt')

ft100_w5_min200 = os.path.join(dname, 'fasttext', 'ft100_win5_minCount200.vec')
ft200_w5_min200 = os.path.join(dname, 'fasttext', 'ft200_win5_minCount200.vec')
ft100_w10_min200 = os.path.join(dname, 'fasttext', 'ft100_win10_minCount200.vec')
ft200_w10_min200 = os.path.join(dname, 'fasttext', 'ft200_win10_minCount200.vec')
ft100_w15_min200 = os.path.join(dname, 'fasttext', 'ft100_win15_minCount200.vec')
ft200_w15_min200 = os.path.join(dname, 'fasttext', 'ft200_win15_minCount200.vec')

# final
embedding_name1 = ['glove100_w5_min200', 'glove200_w5_min200', 'glove100_w10_min200', 'glove200_w10_min200',
                   'glove100_w15_min200', 'glove200_w15_min200']
embedding_path1 = [glove100_w5_min200, glove200_w5_min200, glove100_w10_min200, glove200_w10_min200,
                   glove100_w15_min200, glove200_w15_min200]

embedding_name2 = ['sg100_w5_min200', 'sg200_w5_min200', 'sg100_w10_min200', 'sg200_w10_min200', 'sg100_w15_min200',
                   'sg200_w15_min200']
embedding_path2 = [sg100_w5_min200, sg200_w5_min200, sg100_w10_min200, sg200_w10_min200, sg100_w15_min200,
                   sg200_w15_min200]

# embedding_name2= ['sg100_w15_min200', 'sg200_w15_min200']
# embedding_path2 = [sg100_w15_min200, sg200_w15_min200]

embedding_name3 = ['cbow100_w5_min200', 'cbow200_w5_min200', 'cbow100_w10_min200', 'cbow200_w10_min200',
                   'cbow100_15_min200', 'cbow200_15_min200']
embedding_path3 = [cbow100_w5_min200,cbow200_w5_min200, cbow100_w10_min200, cbow200_w10_min200,cbow100_15_min200, cbow200_15_min200]


embedding_name4 = ['ft100_w5_min200', 'ft200_w5_min200', 'ft100_w10_min200', 'ft200_w10_min200',
                   'ft100_15_min200', 'ft200_15_min200']
embedding_path4 = [ft100_w5_min200,ft200_w5_min200, ft100_w10_min200, ft200_w10_min200, ft100_w15_min200, ft200_w15_min200]



label_num = 10

import argparse

parser = argparse.ArgumentParser(description='Select the embedding index: ')
parser.add_argument('--i', type=int, default=0)
parser.add_argument('--embedding', type=int, default=1)
args = parser.parse_args()
EXP_INDEX = args.i
EXP_embedding = args.embedding
if (EXP_embedding == 1):
    embedding_name = embedding_name1
    embedding_path = embedding_path1
elif (EXP_embedding == 2):
    embedding_name = embedding_name2
    embedding_path = embedding_path2
elif (EXP_embedding == 3):
    embedding_name = embedding_name3
    embedding_path = embedding_path3
elif (EXP_embedding == 4):
    embedding_name = embedding_name4
    embedding_path = embedding_path4
assert EXP_INDEX < len(embedding_name) , 'Embedding out of range!'
print('Indexing %s word vectors.' % embedding_name[EXP_INDEX])
# 1. load pretrained embedding
embeddings_index = load_pretrained_model(embedding_path[EXP_INDEX])
print('Found %s word vectors.' % len(embeddings_index))
EMBEDDING_DIM = len(list(embeddings_index.values())[0])

# load data
print('loading tweets ...')
(X_train, y_train), (X_val, y_val) = load_tweets()

# tokenize, filter punctuation, lowercase
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS, lower=True)
tokenizer.fit_on_texts(X_train)
vocarb_size = len(tokenizer.word_index) + 1
print("%d word types" % len(tokenizer.word_index))

# encoding method 0 : Tokenizer.texts_to_sequence
# ========================
train_seq = tokenizer.texts_to_sequences(X_train)
# print(len(encoded_text))

word_index = tokenizer.word_index

# print('index len:', len(word_index))
train_pad_seq = pad_sequences(sequences=train_seq, maxlen=MAX_SEQUENCE_LENGTH)

# pad val sequence
val_seq = tokenizer.texts_to_sequences(X_val)
val_pad_seq = pad_sequences(sequences=val_seq, maxlen=MAX_SEQUENCE_LENGTH)

y_train = to_categorical(np.asarray(y_train))
y_val = to_categorical(np.asarray(y_val))

print("padding sequnce(X_input) shape:", train_pad_seq.shape)
print("target(y_train) shape:", y_train.shape)
print('-' * 80)

print('Preparing embedding matrix.')
# Embedding matrix
num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# load pre-trained word embeddings into an Embedding layer
# note that we set trainable = False so as to keep the embeddings fixed
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

print('Training model.')
# hyper-params
# filters_list = [64, 128]
# kernel_size_list = [3,4,5]
# maxpooling_size_list = [2,3]

filters_list = [64, 128]
kernel_size_list = [3, 4, 5]
maxpooling_size_list = [2]

for filters in filters_list:
    for kernel_size in kernel_size_list:
        for maxpooling_size in maxpooling_size_list:
            # train a 1D convnet with global maxpooling
            sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
            embedded_sequences = embedding_layer(sequence_input)
            x = embedded_sequences
            # x = Conv1D(filters, kernel_size, activation='relu')(x)
            # x = MaxPooling1D(maxpooling_size)(x)
            x = Conv1D(filters, kernel_size, activation='relu')(x)
            x = GlobalMaxPooling1D()(x)
            # x = Dense(filters, activation='relu')(x)
            preds = Dense(label_num, activation='softmax')(x)

            model = Model(sequence_input, preds)
            model.compile(loss='categorical_crossentropy',
                          optimizer='adam',
                          metrics=['acc'])

            history = model.fit(train_pad_seq, y_train,
                                batch_size=BATCH_SIZE,
                                epochs=EPOCH_NUM,
                                validation_data=(val_pad_seq, y_val))

            # save history info
            EXP_NAME = '%sfilter%s_kernel%s_maxpool%s' % (
            embedding_name[EXP_INDEX], filters, kernel_size, maxpooling_size)
            print("EXP: %s" % EXP_NAME)
            plot_filename = '%s.pdf' % EXP_NAME
            # subdir to save history
            subdir = 'CNN_%s' % embedding_name[EXP_INDEX]
            save_history(history, '{}.csv'.format(plot_filename[:-4]), subdir=subdir)
            # save model
            # visialize_model(model, filepath=plot_filename)
            # save single history
            # plot_fit(history, plot_filename=plot_filename)
