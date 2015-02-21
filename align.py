__author__ = 'fwirjo'

import sys

try:
    fp1 = open(sys.argv[1], 'r')
    fp2 = open(sys.argv[2], 'r')
    fp3 = open(sys.argv[3], 'r')
    gap_penalty = sys.argv[4]
except IndexError:
    print "Usage: align.py <file1> <file2> <matrix> <gap-penalty>"
    sys.exit(1)


def parsefile(fp):
    seq = ""
    for line in fp:
        line = line.rstrip()
        if line.startswith('>'):
            continue
        seq += line
    return seq


def parse_matrix(fp):
    table = {}
    initial = True
    letters = []
    for line in fp:
        if initial:
            letters = line.split()
            initial = False
            continue
        temp = line.split()
        cur = temp[0]
        for i in range(0, 4):
            table[cur + letters[i]] = int(temp[i+1])

    return table


seqA = parsefile(fp1)
seqB = parsefile(fp2)
lookup_table = parse_matrix(fp3)

#print "seqA " + seqA + "\n", "seqB " + seqB + "\n", lookup_table


def align(seq1, seq2, matrix):
    a = len(seq1)
    b = len(seq2)

    array = [[0 for i in range(b + 1)] for j in range(a + 1)]

    array[0][0] = 0

    # build matrix
    # array is of size [a+1][b+1] to include score for comparison of gap character '-'

    for i in range(1, a + 1):
        array[i][0] = array[i-1][0] + int(gap_penalty)
    for j in range(1, b + 1):
        array[0][j] = array[0][j-1] + int(gap_penalty)

    for i in range(1, a + 1):
        for j in range(1, b + 1):

            # score for a match is added to the previous diagonal score
            match = int(array[i-1][j-1]) + int(matrix[seq1[i-1] + seq2[j-1]])
            delete = int(array[i-1][j]) + int(gap_penalty)
            insert = int(array[i][j-1]) + int(gap_penalty)

            # score in this cell is the max of the three
            array[i][j] = max(match, delete, insert)

    aligned_a = ""
    aligned_b = ""

    # trace back to find optimal alignment of sequences


    while a > 0 or b > 0:
        if a > 0 and b > 0 and array[a][b] == int(array[a-1][b-1]) + int(matrix[seq1[a-1] + seq2[b-1]]):
            aligned_a += seq1[a-1]
            aligned_b += seq2[b-1]
            a -= 1
            b -= 1
        if a > 0 and array[a][b] == int(array[a-1][b]) + int(gap_penalty):
            aligned_a += seq1[a-1]
            aligned_b += "-"
            a -= 1
        if b > 0 and array[a][b] == int(array[a][b-1]) + int(gap_penalty):
            aligned_a += "-"
            aligned_b += seq2[b-1]
            b -= 1

    f = open('output.txt', 'w')
    print >> f, "The optimal alignment between given sequences has score " + str(array[a-1][b-1]) + "\n", aligned_a[::-1] + "\n", aligned_b[::-1]
    f.close()

align(seqA, seqB, lookup_table)