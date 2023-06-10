# Provides a binary tree in array representation via recursion

class ArrayRepesentation:
    def __init__(self, total):
        self.l = [None]*total
        self.r = [None]*total
    def __str__(self):
        line1 = ' '.join([str(n) for n in self.l])
        line2 = ' '.join([str(n) for n in self.r])
        return f'{line1}\n{line2}'
    def translate(self, tree):
        order = tree.data-1
        if order < 0:
            return
        self.l[order] = tree.lchild.data
        self.r[order] = tree.rchild.data
        self.translate(tree.lchild)
        self.translate(tree.rchild)

class Node:
    def __init__(self, preorderNumber):
        self.lchild = self.rchild = None
        self.data = preorderNumber

def getSums(n): # generate paired sums of n
    sums = dict()
    for x in range(0, n+1, 1):
        sums[x] = n-x
    return sums

def enum(n, order): # create binary set of trees
    if n==0:
        return [Node(0)]
    if n==1:
        root = Node(order)
        root.lchild = Node(0)
        root.rchild = Node(0) 
        return [root]
    sumPair = getSums(n-1)
    treeList = []
    for tree in range(0, n, 1):
        leftList = enum(tree, order+1) #key
        rightList = enum(sumPair[tree], order+tree+1) #value
        for i in range(0, len(leftList), 1):
            for j in range(0, len(rightList), 1): 
                root = Node(order)
                root.lchild = leftList[i]
                root.rchild = rightList[j]
                treeList.append(root)
    return treeList

def internalAR(n: int, print_to_console = False): # n = number of internal nodes
    tArray = ArrayRepesentation(n)

    fn = enum(n,1) # pass in 1 as order first
    if print_to_console:
        for i, tree in enumerate(fn):
            tArray.translate(tree) # convert tree to array representation
            print(f'Iteration {i+1}\n{tArray}\n')
    return fn