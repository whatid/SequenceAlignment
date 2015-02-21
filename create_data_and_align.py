__author__ = 'fwirjo'

import sys
import random
import os

try:
    length = int(sys.argv[1])
except IndexError:
    print "Usage: create_data_and_align.py <int>"
    sys.exit(1)

# initialize basic random number generator
random.seed()


def base(string_length):
    dna = ""
    for i in range(0, string_length):
        dna += random.choice("ACGT")

    return dna

base_string = base(length)
#print "base string: " + base_string + "\n"


def derived(string, L):
    temp = list(string)
    count = len(temp)
    for i in range(0, int(L/10)):
        position = random.randint(0, count)
        select = random.choice("ab")
        if select == "a":
            temp.pop(position)
            count -= 1
        else:
            temp.insert(position, random.choice("ACGT"))
    return ''.join(temp)

f = open('s1.txt', 'w')
print >> f, ">string1" + "\n" + derived(base_string, length)
f.close()

f = open('s2.txt', 'w')
print >> f, ">string2" + "\n" + derived(base_string, length)
f.close()




