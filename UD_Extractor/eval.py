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

@file: eval.py

@time: 20/06/2018 17:55 

@desc：       
               
'''
from _config import *
import codecs, pickle, os

def read_valid_file():
    valid_pair = []
    with codecs.open(VALID_FILE, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line_ = line.split()
            if len(line_) == 2:
                pair = (line_[0].lower(), line_[1].lower())
                valid_pair.append(pair)
        # print("Initial {} seeds: {}".format(len(valid_pair), valid_pair))

    with open(VAL_pkl, 'wb') as f:
        pickle.dump(valid_pair, f)
    return valid_pair

def eval_recall(_list):

    if not os.path.exists(VAL_pkl):
        valid_tup = read_valid_file()
    else:
        with open(VAL_pkl, 'rb') as f:
            valid_tup = pickle.load(f)
    tp = 0
    for tup in valid_tup:
        if tup in _list:
            tp += 1
    rec = tp/len(valid_tup)
    print("Recall: %s" % rec)
    # print("tp:", tp)
    return rec

def save_iter(iter_num, list_obj, fname, exp_name='Bootstrap'):

    iter_No = os.path.join(iter_dir, exp_name,  'Iter%s' % iter_num)
    filename = os.path.join(iter_No, fname+'.txt')
    pkl_fname = os.path.join(iter_No, fname+'.pkl')
    # if not os.path.exists(iter_No):
    #     os.mkdir(iter_No)
    os.system('mkdir -p %s' % iter_No)

    with open(pkl_fname, 'wb') as f:
        pickle.dump(list_obj, f)

    with open(filename, 'w', encoding='utf-8') as f:
        for tup in list_obj:
            f.write('{}\n'.format(tup))
    print('Finish writing into %s !' % filename)

def load_iter(iter_num , fname, exp_name='Bootstrap'):
    iter_No = os.path.join(iter_dir, exp_name, 'Iter%s' % iter_num)

    assert fname.endswith('.pkl'), "fname needs to be ended with '.pkl' !"
    filename = os.path.join(iter_No, fname)

    if not os.path.exists(iter_No):
        os.mkdir(iter_No)
    with open(filename, 'rb') as f:
        list_obj = pickle.load(f)
    return list_obj


if __name__ == '__main__':
    # valid_pair = read_valid_file()
    # from collections import Counter
    # words = Counter(pair[0] for pair in valid_pair)
    # print(words.most_common())

    test = [('ur', 'your'), ('m8s', 'mates')]
    # save_iter(1, test, 'test')
    eval_recall(test)
