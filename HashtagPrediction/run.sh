#!/usr/bin/env bash

source activate mlp

ii=3


for embedding_index in 0 1 2 3 4 5; do
    python train_cnn.py --i $embedding_index --embedding $ii
done
