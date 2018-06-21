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

@file: generate_hashtag_data.py

@time: 21/06/2018 18:00 

@desc：       
               
'''
import os, re, codecs, pickle
from collections import defaultdict

hashtag_d = defaultdict(list)

tweets_dir = '/Volumes/Ed/129.215.197.21:2020'
# en_tweets = os.path.join(tweets_dir, 'en_tweets')
en_tweets = os.path.join(tweets_dir, 'en_2G')

hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)

def count_tweets():
    with codecs.open(en_tweets, encoding='utf-8') as f:
        for i,line in enumerate(f):
            print(line)
            hashtags = hashtag_re.findall(line)
            for tag in hashtags:
                hashtag_d['tag'].append(i)
    with codecs.open('stat_hashtag.pkl', 'wb') as f:
        pickle.dump(hashtag_d, f)
# print(hashtag_d)
with codecs.open('stat_hashtag.pkl', 'rb') as f:
    hashtag_stat = pickle.load(f)




# text = "people will work for a living but they'll die for recognition . - lee odden #quote"