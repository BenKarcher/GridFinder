from latinFinder import find
import numpy as np
from itertools import product


def __wordSetsHelper__(letters, maxSize, words):
    if len(letters) == 0:
        return [[]]
    if maxSize == 1:
        letters = sorted(letters)
        return [[word] for word in words if sorted(word) == letters]
    res = []
    for mask in range(1, 2**len(letters)):
        used = []
        unused = []
        for i, l in enumerate(letters):
            if mask & (1 << i):
                used.append(l)
            else:
                unused.append(l)
        used = sorted(used)
        options = [word for word in words if sorted(word) == used]
        if len(options) > 0:
            remaining = __wordSetsHelper__(unused, maxSize-1, words)
            for option, remaining in product(options, remaining):
                res.append([option]+remaining)
    return res


def wordSets(wordList, letters, blanks):
    prefiltered = [word for word in wordList if len(word) <= len(
        letters) and all(l in letters for l in word)]
    lines = __wordSetsHelper__(letters, blanks+1, prefiltered)
    return [lines[i] for i in range(len(lines)) if lines[i] not in lines[:i]]


def __encodingsHelper__(line, dof, encoding, decoding):
    res = []
    if len(line) == 1:
        for i in range(dof+1):
            res.append([0 for _ in range(i)]+[encoding[l]
                       for l in line[0]]+[0 for _ in range(dof-i)])
        return res
    for i in range(dof+1):
        prefix = [0 for _ in range(i)]+[encoding[l] for l in line[0]]
        res.extend(
            [prefix+[0]+enc for enc in __encodingsHelper__(line[1:], dof-i, encoding, decoding)])
    return res


def encode(lines, letters, blanks):
    encoding = {l: i+1 for i, l in enumerate(set(letters))}
    encoding[" "] = 0
    decoding = {a: b for b, a in encoding.items()}
    encodedLines = []
    for line in lines:
        encodedLines.extend(__encodingsHelper__(
            line, blanks+1-len(line), encoding, decoding))
    encodedLines = [encodedLines[i] for i in range(
        len(encodedLines)) if encodedLines[i] not in encodedLines[:i]]
    encodedLines = np.array(encodedLines)
    return encodedLines, encoding, decoding


def findGrids(encodedList, max):
    res = np.array(find(encodedList, max))
    width = int(res.shape[1]**0.5)
    return res.reshape(res.shape[0], width, width)


def decodeGrid(grid, decoding):
    res = ""
    for row in grid:
        for val in row:
            res += decoding[val]
        res += "\n"
    return res


def printEncodedGrid(grid, decoding):
    for row in grid:
        "".join(decoding[l] for l in row)
