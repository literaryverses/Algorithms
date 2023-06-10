# Generate a normalized Polish Expression based on n slices
# Generate floorplan off of normalized Polish Expression

from random import randint
from copy import copy
from internalAR import Node
from expandFP import Rectangle, isRoot, calculate

def operatorMake(type): # selects operator type
    if type == 0:
        return '*' # vertical slice
    elif type == 1:
        return '+' # horizontal slice

def reGenerate(operand, operator): # recursively generate PE
    if operator == 0:
        return str(operand)
    else:
        if randint(0,1) == 1:
            return f'{operand} \
            {reGenerate(operand+1, operator-1)} \
            {operatorMake(randint(0,1))}'
        else:
            return f'{reGenerate(operand+1, operator-1)} \
            {operand} \
            {operatorMake(randint(0,1))}'
    pass

def normalize(pe): # converts PE to normalized PE
    for i, x in enumerate(peList := pe.split()):
        if isRoot(x) and isRoot(peList[i-1]) and x == peList[i-1]:
            if x == '*': # vertical slice
                peList[i] = operatorMake(1)
            elif x == '+': # horizontal slice
                peList[i] = operatorMake(0)
    return ' '.join(peList)

def getRectangle(node, rects): # get rectangle from node in binary tree
    if isinstance(node, Node): return node.data[1] # internal node
    else: return rects[node] # external node

def setRectangle(node, newRect, rects): # updates node with new rectangle
    if isinstance(node, Node): node.data[1] = newRect # internal node
    else: rects[node] = newRect # external node

def fitRectangle(root, rects): # fits the dimensions of adjacent rectangles
    if not isinstance(root, Node):
        return
    operator = root.data[0]
    lRect = getRectangle(root.lchild, rects)
    rRect = getRectangle(root.rchild, rects)
    if operator == '+': # horizontal slice
        if lRect.width < rRect.width:
            lRect.width = rRect.width
            setRectangle(root.lchild, lRect, rects)
        elif rRect.width < lRect.width:
            rRect.width = lRect.width
            setRectangle(root.rchild, rRect, rects)
    elif operator == '*': # vertical slice
        if lRect.height < rRect.height:
            lRect.height = rRect.height
            setRectangle(root.lchild, lRect, rects)
        elif rRect.height < lRect.height:
            rRect.height = lRect.height
            setRectangle(root.rchild, rRect, rects)
    fitRectangle(root.lchild, rects)
    fitRectangle(root.rchild, rects)

# determines the dimensions of the rectangles via postorder traversal
def rectMake(pe):
    i = 0
    rects = dict()
    bTree = copy(pe).split()
    while (len(bTree)>1):
        char = bTree[i]
        if isRoot(char):
            node = Node(0)
            node.lchild = bTree.pop(i-2)
            node.rchild = bTree.pop(i-2)
            node.data = [char, 
                calculate(getRectangle(node.lchild, rects),
                getRectangle(node.rchild, rects), 
                char)]
            bTree[i-2] = node
            i-=1
        else:
            rects[bTree[i]] = Rectangle(1, 1)
            i+=1
    fitRectangle(bTree[0], rects)
    return rects

def polishExp(n: int): # generates PE from given # of slices
    return reGenerate(0, n) # starts off with 0 operands

def createFP(total, print_to_console = False): # returns random PE and FP given # of slices
    pe = normalize(polishExp(int(total)))
    rects = rectMake(pe)

    if print_to_console:
        print(f'Polish Expression: \n {pe}')
        [print(f'Rectangle {key}:\n\t{value}') for key, value in rects.items()]
    return pe, rects