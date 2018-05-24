#!/usr/bin/env python

# encoding: utf-8

'''
  
             \ \ / /__| | ___   _ _ __    / ___| | | |  / \  |_ _|
              \ V / _ \ |/ / | | | '_ \  | |   | |_| | / _ \  | | 
               | |  __/   <| |_| | | | | | |___|  _  |/ ___ \ | | 
               |_|\___|_|\_\\__,_|_| |_|  \____|_| |_/_/   \_\___
 ==========================================================================
@author: Yekun Chai

@license: School of Informatics, Edinburgh

@contact: s1718204@sms.ed.ac.uk

@file: run_UD_spider.py

@time: 15/05/2018 16:46

@desc:         
               
'''              


from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print("Urban Dict spider dir:", os.path.dirname(os.path.abspath(__file__)))

# uncomment this for directly scraping from website
execute(['scrapy', 'crawl', 'UD'])

# uncomment this for fetch data from API
# execute(['scrapy', 'crawl', 'UD-API'])



# -------------------------
# prevent OSX from sleeping.
# -------------------------
# pmset noidle
