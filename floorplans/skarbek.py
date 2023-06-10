# Provides a binary tree in array representation via Skarbek's algorithm

class ArrayTree:
    def __init__(self, total, index):
        self.l = [None]*total
        self.r = [None]*total
        self.order = index
    def copy(self, other):
        self.l = [x for x in other.l if x != None]
        self.r = [x for x in other.r if x != None]
    def print(self):
        print(f'Iteration {self.order}')
        printing = self.l[:-1] + self.r
        for i,x in enumerate(printing):
            if i==len(printing)/2:
                print()
            print(x, end = ' ')

def visitTree(bTree, n):
    # P3 Find j
    j = 1
    while (bTree.l[j-1]==0):
        bTree.r[j-1] = 0
        bTree.l[j-1] = j+1
        j+=1
        if j>n-1:
            return None
    # P4 Find k and y
    y = bTree.l[j-1]
    k = 0
    while (bTree.r[y-1]>0):
        k = y
        y = bTree.r[y-1]
    # P5 Promote y
    if k>0:
        bTree.r[k-1] = 0
    else:
        bTree.l[j-1] = 0    
    bTree.r[y-1] = bTree.r[j-1]
    bTree.r[j-1] = y
    return bTree

def algorithm(n):
    index = 1
    if n<1:
        bTree = ArrayTree(1,1)
        bTree.l[0] = 0
        bTree.r[0] = 0
        return [bTree]
    else:
        bTree = ArrayTree(n,index)
        bForest = []
        while (bTree != None):
            if (index==1): # P1 initialize
                for k in range(0,n-1,1):
                    bTree.l[k] = k+2
                    bTree.r[k] = 0
                bTree.l[n-1] = bTree.r[n-1] = 0
                bTree.l.append(1)
                doneTree = bTree
            else:
                # P2 visit binary tree
                doneTree = visitTree(bTree, n) 
            if (doneTree!=None):
                bForest.append(doneTree)
            else:
                break
            index+=1
            bTree = ArrayTree(n, index)
            bTree.copy(doneTree)
    return bForest

def skarbek(n, print_to_console = False): # n = # of internal nodes
    ARList = algorithm(int(n))
    if print_to_console:
        for tree in ARList:
            tree.print()
            print('\n')
    return ARList