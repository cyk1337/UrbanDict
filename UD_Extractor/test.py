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

# class Test:
#     def __init__(self):
#         self.x = 0
#
#
# t = Test()
# print(t.x)
# l = list()
# l.append(t)
# t.x +=1
# print(t.x)
# t.x +=1
# print(l[0].x)

def iterative_levenshtein(s, t):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    rows = len(s) + 1
    cols = len(t) + 1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row - 1][col] + 1,  # deletion
                                 dist[row][col - 1] + 1,  # insertion
                                 dist[row - 1][col - 1] + cost)  # substitution
    # for r in range(rows):
    #     print(dist[r])

    # return dist[row][col]
    return dist[row][col]/(len(s)+len(t))


print(iterative_levenshtein("the", "teh"))