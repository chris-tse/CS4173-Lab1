#! /usr/local/bin/python3

import sys

def n_lower_chars(string):
    return sum(1 for char in string if char.islower())

diff = int(sys.argv[1])
text = sys.stdin.read().split()

for word in text:
    num_lower_case = n_lower_chars(word)
    if num_lower_case <= diff and num_lower_case > 0:
        print(word, end=', ')


