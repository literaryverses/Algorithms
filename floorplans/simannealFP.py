# Using simulated annealing to generate slicing floorplans
# See D. F. Wong and C. L. Liu, Floorplan Design of VLSI Circuits, Algdorithmica 4 (1989), 263 - 291 for specifics on the algorithm

import expandFP, orientFP, math
from random import randint, choice
from copy import deepcopy

class Expression:
    def __init__(self, pe, dimensions):
        self.h = []
        self.v = []
        self.operands = []
        self.dimensions = dimensions

        self.pe = pe.split()
        for i, char in enumerate(self.pe):
            if expandFP.isRoot(char):
                if char == '+':
                    self.h.append(i)
                elif char == '*':
                    self.v.append(i)
            else:
                self.operands.append(i)

    def switch(self, i, j, copify) -> list:
        exp = self.pe
        if copify == True:
            exp = deepcopy(self.pe)
        exp[j], exp[i] = exp[i], exp[j]
        return exp

def move(exp_state, m):
    operators = exp_state.h + exp_state.v
    operators.sort()
    operand = randint(0, len(exp_state.operands)-1) # select random operand

    if m == 1: # swap two adjacent operands
        shift = choice([-1, 1]) # set left (-1) or right (+1)        
        if operand == 0: 
            shift = 2
        elif operand == len(exp_state.operands)-1: 
            shift = 0

        exp_state.switch(exp_state.operands[operand], exp_state.operands[operand + shift], False)
    elif m == 2: # complement a chain of nonzero length
        chain_start = [operators[0]]
        chain_max = len(operators)
        for i in range(chain_max-1, 0, -1):
            if operators[i-1] != operators[i]-1:
                chain_start.append(operators[i])
    
        chain = chain_start[randint(0, len(chain_start)-1)]

        for i in range(chain, chain_max, 1):        
            if i > len(exp_state.rpe): break
            elif exp_state.rpe[i] == 'h':
                exp_state.rpe[i] = 'v'
                exp_state.v.append(i)
                exp_state.h.pop(exp_state.h.index(i))
            elif exp_state.rpe[i] == 'v':
                exp_state.rpe[i] = 'h'
                exp_state.h.append(i)
                exp_state.v.pop(exp_state.v.index(i))
            else: break
    else: # m == 3 # swap two adjacent operand and operator
        while (True):
            m = randint(1,4)

            if m<3: operators = exp_state.h
            else: operators = exp_state.v
            if m%2 == 0: m = -1 # set direction of adjacency
            else: m = 1

            operator = randint(0, len(operators)-1)
            
            if operator == 0: m = 1
            elif operator == len(operators)-1: m = -1
            operatorI = operators[operator]

            if (operatorI+m in exp_state.operands): # operator next to operand?
                operand = exp_state.operands.index(operatorI+m)
            else: 
                continue
            operandI = exp_state.operands[operand]
            
            if exp_state.rpe[operatorI+2*m] == exp_state.rpe[operatorI]: # operator not adjacent to same type?
                continue

            newExp = exp_state.switch(operatorI, operandI, True)
            if isSkewed(newExp):
                exp_state.rpe = newExp
                exp_state.operands.pop(operand)
                operators.append(operandI)
                operators.pop(operator)
                exp_state.operands.append(operatorI)
                break
            else:
                continue

    return exp_state

def isSkewed(rpeList): # checks if rpe is a skewed slicing floorplan
    i = 0
    test = deepcopy(rpeList)
    while (len(test)>1): # checks if sequence works
        operator = test[i]
        if expandFP.isRoot(operator):
            if i-2 < 0: 
                return False
            test.pop(i-2)
            test.pop(i-2)
            test[i-2] = '1'
            i-=1
        else: i+=1

    for i in range(len(rpeList)-1): # check if skewed
        if rpeList[i] == rpeList[i+1]:
            return False
    return True

def cost(exp_state):
    h, w = orientFP.orientFP(' '.join(exp_state.rpe), exp_state.dimensions, 'h*w', False)[0]
    return h * w

def neighborhood(exp_state):
    exp_state = move(exp_state, randint(1,3))
    return exp_state

def simulatedAnnealing(initial_state, p, e, r, k):
    best = exp_state = initial_state
    mt = uphill = 0
    n = k*len(best.operands)
    t = 1 #4406.6/math.log(p) #diffAvg/math.log(p) proofreading
    while (True):
        mt = uphill = reject = 0
        while (True):
            new_state = neighborhood(deepcopy(exp_state))
            mt +=1
            diffCost = cost(new_state) - cost(exp_state)
            if (diffCost<= 0 or p < math.pow(math.e, -diffCost/t)):
                if (diffCost > 0): uphill += 1
                exp_state = new_state
                if cost(exp_state) < cost(best): 
                    best = exp_state
                    print(cost(best)) #proofreading
            else:  reject += 1
            if (uphill > n or mt > 2*n): break
        t *= r #reduce temperature
        if (reject/mt > 0.95 or t < e): break
        #print(cost(best))
    return best

#-main-------
r = 0.85 # between 
k = 5 # between 5 - 10, moves per temp
p = 0.5 # probability comparison
e = 0.001 # when temp is too low
'''
rpe = input("Input a reverse Polish expression >>")
rectangles = input("input rectangles")
exp = Expression(rpe, rectangles)
simulatedAnnealing(exp, p, e, r, k)
'''
#rpe = 'f g j h c v h a v b h d h e v'
rpe = '16 0 10 30 43 33 v 34 h 15 h 6 9 h 5 41 11 v h 25 v 13 v 46 45 v h 3 v 29 v h v h v 31 36 1 12 h 49 h 35 28 v 37 v 17 42 8 h 39 h v 27 v 23 v 44 v h v h 2 h 7 h v h 38 h 20 h v h 32 40 h 47 h 48 26 24 h v h 21 h 14 h v 18 22 v 19 v h 4 v'

#rectangles = '(4, 6), (4, 3), (4, 1), (2, 3), (1, 1), (1, 2), (3, 3), (3, 4)'
rectangles = "(9, 9), (1, 9), (6, 9), (4, 9), (7, 9), (3, 10), (1, 10), (2, 10), (1, 18), (2, 18), (8, 5), (1, 8), (9, 8), (9, 3), (9, 5), (9, 2), (8, 2), (7, 2), (8, 3), (8, 4), (1, 7), (5, 7), (6, 7), (4, 7), (8, 6), (8, 7), (8, 8), (6, 4), (6, 2), (1, 6), (6, 3), (6, 5), (6, 6), (7, 7), (7, 3), (1, 5), (2, 5), (3, 5), (4, 5), (3, 4), (2, 4), (1, 4), (4, 4), (5, 5), (2, 3), (2, 2), (3, 3), (3, 1), (2, 1), (1, 1)"

exp = Expression(rpe, rectangles)
best = simulatedAnnealing(exp, 0, e, r, k)

for i in range(0, 10, 1):
    print('%d:' % i)
    pe = ' '.join(best.rpe)
    print(pe)
    print(orientFP.orientFP(pe, best.dimensions, 'h*w', False))