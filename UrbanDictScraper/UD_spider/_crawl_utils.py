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
import os, codecs, time, math

log_dir = 'Log'

def _err_log(err):
    log_file = 'err.log'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    err_file = os.path.join(log_dir, log_file)
    with codecs.open(err_file, 'a', 'utf-8') as f:
        f.write(err)

def _time_log(parse_full_field, spider_name, pipline_name, start_time, finish_time):
    if start_time is None or finish_time is None:
        return
    log_file = 'spider.log'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, log_file)
    with codecs.open(log_file, 'a', 'utf-8') as f:
        timedelta = finish_time - start_time
        runtime_msg = days_hours_mins_secs(timedelta)
        msg = 'ParseAll:{}, Spider:{},{}, start:{}, finish:{}, runtime:{}\n'\
            .format(parse_full_field, spider_name, pipline_name, str(start_time), str(finish_time), runtime_msg)
        msg = '{}{}{}'.format(msg, '-'*30, '\n')
        print(msg)
        f.write(msg)


def days_hours_mins_secs(td):
    return "{}d,{}h,{}m,{}s".format(td.days, td.seconds//3600, (td.seconds//60)%60, td.seconds%60)

def _filter_word_log(word_info):
    log_file = 'filtered_word.log'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, log_file)
    with codecs.open(log_file, 'a', 'utf-8') as f:
        f.write(word_info)



def changeTime(allTime):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return "%d sec" % math.ceil(allTime)
    elif allTime > day:
        days = divmod(allTime, day)
        return "%d days, %s" % (int(days[0]), changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return '%d hours, %s' % (int(hours[0]), changeTime(hours[1]))
    else:
        mins = divmod(allTime, min)
        return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))