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

@file: label_processing.py

@time: 25/06/2018 22:58 

@desc：       
               
'''              
import pandas as pd
import sqlalchemy as sa
from nltk.tokenize import word_tokenize

def conn_db():
    engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
    conn = engine.connect()
    return conn

conn = conn_db()
sql = "SELECT defid, word, variant, definition from UrbanDict WHERE label >=1"
df = pd.read_sql(sql, conn)
for _, row in df.iterrows():
    var = row['variant'].lower()
    defn = row['definition'].lower()
    defid = row['defid']
    toks = word_tokenize(defn)
    records = dict()
    df = pd.DataFrame(columns=['defid', 'variant', 'ctx_def', 'ctx_aft'])
    index_list =[]
    for i, tok in enumerate(toks):
        if tok.strip() == var.strip():
            records['defid'] = defid
            records['variant'] = var
            index_list.append(i)
            if i-5 >=0:
                ctx_def = " ".join(toks[i-5:i])
            else:
                ctx_def = " ".join(toks[:i])
            records['ctx_def'] = ctx_def
            if len(toks)>i+5:
                ctx_aft = " ".join(toks[i:i + 5])
            else:
                ctx_aft = " ".join(toks[i:])
            records['ctx_aft'] = ctx_aft
            # TODO: write data to index table
            df_record = pd.DataFrame.from_dict(records)
            df.append(df_record)
    df.to_sql("var_index", con=conn, if_exists='append')

