#!/usr/bin/env python

import sys
infile = sys.stdin
next(infile) # skip first line of input file
# input comes from STDIN (standard input)
for line in infile:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split(",")
    print ("%s,%s,%s,%s" % ('height', words[37],'zip', words[10]))