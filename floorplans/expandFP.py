# Calculates the overall height and width of a slicing floorplan

from re import compile

class Rectangle:
    def __init__(self, height, width):
        self.width = width
        self.height = height
    def __str__(self):
        return f'Height: {self.height}, Width: {self.width}'

def isRoot(operator):
    if operator == '*': return True # vertical slice 
    elif operator == '+': return True # horizontal slice
    else: return False

def getDimensions(dimStr): # extract dimensions from string
    dimensions = []
    dimRegex = compile(r'\d+,\d+|\d+, \d+')
    for dim in dimRegex.findall(dimStr):
        if dim[dim.index(',')+1].isdigit():
            h, w = [int(x) for x in dim.split(',')]
            dimensions.append((h,w))
        else:
            h, w = [int(x) for x in dim.split(', ')]
            dimensions.append((h,w))
    return dimensions

def castFromPE(pe, dimensions): # cast dimensions onto PE operands
    modules = dict()
    for i, char in enumerate(filter(lambda x: not isRoot(x), pe.split())):
        if isRoot(char):
            continue
        else:
            modules[char] = Rectangle(dimensions[i][0], dimensions[i][1])
    return modules

def calculate(x, y, operator): # calculate new rectangle via operator
    height = width = 0
    if operator == '*': # vertical slice 
        height = max(x.height, y.height)
        width = x.width + y.width
    elif operator == '+': # horizontal slice 
        height = x.height + y.height
        width = max(x.width, y.width)
    return Rectangle(height, width)
    
def translate(pe, modules): # finds final rectangle from PE
    i = 0
    pe = pe.split()
    while (len(pe)>1):
        char = pe[i]
        if isRoot(char):
            pe[i-2] = calculate(pe.pop(i-2), pe.pop(i-2), char)
            i-=1
        else:
            pe[i] = modules[pe[i]]
            i+=1
    return pe[0]

# Returns the height of width of floorplan given a PE and dimensions
def expandFP(pe, dimensions):
    answer = translate(pe, castFromPE(pe, dimensions))
    return answer.height, answer.width