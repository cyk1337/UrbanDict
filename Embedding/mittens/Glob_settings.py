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

@file: settings.py.py

@time: 03/07/2018 00:51 

@desc：       
               
'''              
import os

data_dir= '/Volumes/Ed/data'
wiki_dir = os.path.join(data_dir, 'wiki')
tweet_dir = os.path.join(data_dir, 'tweet')

simpwiki_bz = os.path.join(wiki_dir, 'simplewiki-20180701-pages-articles.xml.bz2')
simpwiki_file = os.path.join(wiki_dir, 'simplewiki.txt')

enwiki_bz = os.path.join(wiki_dir, 'enwiki-20180701-pages-articles-multistream.xml.bz2')
enwiki_file = os.path.join(wiki_dir, 'enwiki.txt')

