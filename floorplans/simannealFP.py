# Using simulated annealing to generate slicing floorplans
# See D. F. Wong and C. L. Liu, Floorplan Design of VLSI Circuits, Algdorithmica 4 (1989), 263 - 291 for specifics on the algorithm

import math
from expandFP import isRoot
from orientFP import bindToPE, translate
from random import randint, randrange, choice, sample
from copy import deepcopy

class Expression:
    def __init__(self, pe: str, dimensions: str):
        self.h = [] # horizontal slice indices
        self.v = [] # vertical slice indices
        self.operands = [] # operand indices
        self.rects = bindToPE(pe, dimensions) # dimensions

        self.pe = pe.split()
        for i, char in enumerate(self.pe):
            if isRoot(char):
                if char == '+':
                    self.h.append(i)
                elif char == '*':
                    self.v.append(i)
            else:
                self.operands.append(i)

    def switch(self, i: int, j: int, copify: bool) -> list:
        exp = self.pe
        if copify == True:
            exp = deepcopy(self.pe)
        exp[j], exp[i] = exp[i], exp[j]
        return exp

def move(exp_state, m): # move from one state to another
    operators = exp_state.h + exp_state.v
    operators.sort()
    shift = choice([-1, 1]) # set left (-1) or right (+1)

    if m == 1: # swap two adjacent operands
        shift = choice([-1, 1]) # set left (-1) or right (+1)
        operand = randrange(len(exp_state.operands)) # select random operand index
        shift = choice([-1, 1]) # set left (-1) or right (+1)
        if operand == 0:
            shift = 1
        elif operand == len(exp_state.operands)-1:
            shift = -1
        exp_state.switch(exp_state.operands[operand], exp_state.operands[operand + shift], False)
    
    elif m == 2: # complement a chain of nonzero length
        chain = sample(range(len(operators)), 2) # range in operator indices
        chain.sort()
        for i in range(chain[0], chain[1]): # range in PE indices
            if exp_state.pe[i] == '+': # horizontal slice
                exp_state.pe[i] = '*'
                exp_state.v.append(i)
                exp_state.h.remove(i)
            elif exp_state.pe[i] == '*': # vertical slice
                exp_state.pe[i] = '+'
                exp_state.h.append(i)
                exp_state.v.remove(i)
            else:
                raise Exception('Operator was input incorrectly')

    elif m == 3: # swap two adjacent operand and operator
        trial = -1 # attempt per operator
        executions = [operator := choice(operators), shift := shift * -1, operators.remove(operator)]
        while (True):
            trial += 1
            executions[trial]
            if trial == 2: # reset for next operator
                trial = 0
                continue
            if not 0 <= operator + shift < len(exp_state.pe):
                continue # out of index, jump to next loop
            new_pe = [char for char in exp_state.pe]
            new_pe[operator], new_pe[operator + shift] = new_pe[operator + shift], new_pe[operator]
            if isNormalized(new_pe) and balloting_property(new_pe):
                exp_state.pe = new_pe # select if PE is normalized and satisfy balloting property
                break
    return exp_state

def isNormalized(pe: list) -> bool: # checks if PE is normalized (no consecutive operators)
    for i,char in enumerate(pe):
        if isRoot(char) and char == pe[i-1]:
            return False
    return True

def balloting_property(pe: list) -> bool: # checks if PE satisfies balloting property (operands > operators)
    operator_count = operand_count = 0
    for char in pe:
        if isRoot(char):
            operator_count += 1
        else:
            operand_count += 1
        if operand_count <= operator_count:
            return False
    return True

def cost(exp_state, λ): # determines cost of new state
    eq = '(h*w)+p*(2*h+2*w)' # cost function
    h, w = translate(' '.join(exp_state.pe), exp_state.rects.copy(), eq, λ)[0] # height and width
    return eval(eq)

'''
p = cooling ratio
e = minimum temperature
k = limits the moves tried
k = number of iterations (limits runtime)
λ = user-specified parameter for cost function - default is 0
'''
def simulatedAnnealing(exp, p, e, r, k, λ = 0): # simulated annealing algo
    best = exp_state = exp # initial state
    mt = uphill = 0
    n = k*len(best.operands)
    t = 1 #4406.6/math.log(p) #diffAvg/math.log(p) proofreading
    while (True):
        mt = uphill = reject = 0
        while (True):
            new_state = move(deepcopy(exp_state), randint(1,3))
            mt +=1
            diffE = cost(new_state, λ) - cost(exp_state, λ)
            if (diffE <= 0 or p < math.pow(math.e, -diffE/t)):
                if (diffE > 0): uphill += 1
                exp_state = new_state
                if cost(exp_state, λ) < cost(best, λ): 
                    best = exp_state
            else:  reject += 1
            if (uphill > n or mt > 2*n): break
        t *= r #reduce temperature
        if (reject/mt > 0.95 or t < e): break
        #print(cost(best))
    return best

#-main------
r = 0.85 # between 
k = 5 # between 5 - 10, moves per temp
p = 0.5 # probability comparison
e = 0.001 # when temp is too low
λ = 0 # user-specified parameter

'''
pe = input("Input a reverse Polish expression >>")
rectangles = input("input rectangles")
exp = Expression(pe, rectangles)
simulatedAnnealing(exp, p, e, r, k)
'''
#pe = 'f g j h c v h a v b h d h e v'
pe = '16 0 10 30 43 33 v 34 h 15 h 6 9 h 5 41 11 v h 25 v 13 v 46 45 v h 3 v 29 v h v h v 31 36 1 12 h 49 h 35 28 v 37 v 17 42 8 h 39 h v 27 v 23 v 44 v h v h 2 h 7 h v h 38 h 20 h v h 32 40 h 47 h 48 26 24 h v h 21 h 14 h v 18 22 v 19 v h 4 v'

#rectangles = '(4, 6), (4, 3), (4, 1), (2, 3), (1, 1), (1, 2), (3, 3), (3, 4)'
rectangles = "(9, 9), (1, 9), (6, 9), (4, 9), (7, 9), (3, 10), (1, 10), (2, 10), (1, 18), (2, 18), (8, 5), (1, 8), (9, 8), (9, 3), (9, 5), (9, 2), (8, 2), (7, 2), (8, 3), (8, 4), (1, 7), (5, 7), (6, 7), (4, 7), (8, 6), (8, 7), (8, 8), (6, 4), (6, 2), (1, 6), (6, 3), (6, 5), (6, 6), (7, 7), (7, 3), (1, 5), (2, 5), (3, 5), (4, 5), (3, 4), (2, 4), (1, 4), (4, 4), (5, 5), (2, 3), (2, 2), (3, 3), (3, 1), (2, 1), (1, 1)"
exp = Expression(pe, rectangles)
best = simulatedAnnealing(exp, 0, e, r, k)

for i in range(0, 10, 1):
    print(f'{i}: ')
    pe = ' '.join(best.pe)
    print(pe)
    #print(orientFP(pe, best.rects))