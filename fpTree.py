# FP-Growth: FP-Tree

class TreeNode:
    def __init__(self, name, numOccur, parentNode):
        self.name = name
        self.cnt = numOccur
        self.parent = parentNode
        self.children = {}
        self.next = None

    def inc(self, numOccur):
        self.cnt += numOccur

    # def disp(self, ind = 1):
    #     print("  " * ind, self.name, "  ", self.cnt)
    #     for child in self.children.values():
    #         child.disp(ind+1)

def constructTree(dataset, minsupport):
    # create header table
    headerTable = createHeaderTable(dataset, minsupport)
    if len(headerTable) == 0: return None, None
    fpTree = TreeNode('Null Set', 1, None)

    # scan over dataset, construct FP-tree
    for transaction, cnt in dataset.items():
        itemsIsFreq = {}
        for item in transaction:
            if item in headerTable.keys():
                itemsIsFreq[item] = headerTable[item][0]
        if len(itemsIsFreq) > 0:
            updateTree = fpTree
            for item in [v[0] for v in sorted(itemsIsFreq.items(), key=lambda p:p[1], reverse=True)]:
                if item in updateTree.children:
                    updateTree.children[item].inc(cnt)
                else:
                    updateTree.children[item] = TreeNode(item, cnt, updateTree)
                    if headerTable[item][1] == None:
                        headerTable[item][1] = updateTree.children[item]
                    else:
                        updateHeader(headerTable[item][1], updateTree.children[item])
                updateTree = updateTree.children[item]
    return fpTree, headerTable

def createHeaderTable(dataset, minsupport):
    headerTable = {}
    for transaction in dataset:
        for item in transaction:
            # headerTable[item] = headerTable.get(item, 0) + 1 =====> ???
            headerTable[item] = headerTable.get(item, 0) + dataset[transaction]
    for k in list(headerTable):
        if headerTable[k] < minsupport:
            del headerTable[k]
        else: 
            headerTable[k] = [headerTable[k], None] # add a pointer to simalar item
    return headerTable

def updateHeader(node, target):
    while (node.next != None):
        node = node.next
    node.next = target

def traverseUp(startNode, prefixPath):
    while startNode.parent != None:
        prefixPath.append(startNode.name)
        startNode = startNode.parent

def findPrefixPath(basePattern, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        traverseUp(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.cnt
        treeNode = treeNode.next
    return condPats

def mineTree(headerTable, minSupport, preFix, freqItemSet):
    itemList = [v[0] for v in sorted(headerTable.items(), key = lambda p:p[1][0])]
    if(len(itemList) == 0): return
    for basePattern in itemList:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePattern)
        freqItemSet[frozenset(newFreqSet)] = headerTable[basePattern][0]
        condPatternBases = findPrefixPath(basePattern, headerTable[basePattern][1])
        
        # TODO: debug, for constructed tree's ambiguity
        if(condPatternBases != {}):
            condFPtree,condHeaderTable = constructTree(condPatternBases, minSupport)
            if condHeaderTable != None:
                mineTree(condHeaderTable, minSupport, newFreqSet, freqItemSet)

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict