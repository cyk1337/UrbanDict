#!/usr/bin/env bash
#
# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

RESULTDIR=result
#DATADIR=data

mkdir -p "${RESULTDIR}"
#mkdir -p "${DATADIR}"

#if [ ! -f "${DATADIR}/fil9" ]
#then
#  wget -c http://mattmahoney.net/dc/enwik9.zip -P "${DATADIR}"
#  unzip "${DATADIR}/enwik9.zip" -d "${DATADIR}"
#  perl wikifil.pl "${DATADIR}/enwik9" > "${DATADIR}"/fil9
#fi
#
#if [ ! -f "${DATADIR}/rw/rw.txt" ]
#then
#  wget -c https://nlp.stanford.edu/~lmthang/morphoNLM/rw.zip -P "${DATADIR}"
#  unzip "${DATADIR}/rw.zip" -d "${DATADIR}"
#fi

make

#tweet dir
TWEET_DIR=/Volumes/Ed/data/tweet
tweets=${TWEET_DIR}/en_2G

output_file=${RESULTDIR}/fasttextModel

echo "$ ./fasttext skipgram -input $tweets -output $output_file -dim 100 -ws 5 -epoch 5 -minCount 100 -neg 5"
./fasttext skipgram -input $tweets -output $output_file -dim 100 -ws 5 -epoch 5 -minCount 100 -neg 5
# ./fasttext skipgram -input $CORPUS -output $outputfile -dim 100 -ws 5 -epoch 5 -minCount 100 -neg 5

#cut -f 1,2 "${DATADIR}"/rw/rw.txt | awk '{print tolower($0)}' | tr '\t' '\n' > "${DATADIR}"/queries.txt
#
#./fasttext print-word-vectors "${RESULTDIR}"/$output_file.bin > "${RESULTDIR}"/vectors.txt
#
#python eval.py -m "${RESULTDIR}"/vectors.txt -d "${DATADIR}"/rw/rw.txt
