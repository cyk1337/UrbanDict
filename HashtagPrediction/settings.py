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

@file: settings.py

@time: 22/06/2018 18:53 

@desc：       
               
'''
import os

work_dir = os.path.dirname(os.path.abspath(__file__))
# csv raw docs
data_file = os.path.join(work_dir, 'csv')
train_csv = os.path.join(data_file, 'train.csv')
val_csv = os.path.join(data_file, 'val.csv')
test_csv = os.path.join(data_file, 'test.csv')

# embedding
embedding_dir = os.path.join(work_dir, 'embedding')
glove_path = os.path.join(embedding_dir, 'glove50', 'vectors.txt')


# results
result_dir = os.path.join(work_dir, 'result')
plot_dir = os.path.join(result_dir, 'plot')
log_dir = os.path.join(result_dir, 'logs')
model_dir = os.path.join(result_dir, 'model')
history_dir = os.path.join(result_dir, 'history')

EMBEDDING_DIM = 50

MAX_NUM_WORDS = 20000
MAX_SEQUENCE_LENGTH = 200

# hyper-params
EPOCH_NUM = 15
BATCH_SIZE = 128
