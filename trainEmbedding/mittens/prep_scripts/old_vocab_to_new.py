"""
Generate a file where each line corresponds to a line in vocab2,
listing the index to find the same word in vocab1.
"""

import sys

vocab2ind = {}
with open(sys.argv[1]) as old_vocab_fh:
    for (i, line) in enumerate(old_vocab_fh):
        (word, cnt) = line.strip().split()
        vocab2ind[word] = i

with open(sys.argv[2]) as new_vocab_fh:
    for line in new_vocab_fh:
        (word, cnt) = line.strip().split()
        if word in vocab2ind:
            print(vocab2ind[word])
        else:
            print("")
