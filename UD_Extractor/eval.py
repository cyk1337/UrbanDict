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

def conn_db():
    engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
    conn = engine.connect()
    return conn

def get_defns_from_defids(defid):
    pd.options.display.max_colwidth = 10000
    conn = conn_db()
    db_name = 'UrbanDict'
    sql_loadUD = "SELECT label, defid, definition FROM %s WHERE defid = %s" % (db_name, defid)
    df = pd.read_sql(sql=sql_loadUD, con=conn)
    # defns = df.to_string(header=False, index=False)
    return df


def sample2Estimate_prec(_dir):
    bt_dir = os.path.join('iter_result', _dir)
    for iter_dir in os.listdir(bt_dir):
        if not iter_dir.startswith('Iter'): continue
        filename = os.path.join(bt_dir, iter_dir, 'candi_tup.pkl')
        with open(filename, 'rb') as f:
            tup_list = pickle.load(f)
        tup_sample = random.sample(tup_list, 100)
        sample_dir = os.path.join(bt_dir, '%ssample100' % _dir)
        if not os.path.exists(sample_dir):
            os.mkdir(sample_dir)
        file = os.path.join(sample_dir, '%ssample100.txt' % iter_dir)
        # records = []
        df = pd.DataFrame()
        for tup in tup_sample:
            pair = '%s, %s' % (tup.word, tup.variant)
            # defids = '('+','.join([str(id) for id in set(tup.defid_list)])+')'
            for defid in set(tup.defid_list):
                defn = get_defns_from_defids(defid)
                defn.insert(loc=1, column='pair', value=pair)
                df = df.append(defn)

        # df = pd.DataFrame.from_records(records)
        df.to_csv(file, header=True, index=False, sep="\t", escapechar='\\',doublequote=False)
        print("Finish writing into %s" % file)

def update_label_db(defid_list, label, sample_file):
    conn = conn = conn_db()
    len_ = len(defid_list)
    if len_ > 1:
        sql_update = "UPDATE UrbanDict SET label = %s WHERE defid in %s" % (label, defid_list)
    elif len_ == 1:
        sql_update = "UPDATE UrbanDict SET label = %s WHERE defid = %s" % (label, defid_list[0])
    try:
        conn.execute(sql_update)
        print("Update label %s complete!" % label)
    except Exception as e:
        print("Fail to update label: %s, %s" % (sample_file[-18:-13],e))

def update_variant_db(defid, variant, sample_file):
    conn = conn_db()
    sql_update = "UPDATE UrbanDict SET variant ='"+variant+"' WHERE defid = "+ str(defid)
    try:
        conn.execute(sql_update)
        # print('Finish updating variant: %s' % defid)
    except Exception as e:
        print("Update variant fail: %s: %s" % (sample_file[-18:-13], e))

def _count_and_write_db(sample_file):
    df = pd.read_csv(sample_file, sep="\t")
    # label 1: true defn and correct label
    label_1 = df[df['label']==1]
    # label 1: true defn but wrong label
    label_2 = df[df['label']==2]
    # negative defn
    label_nan = df[df['label'].isna()]
    # prec = label_1['pair'].count()/100
    prec = label_1['pair'].nunique()/100

    # update label in db
    pos_list = tuple(label_1['defid'].tolist())
    neg_list = tuple(label_nan['defid'].tolist())
    if len(pos_list) >0:
        update_label_db(pos_list, 1, sample_file)
        update_label_db(neg_list, 0, sample_file)
        if label_2['defid'].count() > 0:
            label2 = tuple(label_2['defid'].tolist())
            update_label_db(label2, 2, sample_file)
    else:
        print('Please manually label first! %s' % sample_file)

    # update variant in db
    corr = df[df['label'] >= 1]
    if corr['label'].count() > 0:
        variant = corr['pair'].str.split(',', expand=True)[1]
        corr.insert(loc=2, column='variant', value=variant)
        for i, row in corr.iterrows():
            defid = row['defid']
            variant = row['variant']
            update_variant_db(defid, variant, sample_file)

    # write precision into log file
    result_dir = os.path.dirname(os.path.dirname(sample_file))
    log_file = os.path.join(result_dir, 'logs')
    with open(log_file, 'a') as f:
        log_iter = "Iteration %s: prec %s" % (sample_file[-14], prec)
        f.write(log_iter+'\n')
        print(log_iter)

def update_sample_dir(_dir):
    for sample_file in os.listdir(_dir):
        if not sample_file.endswith('.txt'): continue
        _count_and_write_db(sample_file)


if __name__ == '__main__':
    # valid_pair = read_valid_file()
    # from collections import Counter
    # words = Counter(pair[0] for pair in valid_pair)
    # print(words.most_common())

    # test = [('ur', 'your'), ('m8s', 'mates')]
    # # save_iter(1, test, 'test')
    # eval_recall(test)

    # sample2Estimate_prec('RlogF_distinct_t10_p10+')
    # sample2Estimate_prec('RlogF_distinct_ctx3_t10_p10')
    file = 'iter_result/RlogF_distinct_ctx3_t10_p10/RlogF_distinct_ctx3_t10_p10sample100/Iter1sample100.txt'
    _count_and_write_db(file)