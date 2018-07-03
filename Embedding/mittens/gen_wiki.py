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

@file: gen_wiki.py

@time: 03/07/2018 21:05 

@desc：       
               
'''              
from __future__ import print_function
import logging

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Glob_settings import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

from gensim.corpora import WikiCorpus

# wiki_bz = simpwiki_bz
# wiki_file = simpwiki_file
wiki_bz = enwiki_bz
wiki_file = enwiki_file

wiki = WikiCorpus(wiki_bz, lemmatize=False, dictionary={})

f = open(wiki_file, 'w')
print('Writing to %s' % wiki_file)
for i, text in enumerate(wiki.get_texts()):
    f.write(' '.join(text) + '\n')
    if (i % 10000 == 0):
        logger.info("Saved " + str(i) + " articles")

f.close()