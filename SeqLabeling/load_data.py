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
from nltk.tokenize import word_tokenize
import nltk


def gen_label(label_index, defn_toks):
    labels = [OUT_SIGN] * len(defn_toks)
    if label_index is not None:
        labels[label_index] = IN_SIGN
    return labels

@timeit
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
    # 2.91 sec
    pos_df['tokens'] = pos_df['definition'].apply(lambda x: word_tokenize(x))
    pos_df['pos_data'] = pos_df.apply(lambda row: [(word, tag, label) for (word, tag), label in
                                      zip(nltk.pos_tag(row['tokens']),gen_label(row['label_index'], row['tokens']))],
                                      axis=1)
    pos_data = pos_df['pos_data'].tolist()

    # ==================================================

    neg_df = pd.read_csv(NEG_DATA, sep='\t')
    # neg_df['tokens_num'] = neg_df["definition"].apply(lambda x: len(word_tokenize(x)))
    # ==================================================
    # neg_df['labels'] = OUT_SIGN * neg_df['tokens_num']
    # neg_df['pos_tags'] =  neg_df["definition"].apply(lambda x: nltk.pos_tag(word_tokenize(x)))
    # neg_df['neg_data'] = neg_df['pos_tags'].apply(lambda x: [(word, tag, OUT_SIGN) for word, tag in x])
    # ==================================================
    neg_df['neg_data'] = neg_df["definition"].apply(lambda x: [(word, tag, OUT_SIGN) for word, tag in nltk.pos_tag(word_tokenize(x))])
    neg_data = neg_df['neg_data'].tolist()
    # ==================================================
    return pos_data, neg_data


if __name__ == '__main__':
    load_data()

