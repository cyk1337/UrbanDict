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

@file: load_data.py

@time: 26/06/2018 16:09 

@desc：       
               
'''              
from SL_config import *

import pandas as pd
import sqlalchemy as sa
from nltk.tokenize import word_tokenize
import nltk
import spacy


def gen_label(label_index, defn_toks):
    labels = [OUT_SIGN] * len(defn_toks)
    if label_index is not None:
        labels[label_index] = IN_SIGN
    return labels

# @timeit
def load_data():
    pos_df = pd.read_csv(POS_DATA, sep='\t')
    # ==================================================
    # 2.93 sec
    # pos_data = []
    # for i, row in pos_df.iterrows():
    #     label_index = row['label_index']
    #     defn = row['definition']
    #     tok_defn = word_tokenize(defn)
    #     labels = gen_label(label_index, defn)
    #     pos_tags = nltk.pos_tag(tok_defn)
    #     line = [(word, tag, label) for (word,tag), label in zip(pos_tags, labels)]
    #     pos_data.append(line)
    # ==================================================

    # ==================================================

    neg_df = pd.read_csv(NEG_DATA, sep='\t')
    # neg_df['tokens_num'] = neg_df["definition"].apply(lambda x: len(word_tokenize(x)))
    # ==================================================
    # neg_df['labels'] = OUT_SIGN * neg_df['tokens_num']
    # neg_df['pos_tags'] =  neg_df["definition"].apply(lambda x: nltk.pos_tag(word_tokenize(x)))
    # neg_df['neg_data'] = neg_df['pos_tags'].apply(lambda x: [(word, tag, OUT_SIGN) for word, tag in x])
    # ==================================================
    # 2.91 sec
    # if USE_NLTK is True:
    pos_df['tokens'] = pos_df['definition'].apply(lambda x: word_tokenize(x))
    pos_df['pos_data'] = pos_df.apply(lambda row: [(word, tag, label) for (word, tag), label in
                        zip(nltk.pos_tag(row['tokens']), gen_label(row['label_index'], row['tokens']))],
                        axis=1)

    neg_df['neg_data'] = neg_df["definition"].apply(lambda x: [(word, tag, OUT_SIGN) for word, tag in nltk.pos_tag(word_tokenize(x))])
    pos_data = pos_df['pos_data'].tolist()
    neg_data = neg_df['neg_data'].tolist()
    return pos_data, neg_data

    # elif USE_SPACY is True:
    #     nlp = spacy.load('en')
    #     pos_data = []
    #     for i, row in pos_df.iterrows():
    #         label_index = row['label_index']
    #         defn = row['definition']
    #         doc = nlp(defn, disable=['ner','textcat'])
    #         labels = gen_label(label_index, defn)
    #         line = [(w, label) for w, label in zip(doc, labels)]
    #         pos_data.append(line)
    #     neg_data = []
    #     for i, row in neg_df.iterrows():
    #         defn = row['definition']
    #         doc = nlp(defn, disable=['ner','textcat'])
    #         line = [(w, OUT_SIGN) for w in doc]
    #         neg_data.append(line)
    #     return pos_data, neg_data


# @timeit
def load_unlabel_data():
    unlabel_df = pd.read_csv(UNLABEL_DATA, sep='\t', chunksize=10000)
    # unlabel_df = pd.read_csv(UNLABEL_DATA, sep='\t', chunksize=10000, nrows=100000)
    # neg_df['tokens_num'] = neg_df["definition"].apply(lambda x: len(word_tokenize(x)))
    # ==================================================
    # neg_df['labels'] = OUT_SIGN * neg_df['tokens_num']
    # neg_df['pos_tags'] =  neg_df["definition"].apply(lambda x: nltk.pos_tag(word_tokenize(x)))
    # neg_df['neg_data'] = neg_df['pos_tags'].apply(lambda x: [(word, tag, OUT_SIGN) for word, tag in x])
    # ==================================================

    # unlabel_data = []
    # # unlabel_df['unlabel_data'].tolist()
    # unlabel_defids = []
    # # unlabel_df.tolist()
    # unlabel_word = []
    #
    # for _, row in unlabel_df.iterrows():
    #     try:
    #         row_data = nltk.pos_tag(word_tokenize(row["definition"]))
    #         unlabel_data.append(row_data)
    #     except Exception as e:
    #         print('%s, %s' % (e, row))
    #     unlabel_defids.append(row['defid'])
    #     unlabel_word.append(row['word'])
    # # ==================================================

    #
    for _, chunk in enumerate(unlabel_df):
        # if USE_NLTK is True:
        try:
            chunk['unlabel_data'] = chunk["definition"].apply(
            lambda x: [(word, tag) for word, tag in nltk.pos_tag(word_tokenize(x))])
            unlabel_data = chunk['unlabel_data'].tolist()
        except Exception as e:
            print("Error:", e, chunk)
            continue
        # elif USE_SPACY is True:
        #     # TODO
        #     pass

        unlabel_defids = chunk['defid'].tolist()
        unlabel_word = chunk['word'].tolist()

        yield unlabel_data, unlabel_defids, unlabel_word


if __name__ == '__main__':
    # load_data()

    # gen_unlabeled_data()
    load_unlabel_data()