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

embedding_name = 'glove'

print('Indexing %s word vectors.' % embedding_name)
# 1. load pretrained embedding
embeddings_index = load_pretrained_model(glove_path)
print('Found %s word vectors.' % len(embeddings_index))

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
num_words = min(MAX_NUM_WORDS, len(word_index)+1)
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# subdir to save history
subdir = 'CNN_%s' % embedding_name


# load pre-trained word embeddings into an Embedding layer
# note that we set trainable = False so as to keep the embeddings fixed
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

print('Training model.')

# train a 1D convnet with global maxpooling
sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
x = Conv1D(128, 5, activation='relu')(embedded_sequences)
x = MaxPooling1D(5)(x)
x = Conv1D(128, 5, activation='relu')(x)
x = MaxPooling1D(5)(x)
x = Conv1D(128, 5, activation='relu')(x)
x = GlobalMaxPooling1D()(x)
x = Dense(128, activation='relu')(x)
preds = Dense(5, activation='softmax')(x)

model = Model(sequence_input, preds)
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])

history  = model.fit(train_pad_seq, y_train,
          batch_size=128,
          epochs=10,
          validation_data=(val_pad_seq, y_val))

# save history info
plot_filename = 'glove_cnn.pdf'
save_history(history, '{}.csv'.format(plot_filename[:-4]), subdir=subdir)
# save model
visialize_model(model, filepath=plot_filename)
# save single history
plot_fit(history, plot_filename=plot_filename)

