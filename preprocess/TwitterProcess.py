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

@file: TwitterProcess.py

@time: 03/06/2018 16:10 
'''

import gzip, os, sys

work_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(work_dir)

from langdetect import detect
from preprocess.twokenize import tokenizeRawTweetText
from preprocess.Preprocess_sub import tokenize

from numba import jit

""" data field
["tweetId", "fromUserId", "fromUserName", "fromUserScreenName", 
"fromUserBigProfileImageURL", "fromUserTimeZone", "fromUserFollowersCount",
"fromUserFolloweesCount", "fromUserLocation", "fromUserLang"(9), "source",
"country", "place", "coordinates", "createdAt", "text"(15), "URLList",
"mediaURLList", "hashTagList", "mentionsList", "retweetCount",
"originalTweetId", "originalTweetText",]
"""


tweets_dir='/disk/data/wmagdy/TweetCrawlers/General/data'
en_tweets = 'en_tweets'

# test_file_path = os.path.join(tweets_dir, 'tweets.2017-02-07.txt.gz')
# tweets_dir = '/Volumes/Ed/129.215.197.21:2020'
# en_tweets = os.path.join(tweets_dir, 'en_tweets')

# if os.path.exists(en_tweets):
#     os.remove(en_tweets)
@jit
def tweet_process(text):
    line = ' '.join(tokenizeRawTweetText(text)).lower()
    # replace url, emojs ..
    # return tokenize(line)
    return line

@jit
def traverse_docs():
    for file_path in os.listdir(tweets_dir):
        if not file_path.endswith('txt.gz'):
            continue
        else:
            with open('tweet_process.log', 'a') as f:
                f.write("Processing {}".format(file_path))
            file_path = os.path.join(tweets_dir, file_path)
            yield file_path

def save_en_tweets(langId, text):
    try:
        if langId.lower() == 'en' and detect(text) == 'en':
            # preprocess tweets
            text = tweet_process(text)
            # print(langId, text.encode('utf-8'))
            with open(en_tweets, 'a', encoding='utf8') as f:
                f.write(text + '\n')
    except Exception as e:
        # merely URL, emoji, hard to detect languages
        # print("Except:", text.encode('utf-8'), e)
        pass

def main():
    for file_path in traverse_docs():
        with gzip.open(file_path, mode='rt', encoding='utf8') as f:
            for line in f:
                cols = line.split('\t')
                if len(cols) != 23:
                    continue
                # langId = cols[9]
                # text = cols[15]
                save_en_tweets(cols[9], cols[15])


if __name__ == '__main__':
    main()


