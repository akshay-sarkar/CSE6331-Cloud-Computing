#!/usr/bin/env python

from operator import itemgetter
import sys,os, time

#current_word = 'Zip'
current_word = 'height'
curr_count = 0
avg = 0.0000
max_age = 0
h1= int(sys.argv[1])
h2= int(sys.argv[2])
zip= int(sys.argv[3])

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    #print (line)
    words = line.split(',')
    word = words[0]
    #age = words[1]
    if word ==  'height':
        try:
            height = words[1]
        except:
            break

    if words[3] == 'zip':
        try:
            z = words[4]
        except:
            break

    try:
        height = int(height)
    except ValueError:
        continue

    try:
        z = int(z)
    except ValueError:
        continue

    if height> h1 and height <h2 and z == zip :
        #max_age = int(age)
        curr_count = curr_count+1
        print(curr_count)

print ('Total \t %s' % (curr_count))