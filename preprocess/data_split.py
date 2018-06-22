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

@file: data_split.py

@time: 22/06/2018 17:36 

@desc：       
               
'''              
import codecs,pickle, os
import pandas as pd

with codecs.open('stat_hashtag30.pkl', 'rb') as f:
    hashtag_N = pickle.load(f)

tags = [t[0] for t in hashtag_N[:5]]

# print(tags)
data_records = []
# t=tags[0]
for i,t in enumerate(tags):
    filename = os.path.join('hashtag', t)
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f:
            toks = line.split()
            if len(toks)<6:
                continue
            elif toks[-1][1:].strip() != t:
                print(toks[-1], t)
                continue
            data_records.append((" ".join(toks[:-1]),toks[-1][1:], i))

df = pd.DataFrame.from_records(data_records, columns=['tweets', 'hashtag', 'label'])
shuffle_data = df.sample(frac=1, random_state=2018)


work_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(work_dir, 'Hashtag prediction', 'data')
train_csv = os.path.join(data_dir, "train.csv")
val_csv = os.path.join(data_dir, "val.csv")
test_csv = os.path.join(data_dir, "test.csv")

split_bound = [0.70, 0.15, 0.15]

# split
RECORDS_NUM = len(shuffle_data)
train_bound = int(split_bound[0] * RECORDS_NUM)
val_bound = int((split_bound[0] + split_bound[1]) * RECORDS_NUM)
train_data = shuffle_data.iloc[:train_bound, :]
val_data = shuffle_data.iloc[train_bound:val_bound, :]
test_data = shuffle_data.iloc[val_bound:, :]

if not os.path.exists(data_dir):
    os.mkdir(data_dir)
if not os.path.exists(train_csv):
    print('Generating {}...'.format(train_csv))
    train_data.to_csv(train_csv, index=False, encoding='utf-8')
    print('Finished', '-' * 80)
if not os.path.exists(val_csv):
    print('Generating {}...'.format(val_csv))
    val_data.to_csv(val_csv, index=False, encoding='utf-8')
    print('Finished', '-' * 80)
if not os.path.exists(test_csv):
    print('Generating {}...'.format(test_csv))
    test_data.to_csv(test_csv, index=False, encoding='utf-8')
    print('Finished', '-' * 80)
else:
    print('%s, %s , %s already exists!' % (train_csv, val_csv, test_csv))