#!/usr/bin/env python

import sys
infile = sys.stdin
next(infile) # skip first line of input file

for line in infile:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split(",")
    print ("%s,%s,%s,%s " % ('Zip', words[10],words[11], words[12]))
--- Reducer.py
#!/usr/bin/env python

from operator import itemgetter
import sys,os, time

#current_word = 'Zip'

curr_count = 0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    #print (line)
    words = line.split(',')
    word = words[0]
    
    zip = words[1]

    try:
        zip = int(zip)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    if zip == 19103:
        curr_count = curr_count+1
        print(curr_count)

print ('Total \t %s' % (curr_count))