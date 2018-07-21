#!/usr/bin/env bash

source activate mlp

for wiki in 0 1;do
for i in 1 2 3 4;do
python calcMAP.py --embedding $i --wiki $wiki
done
done