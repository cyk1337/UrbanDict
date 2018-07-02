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

@file: plot_wordcloud.py

@time: 03/06/2018 20:21 

@desc：       
               
'''
from os import path
import os
from wordcloud import WordCloud

d = path.dirname(__file__)
wordcloud_dir = os.path.join(d, 'WordCloud')
# Read the whole text.
# text = open(path.join(d, 'constitution.txt')).read()
import pandas as pd
import sqlalchemy as sa
import matplotlib.pyplot as plt


def fetch_data():
    engine = sa.create_engine('mysql+pymysql://root:admin@localhost/UrbanDict?charset=utf8')
    conn = engine.connect()
    db_name = 'UrbanDict'
    sql_loadUD = "SELECT definition FROM %s" % db_name
    chunksize = None
    df = pd.read_sql(sql=sql_loadUD, con=conn, chunksize=chunksize)
    return ' '.join(df['definition'])


# Generate a word cloud image
# wordcloud = WordCloud().generate(text)

def basic_plot(text):
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.figure()
    plt.figure(figsize=(20, 10), facecolor='k')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plot_path = os.path.join(wordcloud_dir, 'basic.pdf')
    plt.savefig(plot_path, facecolor='k', bbox_inches='tight')
    plt.show()
    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()


def mask(text):
    import numpy as np
    from PIL import Image
    from os import path
    import matplotlib.pyplot as plt
    import random

    from wordcloud import WordCloud, STOPWORDS

    def grey_color_func(word, font_size, position, orientation, random_state=None,
                        **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

    # d = path.dirname(__file__)

    # read the mask image
    # taken from
    # http://www.stencilry.org/stencils/movies/star%20wars/storm-trooper.gif
    mask = np.array(Image.open(path.join(wordcloud_dir, "stormtrooper_mask.png")))

    # movie script of "a new hope"
    # http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html
    # May the lawyers deem this fair use.

    # preprocessing the text a little bit
    # text = text.replace("HAN", "Han")
    # text = text.replace("LUKE'S", "Luke")

    # adding movie script specific stopwords
    stopwords = set(STOPWORDS)
    # stopwords.add("int")
    # stopwords.add("ext")

    wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
                   random_state=1).generate(text)
    # store default colored image
    default_colors = wc.to_array()
    plt.title("Custom colors")
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
               interpolation="bilinear")
    wc.to_file("a_new_hope.png")
    plt.axis("off")
    plt.figure()
    # plt.title("Default colors")
    plt.imshow(default_colors, interpolation="bilinear")
    plt.axis("off")
    plot_path = os.path.join(wordcloud_dir, 'masked.pdf')
    plt.savefig(plot_path)
    plt.show()


if __name__ == '__main__':
    text = fetch_data()
    basic_plot(text)
    # mask(text)
