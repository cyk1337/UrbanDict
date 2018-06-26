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
import numpy as np

from load_data import load_data
from SL_config import *

def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    # Common features for all words
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i-1][0]
        postag1 = doc[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word.isdigit=%s' % word1.isdigit(),
            '-1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS')

    # Features for words that are not
    # at the end of a document
    if i < len(doc)-1:
        word1 = doc[i+1][0]
        postag1 = doc[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:word.isdigit=%s' % word1.isdigit(),
            '+1:postag=' + postag1
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
    return [label for _, _, label in doc]

#
def get_tokens(doc):
    return [token for token, _,_ in doc]

def split_train_test_set():
    pos_data, neg_data = load_data()
    pos_X = [extract_features(pos_sent) for pos_sent in pos_data]
    pos_y = [get_labels(doc) for doc in pos_data]
    neg_X = [extract_features(neg_sent) for neg_sent in neg_data]
    neg_y = [get_labels(neg_y) for neg_y in neg_data]


    pos_X_train, pos_X_test, pos_y_train, pos_y_test = train_test_split(
        pos_X, pos_y, test_size=TEST_SET_FRAC, random_state=SEED, shuffle=True)
    neg_X_train, neg_X_test, neg_y_train, neg_y_test = train_test_split(
        neg_X, neg_y, test_size=TEST_SET_FRAC, random_state=SEED, shuffle=True)

    X_train = pos_X_train + neg_X_train
    y_train = pos_y_train + neg_y_train
    X_test = pos_X_test + neg_X_test
    y_test = pos_y_test + neg_y_test

    return (X_train, y_train), (X_test, y_test)


def trainPyCRF(X_train, y_train):

    trainer = pycrfsuite.Trainer(verbose=True)

    # Submit training data to the trainer
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    # Set the parameters of the model
    trainer.set_params({
        # default
        'algorithm': 'lbfgs', # {‘lbfgs’, ‘l2sgd’, ‘ap’, ‘pa’, ‘arow’}
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
    labels = {"I": 1, "O": 0}

    # Convert the sequences of tags into a 1-dimensional array
    predictions = np.array([labels[tag] for row in y_pred for tag in row])
    truths = np.array([labels[tag] for row in y_test for tag in row])

    # Print out the classification report
    print(classification_report(
        truths, predictions,
        target_names=["I", "O"]))

    # y_pred = [tagger.tag(xseq) for xseq in X_test]
    #
    # # Let's take a look at a random sample in the testing set
    # i = 12
    # for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
    #     print("%s (%s)" % (y, x))
    #
    # print("Predicted:", ' '.join(tagger.tag(extract_features(example_sent))))
    # print("Correct:  ", ' '.join(get_labels(example_sent)))

def main():
    (X_train, y_train), (X_test, y_test) = split_train_test_set()
    # train CRF model
    if not os.path.exists(MODEL_FILE):
        trainPyCRF(X_train, y_train)

    eval_Test(X_test, y_test)



if __name__ == '__main__':
    main()