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
    labels_list = label_index.split()

    labels = [OUT_SIGN] * len(defn_toks)

    try:
        for label in labels_list:
            label = int(label)
            labels[label] = IN_SIGN
    except Exception as e:
        print(e)
        print("tokens:", defn_toks)
        print("label_index", label_index)
    return labels


# @timeit
def load_data(load_silver_iter):
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

    nlp = spacy.load('en')
    pos_data = []
    for i, row in pos_df.iterrows():
        label_index = row['label_index']
        defn = row['definition'].lower()
        doc = nlp(defn, disable=['ner', 'textcat'])
        defn_toks = [w.text for w in doc]

        labels = gen_label(label_index, defn_toks)
        line = [(w, label) for w, label in zip(doc, labels)]
        pos_data.append(line)

    silver_pos_data = []
    if load_silver_iter > 0:
        ITER_NUM = load_silver_iter
        SILVER_POS_DATA = os.path.join(silver_dir, CRF_MODEL, '{}pos.csv'.format(ITER_NUM - 1))
        print("start loading silver data: %s" % SILVER_POS_DATA)
        silver_pos_df = pd.read_csv(SILVER_POS_DATA, sep='\t')
        for _, row in silver_pos_df.iterrows():
            label_index = row['label_index']
            defn = row["definition"]
            defn = defn.lower()
            doc = nlp(defn, disable=['ner', 'textcat'])
            defn_toks = [w.text for w in doc]
            labels = gen_label(label_index, defn_toks)
            line = [(w, label) for w, label in zip(doc, labels)]
            silver_pos_data.append(line)
    pos_data.extend(silver_pos_data)

    neg_data = []
    for i, row in neg_df.iterrows():
        defn = row['definition'].lower()
        doc = nlp(defn, disable=['ner', 'textcat'])
        line = [(w, OUT_SIGN) for w in doc]
        neg_data.append(line)

    return pos_data, neg_data


# @timeit
def load_unlabel_data():
    if TEST_MODE is True:
        print("Start test mode:\n" + '*' * 80)
        unlabel_df = pd.read_csv(UNLABEL_DATA, sep='\t', chunksize=1000, nrows=10000)
    else:
        unlabel_df = pd.read_csv(UNLABEL_DATA, sep='\t', chunksize=10000)

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

    nlp = spacy.load('en')
    for _, chunk in enumerate(unlabel_df):
        unlabel_data = []
        for i, row in chunk.iterrows():
            definition = row['definition']
            if type(definition) is not str:
                with open(ERR_LOG, 'a') as f:
                    f.write(str(row))
                print("!" * 80 + "\n" + str(row))
                definition = str(definition)
            defn = definition.lower()
            doc = nlp(defn, disable=['ner', 'textcat'])
            line = [(w,) for w in doc]
            unlabel_data.append(line)
        unlabel_defids = chunk['defid'].tolist()
        unlabel_word = chunk['word'].tolist()
        unlabel_defn = chunk['definition'].tolist()

        yield unlabel_data, unlabel_defids, unlabel_word, unlabel_defn


if __name__ == '__main__':
    # load_data()

    # gen_unlabeled_data()
    load_unlabel_data()
