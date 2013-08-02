#!/usr/bin/env python

import nltk
import sys
import re

# docnumber is possibly between 2 and 4 letters followed by at least 6 digits
docnumber = re.compile(r'([A-Za-z]{2,4})?\d{6}\d*')

if len(sys.argv) < 2:
    print 'USAGE: python extract_blocking.py <path to text file>'
    sys.exit()

rawtext = open(sys.argv[1]).read()
if '102' in rawtext or '103' in rawtext:
    print sys.argv[1]
tokens = nltk.word_tokenize(rawtext)
sentences = nltk.sent_tokenize(rawtext)
text = nltk.Text(rawtext)

check102103 = lambda x: '102' in x or '103' in x
checkvalid = lambda x: 'anticipated' in x or 'unpatentable' in x

for sent in sentences:
    if check102103(sent) and checkvalid(sent):
        m = docnumber.search(sent)
        if m:
          print m.group()
