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
# from nltk.tokenize import word_tokenize
import spacy

from SL_config import *

def conn_db():
    engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
    conn = engine.connect()
    return conn

conn = conn_db()
sql = "SELECT defid, word, variant, definition from UrbanDict WHERE label >=1"
df = pd.read_sql(sql, conn)

rows_ = []

# TODO: after manually label, donot change table `var_index` anymore!
# ====================================
# nlp = spacy.load('en')
#
# for _, row in df.iterrows():
#     var = row['variant'].lower()
#     defn = row['definition'].lower()
#     defid = row['defid']
#     doc = nlp(defn, disable=['tagger','parser','ner','textcat'])
#     toks =[w.text for w in doc]
#
#
#     index_list =[]
#     for i, tok in enumerate(toks):
#         if tok.strip() == var.strip():
#             records = dict()
#             records['label_index'] = i
#             records['defid'] = defid
#
#             records['variant'] = var
#             index_list.append(i)
#             if i-5 >=0:
#                 ctx_def = " ".join(toks[i-5:i])
#             else:
#                 ctx_def = " ".join(toks[:i])
#             records['ctx_bef'] = ctx_def
#             if len(toks)>i+6:
#                 ctx_aft = " ".join(toks[i+1:i + 6])
#             else:
#                 ctx_aft = " ".join(toks[i+1:])
#             records['ctx_aft'] = ctx_aft
#             records['defn'] = defn
#             rows_.append(records)
# # df2 = pd.DataFrame(rows_)
# df2 = pd.DataFrame(rows_, columns=['defid', 'label_index', 'variant','ctx_bef', 'ctx_aft', 'defn'])
# df2.drop_duplicates(inplace=True)
# try:
#     df2.to_sql("var_index", con=conn, if_exists='replace', index=False)
# except Exception as e:
#     print(e)
# ====================================

# generate positive data
gen_pos_sql = """SELECT a.defid, a.word,b.variant,b.label_index, a.definition 
            FROM UrbanDict as a 
            JOIN var_index as b ON a.defid = b.defid 
            WHERE a.label >=0 and b.label_index not in ('','-1','-2','-3','-4','-5','-6','-7','-8','-9','-10')
"""
pos_data = pd.read_sql(gen_pos_sql, con=conn)
pos_data.to_csv(POS_DATA, sep='\t', index=False)
print("Positive data generated!")

# generate negative data
gen_neg_sql = "SELECT defid, word, definition FROM UrbanDict WHERE label=0"
neg_data = pd.read_sql(gen_neg_sql, con=conn)
neg_data.to_csv(NEG_DATA, sep='\t', index=False)
print("Negative data generated!")

# generate unlabeled data
gen_unlbl_sql = "SELECT defid, word, definition FROM UrbanDict WHERE label IS NULL and LENGTH(definition)!=0"
gen_unlbl_sql = pd.read_sql(gen_unlbl_sql, con=conn)
gen_unlbl_sql.to_csv(UNLABEL_DATA, sep='\t', index=False)
print("Unlabeled data generated!")
# run directly to generate csv file!