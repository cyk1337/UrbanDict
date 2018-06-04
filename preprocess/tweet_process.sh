#!/usr/bin/env bash

source ~/.benv
source activate mlp

python TwitterProcess.py

#/afs/inf.ed.ac.uk/user/s17/s1718204/PycharmProjects/UD/UrbanDict_SpellingVariants/preprocess/

#longjob -28day -c ./tweet_process.sh

#ps -ef | grep tweet_process.sh