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
import pycrfsuite
import sklearn_crfsuite
import eli5

from load_data import load_data, load_unlabel_data
from SL_config import *

def word2features(doc, i):
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
                # '-%s:head.text='% step + head_text1,
                # '-%s:head.pos_='% step + head_pos1,
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
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]

# A function fo generating the list of labels for each document
def get_labels(doc):
    return [tok[-1] for tok in doc]

def get_tokens(doc):
    return [tok[0].text for tok in doc]

def split_train_test_set():
    pos_data, neg_data = load_data()
    print("Starting to generate features ...")
    pos_X = [extract_features(pos_sent) for pos_sent in pos_data]
    pos_y = [get_labels(doc) for doc in pos_data]
    neg_X = [extract_features(neg_sent) for neg_sent in neg_data]
    neg_y = [get_labels(neg_y) for neg_y in neg_data]


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


def trainPyCRF(X_train, y_train):
    print("Starting training %s" % CRF_MODEL)
    trainer = pycrfsuite.Trainer(verbose=True, algorithm=ALGORITHM)

    # Submit training data to the trainer
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    # Set the parameters of the model
    trainer.set_params({
        # coefficient for L1 penalty
        'c1': L1_penalty,

        # coefficient for L2 penalty
        'c2': L2_penalty,

        # maximum number of iterations
        'max_iterations': MAX_ITER,

        # whether to include transitions that
        # are possible, but not observed
        'feature.possible_transitions': True
    })

    # Provide a file name as a parameter to the train function, such that
    # the model will be saved to the file when training is finished
    trainer.train(MODEL_FILE)
    # print(trainer.logparser.last_iteration)


def eval_Test(X_test, y_test):
    print("Loading model: %s ..." % CRF_MODEL)
    tagger = pycrfsuite.Tagger()
    tagger.open(MODEL_FILE)

    y_pred = [tagger.tag(xseq) for xseq in X_test]

    # Let's take a look at a random sample in the testing set
    # i = 0
    # for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
    #     print("%s (%s)" % (y, x))

    # Create a mapping of labels to indices
    labels = {IN_SIGN: 0, OUT_SIGN: 1}

    # Convert the sequences of tags into a 1-dimensional array
    predictions = [labels[tag] for row in y_pred for tag in row]
    truths = [labels[tag] for row in y_test for tag in row]

    # Print out the classification report
    print(classification_report(
        truths, predictions,
        target_names=[IN_SIGN, OUT_SIGN]))

def mk_prediction():
    tagger = pycrfsuite.Tagger()
    tagger.open(MODEL_FILE)
    count = 0


    for unlabel_data, unlabel_defids, unlabel_word in load_unlabel_data():

        # y_pred = [tagger.tag(xseq) for xseq in pos_data]
        # for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
        #     print("%s (%s)" % (y, x))
        for i, unlabel_sent in enumerate(unlabel_data):
            # print(' '.join(get_tokens(unlabel_sent)), end='\n')
            xseq = extract_features(unlabel_sent)
            y_pred = tagger.tag(xseq)
            # only print sent that is predicted as positive

            if IN_SIGN in y_pred:
                out = "{}\t{}\t".format(unlabel_word[i], unlabel_defids[i])
                print(count, '-'*80)
                count += 1
                for word, label in zip(unlabel_sent, y_pred):
                    if label == IN_SIGN:
                        out += " %s (%s)" % (word[0], label)
                    else:
                        out += " {}".format(word[0])
                res_file = os.path.join(result_dir, '%s.txt' % CRF_MODEL)
                print(out, file=open(res_file, 'a'))


    # print("Predicted:", ' '.join(tagger.tag(extract_features(unlabel_sent))))
    # print("Correct:  ", ' '.join(get_labels(unlabel_sent)))


def main():
    (X_train, y_train), (X_test, y_test) = split_train_test_set()
    # train `pycrfsuite` CRF model
    if not os.path.exists(MODEL_FILE):
        trainPyCRF(X_train, y_train)
    else:
        print("%s already exists!" % CRF_MODEL)

    print('Starting evaluation ..')
    eval_Test(X_test, y_test)

    # print('Starting prediction ..')
    # mk_prediction()



if __name__ == '__main__':
    main()