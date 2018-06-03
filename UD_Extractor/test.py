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


