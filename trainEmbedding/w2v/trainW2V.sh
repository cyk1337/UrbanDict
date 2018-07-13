#!/usr/bin/env bash

source activate mlp

for MAX_VOCAB in 5000; do
    python W2V.py --MaxVocab $MAX_VOCAB
done