#!/usr/bin/env bash
set -e


CORPUS=/Volumes/Ed/data
output_DIR=${CORPUS}/output

WIKI_DIR=${CORPUS}/wiki
EnWiki=${WIKI_DIR}/enwiki.txt
SimpWiki=${WIKI_DIR}/simplewiki.txt

WIKI=$SimpWiki

#tweet dir
TWEET_DIR=${CORPUS}/tweet
tweets=${TWEET_DIR}/en_2G



BUILDDIR=glove
VERBOSE=2
MEMORY=16.0
VOCAB_MIN_COUNT=5
VECTOR_SIZE=50
MAX_ITER=15
WINDOW_SIZE=15
BINARY=2
NUM_THREADS=8
X_MAX=10

wiki_VOCAB_FILE=simpwiki.txt.vocab
wiki_SAVE_FILE=wiki_vectors

# wiki2tweet vocab file
w2t_VOCAB_FILE=${output_DIR}/wiki2twittervocab.txt

wiki_COOCCURRENCE_FILE=wiki_win${WINDOW_SIZE}.cooccurrence.bin
wiki_COOCCURRENCE_SHUF_FILE=wiki_win${WINDOW_SIZE}.cooccurrence.shuf.bin

${BUILDDIR}/vocab_count -min-count 100 < $WIKI > $wiki_VOCAB_FILE
#./count.sh $WIKI $WINDOW_SIZE


${BUILDDIR}/cooccur -memory $MEMORY -vocab-file $wiki_VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $WIKI > $wiki_COOCCURRENCE_FILE

${BUILDDIR}/shuffle -memory $MEMORY -verbose $VERBOSE < $wiki_COOCCURRENCE_FILE > $wiki_COOCCURRENCE_SHUF_FILE

echo "$ $BUILDDIR/glove -save-file $wiki_SAVE_FILE -threads $NUM_THREADS -input-file $wiki_COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $wiki_VOCAB_FILE -verbose $VERBOSE"
$BUILDDIR/glove -save-file $wiki_SAVE_FILE -threads $NUM_THREADS -input-file $wiki_COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $wiki_VOCAB_FILE -verbose $VERBOSE



#################################
# tweets
#################################

tweet_VOCAB_FILE=tweet.txt.vocab
tweet_SAVE_FILE=tweet_vectors
tweet_COOCCURRENCE_FILE=tweet_win${WINDOW_SIZE}.cooccurrence.bin
tweet_COOCCURRENCE_SHUF_FILE=tweet_win${WINDOW_SIZE}.cooccurrence.shuf.bin

#*******************************
#./vocab_count -min-count 100 < $tweets > ${output_DIR}/twitter_en.txt.vocab.tmp
#perl -lne 'print unless /^(@|http)/' ${output_DIR}/twitter_en.txt.vocab.tmp > ${output_DIR}/twitter_en.txt.vocab
#*******************************
echo "$ ${BUILDDIR}/vocab_count -min-count 100 < $tweets > $tweet_VOCAB_FILE"
${BUILDDIR}/vocab_count -min-count 100 < $tweets > $tweet_VOCAB_FILE
#./count.sh $tweets $WINDOW_SIZE

# count.sh $tweets
echo "$ ${BUILDDIR}/cooccur -memory $MEMORY -vocab-file $tweet_VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $tweets > $tweet_COOCCURRENCE_FILE"
${BUILDDIR}/cooccur -memory $MEMORY -vocab-file $tweet_VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $tweets > $tweet_COOCCURRENCE_FILE

echo "$ ${BUILDDIR}/shuffle -memory $MEMORY -verbose $VERBOSE < $tweet_COOCCURRENCE_FILE > $tweet_COOCCURRENCE_SHUF_FILE"
${BUILDDIR}/shuffle -memory $MEMORY -verbose $VERBOSE < $tweet_COOCCURRENCE_FILE > $tweet_COOCCURRENCE_SHUF_FILE

echo "$ $BUILDDIR/glove -save-file $tweet_SAVE_FILE -threads $NUM_THREADS -input-file $tweet_COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $tweet_VOCAB_FILE -verbose $VERBOSE"
$BUILDDIR/glove -save-file $tweet_SAVE_FILE -threads $NUM_THREADS -input-file $tweet_COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $tweet_VOCAB_FILE -verbose $VERBOSE


python prep_scripts/old_vocab_to_new.py $wiki_VOCAB_FILE $tweet_VOCAB_FILE > $w2t_VOCAB_FILE


#echo "$ $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE"
#$BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE
#echo "$ $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE"
#$BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE
#echo "$ $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE"
#$BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
#echo "$ $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE"
#$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE




w2t_SAVE_FILE=${output_DIR}/w2t_vectors

$BUILDDIR/glove -input-file $tweet_COOCCURRENCE_SHUF_FILE -vocab-file $tweet_VOCAB_FILE -save-file $w2t_SAVE_FILE -gradsq-file gradsq -verbose $VERBOSE -vector-size $VECTOR_SIZE -threads $NUM_THREADS \
-alpha 0.75 -x-max $X_MAX -eta 0.05 -binary 2 -model 2\
-source-save-file $wiki_SAVE_FILE -ind-map-file $w2t_VOCAB_FILE -target-save-file $tweet_SAVE_FILE -adaptation-mode 1
#-lambda1 0.1 -lambda2 0.1

#./glove -save-file $Adapt_SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX \
#-iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file  -verbose $VERBOSE \
#-ind-map-file ${output_DIR}/wiki2twittervocab.txt -source-save-file ?  -adaptation-mode ?