__author__ = 'fwirjo'

import sys
try:
    length = sys.argv[1]
except IndexError:
    print "Usage: create_data_and_align.py <int>"
    sys.exit(1)

