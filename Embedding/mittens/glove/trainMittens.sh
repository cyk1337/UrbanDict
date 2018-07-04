#!/usr/bin/env bash
set -e

CORPUS=/Volumes/Ed/data
output_DIR=${CORPUS}/output

WIKI_DIR=${CORPUS}/wiki
EnWiki=${WIKI_DIR}/enwiki.txt
SimpWiki=${WIKI_DIR}/simplewiki.txt


TWEET_DIR=${CORPUS}/tweet
tweets=${TWEET_DIR}/en_2G

WIKI=$SimpWiki

WINDOW_SIZE=15
VERBOSE=2
MEMORY=16.0

./vocab_count -min-count 100 < $WIKI > ${output_DIR}/wikipedia_en.txt.vocab
#./count.sh $WIKI $WINDOW_SIZE

VOCAB_FILE=${WIKI}/vocab.txt
OOCCURRENCE_FILE=${WIKI}_win${WINDOW_SIZE}.cooccurrence.bin
COOCCURRENCE_SHUF_FILE=${WIKI}_win${WINDOW_SIZE}.cooccurrence.shuf.bin
VOCAB_FILE=${WIKI}.vocab
COOCCURRENCE_FILE=${WIKI}_win${WINDOW_SIZE}.cooccurrence.bin
COOCCURRENCE_SHUF_FILE=${WIKI}_win${WINDOW_SIZE}.cooccurrence.shuf.bin
./cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $WIKI > $COOCCURRENCE_FILE
if [[ $? -eq 0 ]]
then
    ./shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
fi


#*******************************
#./vocab_count -min-count 100 < $tweets > ${output_DIR}/twitter_en.txt.vocab.tmp
#perl -lne 'print unless /^(@|http)/' ${output_DIR}/twitter_en.txt.vocab.tmp > ${output_DIR}/twitter_en.txt.vocab
#*******************************
./vocab_count -min-count 100 < $tweets > ${output_DIR}/twitter_en.txt
#./count.sh $tweets $WINDOW_SIZE

# count.sh $tweets
VOCAB_FILE=${tweets}.vocab
COOCCURRENCE_FILE=${tweets}_win${WINDOW_SIZE}.cooccurrence.bin
COOCCURRENCE_SHUF_FILE=${tweets}_win${WINDOW_SIZE}.cooccurrence.shuf.bin
./cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $tweets > $COOCCURRENCE_FILE
if [[ $? -eq 0 ]]
then
    ./shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
fi


python ../prep_scripts/old_vocab_to_new.py ${output_DIR}/wikipedia_en.txt.vocab ${output_DIR}/twitter_en.txt.vocab > ${output_DIR}/wiki2twittervocab.txt


Adapt_SAVE_FILE=${output_DIR}/vectors
VOCAB_MIN_COUNT=5
VECTOR_SIZE=50
MAX_ITER=15

BINARY=2
NUM_THREADS=8
X_MAX=10


#./glove -save-file $Adapt_SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX \
#-iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file  -verbose $VERBOSE \
#-ind-map-file ${output_DIR}/wiki2twittervocab.txt -source-save-file ?  -adaptation-mode ?