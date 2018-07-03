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

@file: sample2eval.py

@time: 01/07/2018 12:56 

@desc：       
               
'''

from SL_config import *

all_result_file = os.path.join(result_dir, 'all_results.log')


def gen_sample100(dir_name, sample_dir):
    if not os.path.exists(sample_dir):
        os.mkdir(sample_dir)
    for _file in os.listdir(dir_name):
        if not _file.startswith('Iteration'): continue
        filename = os.path.join(dir_name, _file)
        sample_file = os.path.join(sample_dir, _file[:4] + _file[-5] + "sample100.txt")
        shuf_cmd = "gshuf -n 100 %s | gsed 's/^/\t/' > %s" % (filename, sample_file)
        os.system(shuf_cmd)
        print("{} generated".format(sample_file))


def count_estimated_label(_dir, sample_dir):
    os.system("echo ---------------------- >> %s" % (all_result_file))
    os.system("echo %s | tee -a %s" % (_dir, all_result_file))
    for sample_ in sorted(os.listdir(sample_dir)):
        if not sample_.startswith('Iter'): continue
        sample_file = os.path.join(sample_dir, sample_)
        silver_exp = os.path.join(silver_dir, _dir)

        with open(sample_file) as f:
            label_list = []
            for line in f.readlines():
                label = line.split('\t')[0]
                label_list.append(label)
            prec = 1 - label_list.count('0') / 100
            prec_log_file = os.path.join(sample_dir, 'prec.log')
            silver_file = os.path.join(silver_exp, sample_[4] + 'pos.csv')
            os.system("echo iter%s: prec:%.2f, line_num: %s | tee -a %s" % (
                sample_[4], prec, file_len(silver_file) - 1, prec_log_file))
            os.system("echo iter%s: prec:%.2f, line_num: %s | tee -a %s" % (
                sample_[4], prec, file_len(silver_file) - 1, all_result_file))

            print('Finish counting %s' % sample_)
    print('Complete eval %s' % _dir)


import subprocess


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def eval_single_exp(_dir):
    dir_name = os.path.join(result_dir, _dir)
    sample_dir = os.path.join(dir_name, 'Sample100')
    # Caution: sample data will change already sampled file!
    # gen_sample100(dir_name, sample_dir)
    #
    count_estimated_label(_dir, sample_dir)


def main():
    for _dir in os.listdir(result_dir):
        if _dir.startswith("CRF"):
            eval_single_exp(_dir)


if __name__ == '__main__':
    #############################
    # eval one exp dir
    #############################
    # _dir = "CRF_lbfgs_Iter200_L1{2.35}_L2{0.08}_ctx4_conf0.9"
    # eval_single_exp(_dir)

    #############################
    # eval all result dir
    #############################
    main()
