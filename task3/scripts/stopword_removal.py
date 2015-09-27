#! /usr/bin/env python2

import sys

from nltk.corpus import stopwords

stop = stopwords.words('english')
with open(sys.argv[1]) as fh:
    for line in fh.readlines():
        print ' '.join([i.lower() for i in line.split() if i.lower() not in stop])
