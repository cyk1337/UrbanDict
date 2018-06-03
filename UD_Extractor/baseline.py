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

@file: baseline.py

@time: 28/05/2018 13:18 

@desc：       
               
'''
import pandas as pd
import sqlalchemy as sa
import re

class Basic(object):
    def __init__(self, sql, chunksize=None):
        engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
        self.conn = engine.connect()
        self.UD_data = pd.read_sql(sql=sql, con= self.conn, chunksize=chunksize)
        # UD_data = self.UD_data.to_json(orient='records')



class Baseline(Basic):
    def __init__(self, chunksize):
        super(Baseline, self).__init__(self.load_sql, chunksize=chunksize)


    @property
    def load_sql(self):
        db_name = 'UrbanDict2'
        sql_loadUD = "SELECT defid, word, definition FROM %s" % db_name
        return sql_loadUD

    # RegEx
    def RE_match(self, definition):
        pattern_spelling = re.compile(u"spelling[^\.,]*[ of| for|][^\.,]* ['|\"|\[](?P<Spelling>\w+)['|\"|\]]")
        m = re.search(pattern_spelling, definition)
        if m is not None:
            spelling_variant = m.group('Spelling')
            print('Extracted spelling variant:{}'.format(spelling_variant))
            return spelling_variant


if __name__ == "__main__":
    chunksize = 10000
    baseline = Baseline(chunksize=chunksize)
    target_list = []
    for i, chunk in enumerate(baseline.UD_data):
        # if i>100: break
        # print(chunk)
        for defn in chunk['definition'].values:
            spelling_variant = baseline.RE_match(defn)
            if spelling_variant:
                row = chunk.loc[chunk['definition']==defn]
                defid = row['defid']
                word = row['word']
                target_tuple = (word, spelling_variant, defid)
                target_list.append(target_tuple)
                print(target_tuple)
