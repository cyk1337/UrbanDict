#!/bin/bash

CORPUS=$1
WINDOW_SIZE=$2
VOCAB_FILE=${CORPUS}.vocab
COOCCURRENCE_FILE=${CORPUS}_win${WINDOW_SIZE}.cooccurrence.bin
COOCCURRENCE_SHUF_FILE=${CORPUS}_win${WINDOW_SIZE}.cooccurrence.shuf.bin
VERBOSE=2
MEMORY=16.0

./cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE
if [[ $? -eq 0 ]]
then
    ./shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
fi
