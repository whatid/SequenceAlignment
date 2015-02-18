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

print "seqA " + seqA + "\n", "seqB " + seqB + "\n", lookup_table


def align(seq1, seq2, matrix):
    a = len(seq1)
    b = len(seq2)

    array = [[0 for i in range(a + 1)] for j in range(b + 1)]

    for i in range (0, a + 1):
        array[i][0] = i * gap_penalty
    for j in range (0, b + 1):
        array[0][j] = j * gap_penalty
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            match = array[i-1][j-1] + matrix[seq1[i] + seq2[j]]
            delete = array[i-1][j] + gap_penalty
            insert = array[i][j-1] + gap_penalty
            array[i][j] = max(match, delete, insert)

    aligned_a = ""
    aligned_b = ""

    while a > 0 or b > 0:
        if a > 0 and b > 0 and array[a][b] == array[a-1][b-1] + matrix[seq1[a] + seq2[b]]:
            aligned_a += seq1[a]
            aligned_b += seq2[b]
            a += -1
            b += -1
        if a > 0 and array[a][b] == array[a-1][b] + gap_penalty:
            aligned_a += seq1[a]
            aligned_b += "-"
        if b > 0 and array[a][b] == array[a][b-1] + gap_penalty:
            aligned_a += "-"
            aligned_b += seq2[b]

    print aligned_a + "\n", aligned_b

align(seqA, seqB, lookup_table)