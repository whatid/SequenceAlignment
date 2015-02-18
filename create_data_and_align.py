__author__ = 'fwirjo'

import sys
import random
try:
    length = int(sys.argv[1])
except IndexError:
    print "Usage: create_data_and_align.py <int>"
    sys.exit(1)

# initialize basic random number generator
random.seed()


def generate(string_length):
    dna = ""
    for i in range(0, string_length):
        dna += random.choice("ACGT")

    print dna
    return

generate(length)