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

@file: trainCRF.py

@time: 26/06/2018 17:44 

@desc：

'''              
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.externals import joblib
import datetime

# import pycrfsuite
import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pandas as pd
import eli5

from load_data import load_data, load_unlabel_data
from SL_config import *
from _utils import days_hours_mins_secs

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfTrainCRF(object):
    def __init__(self):
        self.ITER_NUM = 1
        self.iter_start_time =None
        self.iter_finish_time =None
        # pass

    def word2features(self, doc, i):
        # TODO: add quote information
        w = doc[i][0]
        word = w.text
        pos_ = w.pos_
        tag_ = w.tag_
        lemma_ = w.lemma_
        dep_ = w.dep_
        shape_ = w.shape_
        is_stop = w.is_stop
        is_alpha = w.is_alpha
        head_text =  w.head.text
        head_pos = w.head.pos_
        head_tag = w.head.tag_

        # Common features for all words
        features = [
            'bias',
            'word.lower=' + word.lower(),
            # 'word[-3:]=' + word[-3:],
            # 'word[-2:]=' + word[-2:],
            'word.isupper=%s' % word.isupper(),
            'word.istitle=%s' % word.istitle(),
            'word.isdigit=%s' % word.isdigit(),
            'pos_=' + pos_,
            'tag_=' + tag_,
            'dep_=' + dep_,
            # 'shape_=' + shape_,
            'lemma_=' + lemma_,
            'head_text=' + head_text,
            'head_pos=' + head_pos,
            'head_tag=' + head_tag,

        ]



        for step in range(1, 1+FEAT_CTX_SIZE):
            # Features for words that are not
            # at the beginning of a document
            if i-step > 0:
                w1 = doc[i-step][0]
                word1 = w1.text
                pos_1 = w1.pos_
                tag_1 = w1.tag_
                lemma_1 = w1.lemma_
                dep_1 = w1.dep_
                # shape_1 = w1.shape_
                # is_stop1 = w1.is_stop
                # is_alpha1 = w1.is_alpha
                head_text1 = w1.head.text
                head_pos1 = w1.head.pos_
                head_tag1 = w1.head.tag_
                features.extend([
                    '-%s:word.lower=' % step + word1.lower(),
                    '-%s:word.istitle=%s' % (step, word1.istitle()),
                    '-%s:word.isupper=%s' % (step, word1.isupper()),
                    '-%s:word.isdigit=%s' % (step, word1.isdigit()),
                    '-%s:pos_='% step + pos_1,
                    # '-%s:tag_='% step + tag_1,
                    # '-%s:lemma_='% step + lemma_1,
                    # '-%s:dep_='% step + dep_1,
                    # '-%s:shape_='% step + shape_1,
                    # '-%s:is_stop=%s' % (step, is_stop1),
                    # '-%s:is_alpha=%s' % (step, is_alpha1),
                    '-%s:head.text='% step + head_text1,
                    '-%s:head.pos_='% step + head_pos1,
                    # '-%s:head_tag_='% step + head_tag1,
                ])
            else:
                # Indicate that it is the 'beginning of a document'
                features.append('BOS')

            # Features for words that are not
            # at the end of a document
            if i+step < len(doc)-1:
                w1 = doc[i+step+1][0]
                word1 = w1.text
                pos_1 = w1.pos_
                tag_1 = w1.tag_
                lemma_1 = w1.lemma_
                dep_1 = w1.dep_
                shape_1 = w1.shape_
                # is_stop1 = w1.is_stop
                # is_alpha1 = w1.is_alpha
                head_text1 = w1.head.text
                head_pos1 = w1.head.pos_
                head_tag1 = w1.head.tag_
                features.extend([
                    '+%s:word.lower=' % step + word1.lower(),
                    '+%s:word.istitle=%s' % (step ,word1.istitle()),
                    '+%s:word.isupper=%s' % (step, word1.isupper()),
                    '+%s:word.isdigit=%s' % (step, word1.isdigit()),
                     '+%s:pos_=%s' % (step, pos_1),
                    '+%s:tag_=%s' % (step, tag_1),
                    '+%s:lemma_=%s' % (step, lemma_1),
                    '+%s:dep_=%s' % (step, dep_1),
                    # '+%s:shape_=%s' % (step, shape_1),
                    # '+%s:shape_=%s' % (step, shape_1),
                    # '+%s:is_stop=%s' % (step, is_stop1),
                    # '+%s:is_alpha=%s' % (step, is_alpha1),
                    '+%s:head.text=%s' % (step, head_text1),
                    '+%s:head.pos_=%s' % (step, head_pos1),
                    # '+%s:head_tag_=%s' % (step, head_tag1),
                ])
            else:
                # Indicate that it is the 'end of a document'
                features.append('EOS')

        return features


    # A function for extracting features in documents
    def extract_features(self, doc):
        return [self.word2features(doc, i) for i in range(len(doc))]

    # A function fo generating the list of labels for each document
    def get_labels(self, doc):
        return [tok[-1] for tok in doc]

    def get_tokens(self, doc):
        return [tok[0].text for tok in doc]

    def split_train_test_set(self):
        print("Iter %s : starting to load data ..." % self.ITER_NUM)
        pos_data, neg_data = load_data(self.ITER_NUM)
        print("Iter %s : starting to generate features ..." % self.ITER_NUM)
        pos_X = [self.extract_features(pos_sent) for pos_sent in pos_data]
        pos_y = [self.get_labels(doc) for doc in pos_data]
        neg_X = [self.extract_features(neg_sent) for neg_sent in neg_data]
        neg_y = [self.get_labels(neg_y) for neg_y in neg_data]


        pos_X_train, pos_X_test, pos_y_train, pos_y_test = train_test_split(
            pos_X, pos_y, test_size=TEST_SET_FRAC, random_state=SEED, shuffle=True)
        neg_X_train, neg_X_test, neg_y_train, neg_y_test = train_test_split(
            neg_X, neg_y, test_size=TEST_SET_FRAC, random_state=SEED, shuffle=True)

        # X_train = pos_X_train
        # y_train = pos_y_train

        X_train = pos_X_train + neg_X_train
        y_train = pos_y_train + neg_y_train

        X_test = pos_X_test + neg_X_test
        y_test = pos_y_test + neg_y_test

        return (X_train, y_train), (X_test, y_test)


    def trainCRF(self, X_train, y_train, dump_file):
        print("Starting training %s" % CRF_MODEL)

        crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=L1_penalty,
            c2=L2_penalty,
            max_iterations=MAX_ITER,
            all_possible_transitions=False,
        )
        crf.fit(X_train, y_train)

        # eli5.show_weights(crf, top=30)

        joblib.dump(crf, dump_file)
        return crf


    def eval_Test(self, X_test, y_test, crf, file):
        print("Loading model: %s ..." % CRF_MODEL)
        labels = list(crf.classes_)
        y_pred = crf.predict(X_test)
        metrics.flat_f1_score(y_test, y_pred,
                              average='weighted', labels=labels)

        sorted_labels = sorted(
            labels,
            key=lambda name: (name[1:], name[0])
        )

        print("{} Iter{}".format(self.ITER_NUM,CRF_MODEL), file=open(file, 'a'))
        print(metrics.flat_classification_report(
            y_test, y_pred, labels=sorted_labels, digits=3
        ), file=open(file, 'a'))

        print(metrics.flat_classification_report(
            y_test, y_pred, labels=sorted_labels, digits=3
        ))


    def mk_prediction(self, crf):
        count = 0
        res_dir = os.path.join(result_dir, CRF_MODEL)
        if not os.path.exists(res_dir):
            os.mkdir(res_dir)
        res_file = os.path.join(res_dir, 'Iteration%s.txt' % self.ITER_NUM )
        print("Iteration %s\n" % self.ITER_NUM + "*"*80, file=open(res_file, 'a'))

        for unlabel_data, unlabel_defids, unlabel_word, unlabel_defn in load_unlabel_data():

            # y_pred = [tagger.tag(xseq) for xseq in pos_data]
            # for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
            #     print("%s (%s)" % (y, x))

            rows_ = []
            for i, unlabel_sent in enumerate(unlabel_data):
                # print(' '.join(get_tokens(unlabel_sent)), end='\n')
                xseq = self.extract_features(unlabel_sent)
                y_pred = crf.predict_single(xseq)
                # only print sent that is predicted as positive
                records = dict()

                if IN_SIGN in y_pred:
                    pos_index_list = [pos_indice for pos_indice, y_ in enumerate(y_pred) if y_ == IN_SIGN]
                    for pos_indice in pos_index_list:
                        pos_prob = crf.predict_marginals_single(xseq)[pos_indice][IN_SIGN]
                        if pos_prob > CRF_THRESHOLD:
                            out = "".format()
                            # print(count, '-'*80)
                            count += 1

                            records['defid'] = unlabel_defids[i]
                            records['word'] = unlabel_word[i]
                            records['definition'] = unlabel_defn[i]
                            records['label_index'] = ''
                            records['variant'] = ''
                            # concatenate sentences
                            # variant_list = []
                            out_sent = ""
                            for label_index, (word, label) in enumerate(zip(unlabel_sent, y_pred)):
                                if label == IN_SIGN:
                                    records['label_index'] += "{} ".format(label_index)
                                    records['variant'] += "{} ".format(word[0])
                                    # variant_list.append(word[0])
                                    out_sent += " %s (%s, %.4f)" % (word[0], label, pos_prob)
                                else:
                                    out_sent += " {}".format(word[0])
                            # TODO: achive result w.r.t. iteration
                            out = "{}\t{}\t{}\t{}".format(unlabel_defids[i], unlabel_word[i],records['variant'], out_sent)
                            print(out, file=open(res_file, 'a'))
                            print("{}-\t{}".format(count,out))
                if 'label_index' in records.keys():
                    rows_.append(records)

            self.gen_silver_data(rows_)




        # print("Predicted:", ' '.join(tagger.tag(extract_features(unlabel_sent))))
        # print("Correct:  ", ' '.join(get_labels(unlabel_sent)))

    def gen_silver_data(self, rows_):
        # Save silver data for self-training
        # filepath: /silver/{CRF_MODEL}/pos{ITER}
        iter_dir = os.path.join(silver_dir, CRF_MODEL)
        if not os.path.exists(iter_dir):
            os.mkdir(iter_dir)
        SILVER_POS_DATA = os.path.join(iter_dir, '%spos.csv' % self.ITER_NUM)
        # SILVER_NEG_DATA = os.path.join(silver_dir, 'neg.csv')

        chunk_df = pd.DataFrame(rows_, columns=['defid', 'word', 'variant', 'label_index', 'definition'])

        if os.path.exists(SILVER_POS_DATA):
            header = False
        else:
            header = True

        chunk_df.to_csv(SILVER_POS_DATA, sep = '\t', index = False, mode = 'a', header=header)



    def run(self):
        _dir = os.path.join(model_dir, CRF_MODEL)


        try:
            os.mkdir(_dir)
        except Exception as e:
            print("Fail to create mdoel file: %s" % e)

        while self.ITER_NUM < SELF_ITERATION:
            iter_start_time = datetime.datetime.now()

            MODEL_FILE = os.path.join(_dir, "{}{}.model".format(self.ITER_NUM,CRF_MODEL))
            if not os.path.exists(MODEL_FILE):
                (X_train, y_train), (X_test, y_test) = self.split_train_test_set()
                crf = self.trainCRF(X_train, y_train, MODEL_FILE)

                print('Starting evaluation ..')
                file = os.path.join(eval_dir, CRF_MODEL)
                self.eval_Test(X_test, y_test, crf, file=file)
            else:
                print("loading existing model ...")
                crf = joblib.load(MODEL_FILE)

                # print('Starting evaluation ..')
                # (_, _), (X_test, y_test) = split_train_test_set()
                # eval_Test(X_test, y_test, crf)

            print('Starting to predict unlabeled data ...')
            self.mk_prediction(crf)

            # calc run time for each iteration
            timedelta = datetime.datetime.now() - iter_start_time
            run_time = days_hours_mins_secs(timedelta)
            iter_time_log = "{}-iter{} -runtime: {}".format(CRF_MODEL, self.ITER_NUM, run_time)
            logger.info(iter_time_log)
            with open(LOG_FILE, 'a') as f:
                f.write(iter_time_log)

            # global ITER_NUM
            self.ITER_NUM += 1

if __name__ == '__main__':
    crf_ = SelfTrainCRF()
    crf_.run()
