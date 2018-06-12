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

@file: BootstrapIE.py

@time: 11/06/2018 20:50 

@desc：       
               
'''              
from .baseline import Basic


class BootstrapIE(Basic):
    def __init__(self, chunksize):
        super(BootstrapIE, self).__init__(self.load_sql, chunksize=chunksize)
        self.patterns = list()
        self.seeds = list()
        self.candidate_seeds = list()

    @property
    def load_sql(self):
        db_name = 'UrbanDict'
        sql_loadUD = "SELECT defid, word, definition FROM %s" % db_name
        return sql_loadUD


