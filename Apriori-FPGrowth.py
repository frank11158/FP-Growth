# Association Rules Mining: Aprioir Algorithm using FP-Growth

import sys
from itertools import chain, combinations
from optparse import OptionParser
from collections import defaultdict
import numpy as np
import fpTree

def parse_args():
    parser = OptionParser()
    parser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename',
                         default="Test.data")
    parser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support',
                         default=150,
                         type='int')
    parser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence',
                         default=0.6,
                         type='float')
    (options, args) = parser.parse_args()

    if options.input is not None:
            return options
    else:
            print('No dataset filename specified\n')
            sys.exit('System will exit')

def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

def generateRules(freqItemSet, transLength, minConfidence):
    outputFile = open("rules.txt", 'w', encoding = 'UTF-8')
    def getSupport(item):
            return float(freqItemSet[item])/transLength
    for key, val in freqItemSet.items():
        _subsets = map(frozenset, [x for x in subsets(key)])
        for element in _subsets:
            remain = key.difference(element)
            if len(remain) > 0:
                confidence = getSupport(key)/getSupport(element)
                if confidence >= minConfidence:
                    print(tuple(element), "====>", tuple(remain), "confidence:", confidence)
                    outputFile.write(str(tuple(element)))
                    outputFile.write("====>")
                    outputFile.write(str(tuple(remain)))
                    outputFile.write("confidence:%f\n" % confidence)
    outputFile.close()

def createDataSet(filename):
    loadData = np.loadtxt(filename, dtype=np.int)
    transNum = 1
    trans = []
    initDict = {}
    for line in loadData:
        if (transNum != line[0]):
            initDict[frozenset(trans)] = 1
            transNum += 1
            trans = []
        trans.append(line[2])
        if np.all(line == loadData[-1]):
            initDict[frozenset(trans)] = 1
    return initDict


if __name__=="__main__":
    options = parse_args()
    filename = options.input
    minSupport = options.minS
    minConfidence = options.minC
    
    
    # minSupport = 3
    # minConfidence = 0.6
    # simpDat = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
    #            ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
    #            ['socks', 'gloves'],
    #            ['bread', 'milk', 'shoes', 'socks', 'eggs'],
    #            ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
    #            ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # initSet = fpTree.createInitSet(simpDat)
    
    dataSet = createDataSet(filename)
    _fpTree, HeaderTable = fpTree.constructTree(dataSet, minSupport)
    # myFPtree.disp()
    freqItemSet = {}
    fpTree.mineTree(HeaderTable, minSupport, set([]), freqItemSet)
    print(freqItemSet)

    with open("freq.txt", 'w', encoding = 'UTF-8') as f:
        for key in freqItemSet:
            f.write("%s\n" % key)
    f.close()

    generateRules(freqItemSet, len(dataSet), minConfidence)
    