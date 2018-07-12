#!/usr/bin/env bash

source activate mlp

for embedding_index in 0; do
    python train_cnn.py --i $embedding_index
done