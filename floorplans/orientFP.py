# Orients individual rectangles in a floorplan via rotations!

from expandFP import isRoot, getDimensions

# Stockmeyer's algorithm to find optimal orientations between adjacent rectangles
def algorithm(list1, list2, i, j, mergeList, c):
    k = len(list1)
    m = len(list2)
    if c == 1: # reverse the lists for widths so comparsion can work
        list1.reverse()
        list2.reverse()
    while (i<k and j<m):
        mergeList.append([list1[i], list2[j]])
        if list1[i][c] > list2[j][c]:
            i+=1
            continue
        if list1[i][c] < list2[j][c]:
            j+=1
            continue
        if list1[i][c] == list2[j][c]:
            i+=1
            j+=1
            continue
    return mergeList

def getRotateDims(dimensions): # add in dimensional changes via rotations
    for i,dimension in enumerate(dimensions):
        h, w = dimension
        if h==w:
            dimensions[i] = [(h, w)]
        elif h>w:
            dimensions[i] = [(h, w), (w, h)]
        elif h<w:
            dimensions[i] = [(w, h), (h, w)]
    return dimensions

def bindToPE(pe: list, dimStr: str): # binds dimensions to rectangles set by pe
    rotated_dimensions = getRotateDims(getDimensions(dimStr))
    rects = dict()
    for i, char in enumerate(filter(lambda x: not isRoot(x), pe)):
        if isRoot(char):
            continue
        else:
            rects[char] = rotated_dimensions[i]
    return rects

# finds the optimal orientation using eq as a cost function
def evaluate(list3, eq, cut, λ):
    evaluateList = []
    areaList = []
    for i in range(0, len(list3), 1):
        h, w = calculate(list3[i][0], list3[i][1], cut)
        evaluateList.append(eval(eq))
        areaList.append((h, w))
    i = evaluateList.index(min(evaluateList))
    return list3[i], [areaList[i]] # return as list for translate function

# calculates dimensions of enveloping rectangle between rectangles x and y
def calculate(x, y, operator):
    if operator == 0:
        height = max(x[0], y[0])
        width = x[1] + y[1]
    elif operator == 1:
        height = x[0] + y[0]
        width = max(x[1], y[1])
    return height, width

# returns optimal orientations from PE and dimensions
def translate(pe: list, rects: dict, eq: str, p: int):
    i = 0
    orientations = lambda x: x if isinstance(x, list) else rects[x]
    while (len(pe)>1):
        char = pe[i]
        if isRoot(char):
            if char == '*': # vertical slice 
                c = 0
            else: #char == '+', horizontal slice 
                c = 1
            rect1 = orientations(key1 := pe.pop(i-2))
            rect2 = orientations(key2 := pe.pop(i-2))
            mergeList = algorithm(rect1, rect2, 0, 0, [], c)
            dimenList, enveloping = evaluate(mergeList, eq, c, p)
            if not isinstance(key1, list):
                rects[key1] = dimenList[0]
            if not isinstance(key2, list):
                rects[key2] = dimenList[1]
            pe[i-2] = enveloping
            i-=1
        else:
            i+=1
    return pe.pop().pop(), rects

def print_to_console(h, w, rects): # prints to the console
    print("\nOrientations:")
    for rect in rects:
        print(f'Rectangle {rect}: {rects[rect][0]} X {rects[rect][1]}') # given as height x width
    print(f'\nEnveloping rectangle: {h} X {w}\n') # given as height x width
    print(f'Area: {h*w}\n') # given as height x width

'''
pe = normalized Polish Expession representing floorplan
dimStr = string of dimensions in (height, width) format
eq = non-decreasing function ψ using h, w, and λ 
(user-specified parameter) as parameters
'''
def orientFP(pe: str, dimStr: str, eq = '(h*w)+λ*(2*h+2*w)', λ = 0, doPrint = False):
    pe = pe.split()
    rects = bindToPE(pe, dimStr)
    envelopingRect, rects = translate(pe, rects, eq, λ)

    if doPrint:
        print_to_console(*envelopingRect, rects)

    return envelopingRect, rects
