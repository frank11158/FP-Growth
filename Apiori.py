import sys
import numpy as np
import time
from optparse import OptionParser

def parse_args():
    parser = OptionParser()
    parser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename',
                         default="./Data/Data1.data")
    parser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support',
                         default=0.2,
                         type='int')
    parser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence',
                         default=0.3,
                         type='float')
    (options, args) = parser.parse_args()

    if options.input is not None:
            return options
    else:
            print('No specified dataset\n')
            sys.exit('System will exit')

def createC1(dataSet):
    C1 = []
    for transaction in dataSet: # scan all transactions
        for item in transaction: # scan all item in transaction
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for can in Ck:
        for tid in D:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
                # print("ssCnt[can]:", ssCnt[can])
    # print("ssCnt:", ssCnt)
    numItems = float(len(D))
    # print("numItems:", numItems)
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        # print("support:", support)
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList,supportData

# create Ck
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport):
    C1 = createC1(dataSet) # create C1
    # D = map(set,dataSet)
    D = list(map(set, dataSet))
    L1,supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        # print("Ck:", Ck)
        Lk,supK = scanD(D,Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k +=1
    return L,supportData

def generateRules(L, supportData,minConf):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i>1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)    
    return bigRuleList

def rulesFromConseq(freqSet, H, supportData, br1, minConf):
    m = len(H[0])
    if (len(freqSet) >(m +1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if (len(Hmp1) >1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

def calcConf(freqSet,H,supportData, br1, minConf):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet - conseq]
        if conf>= minConf:
            print(freqSet-conseq,"-->",conseq ,"conf:",conf)
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

def createDataSet(filename):
    loadData = np.loadtxt(filename, dtype=np.int)
    transNum = 1
    trans = []
    Data = []
    for line in loadData:
        if (transNum != line[0]):
            Data.append(trans)
            transNum += 1
            trans = []
        trans.append(line[2])
        if np.all(line == loadData[-1]):
            Data.append(trans)
    return Data

if __name__=="__main__":
    options = parse_args()
    filename = options.input
    minSupport = options.minS
    minConfidence = options.minC

    dataSet = createDataSet(filename)
    print(dataSet)
    # parseData = [line.split("; \n") for line in open('./Data/Market_Basket_Optimisation.csv').readlines()]
    # print(parseData)
    
    tStart = time.time()
    L,supportData = apriori(dataSet, minSupport)
    # print("L:", L)
    # print("supportData:", supportData)
    generateRules(L, supportData, minConfidence)
    tEnd = time.time()
    print(tEnd - tStart)