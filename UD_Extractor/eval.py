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
import random
import pandas as pd
import sqlalchemy as sa

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

def save_iter(iter_num, list_obj, fname, exp_name=EXP_NAME):

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

def load_iter(iter_num , fname, exp_name=EXP_NAME):
    iter_No = os.path.join(iter_dir, exp_name, 'Iter%s' % iter_num)

    assert fname.endswith('.pkl'), "fname needs to be ended with '.pkl' !"
    filename = os.path.join(iter_No, fname)

    with open(filename, 'rb') as f:
        list_obj = pickle.load(f)
    return list_obj


def get_defns_from_defids(defid_list):
    pd.options.display.max_colwidth = 10000
    engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
    conn = engine.connect()
    db_name = 'UrbanDict'
    sql_loadUD = "SELECT defid, definition FROM %s WHERE defid in %s" % (db_name, defid_list)
    df = pd.read_sql(sql=sql_loadUD, con=conn)
    defns = df.to_string(header=False, index=False)
    return defns


def sample2Estimate_prec(_dir):
    bt_dir = os.path.join('iter_result', _dir)
    for iter_dir in os.listdir(bt_dir):
        if not iter_dir.startswith('Iter'): continue
        filename = os.path.join(bt_dir, iter_dir, 'candi_tup.pkl')
        with open(filename, 'rb') as f:
            tup_list = pickle.load(f)
        tup_sample = random.sample(tup_list, 100)
        file = os.path.join(bt_dir, iter_dir, '%ssample100.txt' % iter_dir)
        records = []
        for tup in tup_sample:
            pair = '%s, %s' % (tup.word, tup.variant)
            defids = '('+','.join([str(id) for id in set(tup.defid_list)])+')'

            defn = get_defns_from_defids(defids)
            records.append((None,pair, defn))

        df = pd.DataFrame.from_records(records)
        df.to_csv(file, header=False, index=False, sep="\t", escapechar='\\',doublequote=False)
        print("Finish writing into %s" % file)


if __name__ == '__main__':
    # valid_pair = read_valid_file()
    # from collections import Counter
    # words = Counter(pair[0] for pair in valid_pair)
    # print(words.most_common())

    # test = [('ur', 'your'), ('m8s', 'mates')]
    # # save_iter(1, test, 'test')
    # eval_recall(test)

    sample2Estimate_prec('RlogF_distinct')