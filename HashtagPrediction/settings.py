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
data_file = os.path.join(work_dir, 'csv_10')
train_csv = os.path.join(data_file, 'train.csv')
val_csv = os.path.join(data_file, 'val.csv')
test_csv = os.path.join(data_file, 'test.csv')

# embedding
embedding_dir = os.path.join(work_dir, 'embedding')
# glove50 = '/Volumes/Ed/embedding/glove50/vectors.txt'
# glove100 = '/Volumes/Ed/embedding/glove100/vectors.txt'

#
#
# cbow50 = '/Volumes/Ed/embedding/w2v50/cbow/cbow50_win5_min5.txt'
# cbow100 = '/Volumes/Ed/embedding/w2v100/cbow/cbow100_win5_min5.txt'

# sg50 = '/Volumes/Ed/embedding/w2v50/sg/sg50_win5_min5.txt'
# sg100 = '/Volumes/Ed/embedding/w2v100/sg/sg100_win5_min5.txt'

glove_w5 = '/Volumes/Ed/embedding/w5/tweet_V50000_w5_vectors.txt'
cbow_w5 = '/Volumes/Ed/embedding/w5/cbow100_win5_v50000.txt'
sg_w5 = '/Volumes/Ed/embedding/w5/sg100_win5_v50000.txt'

# results
result_dir = os.path.join(work_dir, 'result')
plot_dir = os.path.join(result_dir, 'plot')
log_dir = os.path.join(result_dir, 'logs')
model_dir = os.path.join(result_dir, 'model')
history_dir = os.path.join(result_dir, 'history')



MAX_NUM_WORDS = 20000
MAX_SEQUENCE_LENGTH = 200

# hyper-params
EPOCH_NUM = 15
BATCH_SIZE = 128
