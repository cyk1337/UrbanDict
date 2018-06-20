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

@file: test.py

@time: 28/05/2018 14:22 

@desc: test code
               
'''

import pandas as pd
import sqlalchemy as sa
import re
# engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
# conn = engine.connect()
# db_name = 'UrbanDict2'
# sql_loadUD = "SELECT defid, word, definition FROM %s LIMIT 1000" % db_name
# chunksize = None
# df = pd.read_sql(sql=sql_loadUD, con=conn, chunksize=chunksize)


# for i, chunk in enumerate(df):
#     print(chunk)


# from ie_utils import load_pkl
# d1 = load_pkl('s1.pkl')
# d2 = load_pkl('s2.pkl')
# diff = set(d1.values())^set(d2.values())
# diff2 = set(d1.keys())^set(d2.keys())
# print(diff)

# def pattern_filter(candidate_pattern):
#     non_pat_list = ['synonym', ]
#     for non_pat in non_pat_list:
#         if non_pat in candidate_pattern:
#             return False
#         else:
#             return True
#
# print(pattern_filter(['synonym', 'for']))

class Test:
    def __init__(self):
        self.x = 0


t = Test()
print(t.x)
l = list()
l.append(t)
t.x +=1
print(t.x)
t.x +=1
print(l[0].x)

