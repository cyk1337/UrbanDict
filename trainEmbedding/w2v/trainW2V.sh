#!/usr/bin/env bash

source activate mlp

#for MAX_VOCAB in 5000; do
#    python W2V.py --MaxVocab $MAX_VOCAB
#done

for MIN_COUNT in 100; do
    python W2V.py --minCount $MIN_COUNT
done