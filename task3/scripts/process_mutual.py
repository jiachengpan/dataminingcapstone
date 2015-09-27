#! /usr/bin/env python2

import sys

mutualInfo = {}
with open(sys.argv[1]) as fh:
    for line in fh.readlines():
        w1, w2, mi = line.split('\t')
        if w1 == w2: continue

        mi = float(mi)
        key = ':::'.join(sorted((w1, w2)))

        if key in mutualInfo:
            mi = (mutualInfo[key] > mi) and mutualInfo[key] or mi
        mutualInfo[key] = mi

result = sorted(mutualInfo.items(), key=lambda d: d[1])

print result[:10]
print '-----'
print result[-10:]

