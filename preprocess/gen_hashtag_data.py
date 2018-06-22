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
    print("Start reading tweets ...")
    with codecs.open(en_tweets, encoding='utf-8') as f:
        for i,line in enumerate(f):
            toks = line.split()
            if toks[-1][0] == '#' and len(toks)>5:
                hashtags = hashtag_re.findall(line)
                if len(hashtags) ==1:
                    for tag in hashtags:
                        hashtag_d[tag].append(i)
    with codecs.open('stat_hashtag.pkl', 'wb') as f:
        pickle.dump(hashtag_d, f)
    print("Finish reading tweets ...")

count_tweets()

with codecs.open('stat_hashtag.pkl', 'rb') as f:
    hashtag_stat = pickle.load(f)

def take_top_30():
    hashtag_count = dict()
    for k, v in hashtag_stat.items():
        hashtag_count[k] = len(v)

    # take the most 10
    d = sorted(hashtag_count.items(), key=lambda x: x[1], reverse=True)[:30]
    # tags = [t[0] for t in d]

    with codecs.open('stat_hashtag10.pkl', 'wb') as f:
        pickle.dump(d, f)

take_top_30()

with codecs.open('stat_hashtag10.pkl', 'rb') as f:
    hashtag_10 = pickle.load(f)


with codecs.open(en_tweets, encoding='utf-8') as f:
    print("Start writing to file ...")
    for i,line in enumerate(f):
        for t in hashtag_10:
            tag = t[0]
            fname = os.path.join('hashtag', tag)
            if i in hashtag_stat[tag]:
                with open(fname, 'a', encoding='utf-8') as file:
                    file.write(line+'\n')
                    print(line)

    print("finish writing ...")

# remove the duplicates
# rm_l = []
# line_list = []
# for t in tags:
#     line_n = hashtag_stat[t]
#     line_list.extend(line_n)
#
# tmp = []
# for i in line_list:
#     if i not in tmp:
#         tmp.append(i)
#     else:
#         rm_l.append(i)
#
# tag_d = dict()
# for t in tags:
#     tag_d[t] = hashtag_stat[t]
#     for x in tag_d[t]:
#         if x in rm_l:
#             tag_d[t].remove(x)







# text = "people will work for a living but they'll die for recognition . - lee odden #quote"