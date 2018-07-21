#!/usr/bin/env bash

source activate mlp

#for MAX_VOCAB in 5000; do
#    python W2V.py --MaxVocab $MAX_VOCAB
#done
for WIN in 10 15; do
for VEC_SIZE in 100 200; do
    python W2V.py --vecSize $VEC_SIZE --window $WIN
done
done