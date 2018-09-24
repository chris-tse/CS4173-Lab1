#! /usr/local/bin/python3

import sys
import re

wordlist = list(map(str.lower, sys.stdin.read().split()))
target = sys.argv[1]

def replace_with_dot(c):
    if c.islower():
        return '.'
    else:
        return c

pattern = ''.join(list(map(replace_with_dot, target)))

for word in wordlist:
    m = re.match(pattern, word, re.IGNORECASE)
    if m != None:
        print(m.group(0))