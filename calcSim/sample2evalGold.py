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

@file: sample2evalGold.py

@time: 04/07/2018 19:05 

@desc：       
               
'''
import pandas as pd
import os
import sqlalchemy as sa


# silver_file = '/Users/yekun/Documents/CODE_/UrbanDict/SeqLabeling/data/silver/CRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx4_conf0.9/0pos.csv'
#
# gold_samp_df = pd.read_csv(silver_file, sep='\t')
#
# sample_df = gold_samp_df.sample(1500)
#
# sample_df.to_csv('sample1500', sep='\t', index=False, header=False)

def sample4handcheck(sample_file):
    filename = '/Users/yekun/Documents/CODE_/UrbanDict/SeqLabeling/SL_result/CRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx4_conf0.9/Iteration0.txt'
    shuf_cmd = "gshuf -n 1500 %s | gsed 's/^/\t/' > %s" % (filename, sample_file)
    os.system(shuf_cmd)


sample_file = 'sample1.5K'


# sample4handcheck(sample_file)

#
def gen_goldTuple():
    f = open('GoldTuple.txt', 'w')
    with open(sample_file) as sample_f:
        for line in sample_f.readlines():
            fields = line.split('\t')
            if fields[0] != '0':
                variants = fields[3].split()
                if len(variants) >= 1:
                    for v in variants:
                        f.write('{}\t{}\n'.format(fields[2].lower(), v.lower()))

    f.close()


# gen_goldTuple()

def fetch_gold_from_db():
    engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
    conn = engine.connect()

    sql = "SELECT defid, word, variant, definition from UrbanDict WHERE label >=1"
    df = pd.read_sql(sql, conn)
    df.to_csv('db_gold', sep='\t', index=False)

    f=open('db_gold.txt', 'w')
    for i, row in df.iterrows():
        variants = row['variant'].split()
        if len(variants)>0:
            for v in variants:
                f.write('{}\t{}\n'.format(row['word'].lower(), v.lower()))
    f.close()

fetch_gold_from_db()
