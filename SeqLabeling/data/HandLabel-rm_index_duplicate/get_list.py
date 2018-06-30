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

@file: get_list.py

@time: 29/06/2018 22:49 

@desc：       
               
'''
""" get all the record that occur > 1
SELECT a.defid, a.word,b.variant,b.label_index, a.definition 
FROM UrbanDict as a 
JOIN var_index as b ON a.defid = b.defid 
WHERE a.label >=0 and a.defid in (SELECT defid FROM var_index
GROUP BY defid
HAVING COUNT(defid)>1)

(SELECT defid FROM var_index
GROUP BY defid
HAVING COUNT(defid)>1)

=> write to list! modify in db.
"""


l = list()
with open('index_dup') as f:
    for line in f:
        l.append(line.strip())

print(l)