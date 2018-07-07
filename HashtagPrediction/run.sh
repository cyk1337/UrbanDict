#!/usr/bin/env bash

for embedding_index in 0 1 2 3 4 5; do
    python train_cnn.py --i $embedding_index
done