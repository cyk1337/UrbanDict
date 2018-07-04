#!/usr/bin/python
from collections import defaultdict
import json
import os
import argparse
import gzip
import sys
import codecs
from time import asctime

verbose = True

def log(s):
    print >> sys.stderr, s
def verblog(s):
    if verbose:
        log(s)

def processfile(path, fname):
    fh = None
    destname = ''
    fullpath = os.path.join(path, fname)
    if fname.startswith('.') or not os.path.isfile(fullpath):
        return
    verblog(fname)

    f = codecs.open(fullpath, 'r', encoding='utf-8')
    if fname.endswith('.gz'):
        f.close()
        f = gzip.open(fullpath, 'rb', encoding='utf-8')

    for line in f:
        yield line
    f.close()

def traversedocs(rootdir):
    for path, subdirs, files in os.walk(rootdir):
        verblog("%s - traversing %s" % (asctime(), path))
        for fname in files:
            for line in processfile(path, fname):
                yield line

def concatenate_main():
    parser = argparse.ArgumentParser(description='munge twitter')
    parser.add_argument('--rootdir')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    verbose = args.verbose
    args.rootdir.rstrip('/')

    for line in traversedocs(args.rootdir):
        yield line

if __name__ == '__main__':
    for line in concatenate_main():
        print line
