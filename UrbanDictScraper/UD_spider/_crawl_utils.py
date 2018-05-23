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

@file: _crawl_utils.py

@time: 23/05/2018 00:30 

@desc：       
               
'''              
import os, codecs

log_dir = 'Log'

def _err_log(err):
    log_file = 'err.log'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    err_file = os.path.join(log_dir, log_file)
    with codecs.open(err_file, 'a', 'utf-8') as f:
        f.write(err)

def _msg_log(msg):
    log_file = 'msg.log'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, log_file)
    with codecs.open(log_file, 'a', 'utf-8') as f:
        f.write(msg)