# Using simulated annealing to find the optimal slicing floorplan
# See D. F. Wong and C. L. Liu, Floorplan Design of VLSI Circuits, Algdorithmica 4 (1989), 263 - 291 for specifics on the algorithm

import math
from expandFP import isRoot
from orientFP import bindToPE, translate, print_to_console
from random import randint, randrange, choice, random
from copy import deepcopy

class Expression:
    def __init__(self, pe: str, dimensions: str):
        self.h = [] # horizontal slice indices
        self.v = [] # vertical slice indices
        self.operands = [] # operand indices
        self.pe = pe.split() # Polish Expression as a list
        self.rects = bindToPE(self.pe, dimensions) # dimensionsclear

        for i, char in enumerate(self.pe):
            if isRoot(char):
                if char == '+':
                    self.h.append(i)
                elif char == '*':
                    self.v.append(i)
            else:
                self.operands.append(i)

    def switch(self, i: int, j: int):
        self.pe[j], self.pe[i] = self.pe[i], self.pe[j]

    def cleanup(self, operator: int, shift: int):
        self.operands.append(operator)
        self.operands.remove(operator+shift)
        if operator in self.h:
            self.h.append(operator+shift)
            self.h.remove(operator)
        elif operator in self.v:
            self.v.append(operator+shift)
            self.v.remove(operator)
    
    def getPE(self) -> str:
        return ' '.join(self.pe)

def chaining(list): # link up consecutive numbers into sublists in a list
    sublist = []
    while list:
        element = list.pop(0)
        if not sublist or sublist[-1] == element-1:
            sublist.append(element)
        else:
            yield sublist
            sublist = [element]
    if sublist: # account for last element
        yield sublist


def move(exp_state): # move from one state to another
    m = randint(1,3)
    operators = exp_state.h + exp_state.v
    operators.sort()
    shift = choice([-1, 1]) # set left (-1) or right (+1)

    if m == 1: # swap two adjacent operands
        operand = randrange(len(exp_state.operands)) # select random operand index
        shift = choice([-1, 1]) # set left (-1) or right (+1)
        if operand == 0:
            shift = 1
        elif operand == len(exp_state.operands)-1:
            shift = -1
        exp_state.switch(exp_state.operands[operand], exp_state.operands[operand + shift])
    
    elif m == 2: # complement a chain of nonzero length
        chain = choice([sublist for sublist in chaining(operators)])
        for index in chain: # range in PE indices
            if exp_state.pe[index] == '+': # horizontal slice
                exp_state.pe[index] = '*'
                exp_state.v.append(index)
                exp_state.h.remove(index)
            elif exp_state.pe[index] == '*': # vertical slice
                exp_state.pe[index] = '+'
                exp_state.h.append(index)
                exp_state.v.remove(index)
            else:
                raise Exception('Operator was input incorrectly in PE')

    elif m == 3: # swap two adjacent operand and operator
        trial = -1 # attempt per operator
        getOperator = (lambda l: choice(l))(operators)
        operator = getOperator
        while (True):
            trial += 1
            if trial == 2: # reset for next operator
                operators.remove(operator)
                trial = 0
            elif trial == 1:
                shift *= -1
            if trial == 0 and operators:
                operator = choice(operators)
            elif not operators: # if there are no operators left
                break
            if not 0 <= operator + shift < len(exp_state.pe):
                continue # out of index, jump to next loop
            if isRoot(exp_state.pe[operator + shift]):
                continue # points to operator and not operand, jump to next loop                
            new_pe = [char for char in exp_state.pe]
            new_pe[operator], new_pe[operator + shift] = new_pe[operator + shift], new_pe[operator]
            if isNormalized(new_pe) and balloting_property(new_pe):
                exp_state.pe = new_pe # select if PE is normalized and satisfy balloting property
                exp_state.cleanup(operator, shift) # attenue lists to match PE
                break
    return exp_state

def isNormalized(pe: list) -> bool: # checks if PE is normalized (no consecutive operators)
    for i,char in enumerate(pe):
        if isRoot(char) and char == pe[i-1]:
            return False
    return True

def balloting_property(pe: list) -> bool: # checks if PE satisfies balloting property (operands > operators)
    operator_count = 0
    for i,char in enumerate(pe):
        if isRoot(char):
            operator_count += 1
            if 2 * operator_count > i:
                return False
    return True

def cost(exp_state, eq, λ): # determines cost of new state
    h, w = translate([e for e in exp_state.pe], deepcopy(exp_state.rects), eq, λ)[0] # height and width
    return eval(eq)

def get_init_temp(exp_state, p, n, eq, λ): # calculates initial temperature
    init_temp_arr = []
    oldCost = cost(exp_state, eq, λ)
    for _ in range(n): # calculate avg from uphill moves
        newCost = cost(move(exp_state), eq, λ)
        if newCost > oldCost:
            init_temp_arr.append(newCost-oldCost)
        oldCost = newCost
    try:
        diffAvg = sum(init_temp_arr)//len(init_temp_arr)
    except ZeroDivisionError:
        print('Given expression is optimal enough')
    return -diffAvg/math.log(p)

def simulatedAnnealing(exp, p, e, r, k, eq = '(h*w)+λ*(2*h+2*w)', λ = 0): # simulated annealing algo
    best_state = exp_state = exp # initial state
    mt = uphill = reject = 0
    n = k*len(best_state.operands)
    t = get_init_temp(deepcopy(exp), p, n, eq, λ)
    while (True):
        mt = uphill = reject = 0
        while (uphill <= n) and (mt <= 2*n):
            new_state = move(deepcopy(exp_state))
            mt += 1 # count total moves
            newCost = cost(new_state, eq, λ)
            diffC = newCost - cost(exp_state, eq, λ) # calculate cost difference
            if (diffC <= 0) or (random() < math.pow(math.e, -diffC/t)):
                if (diffC > 0): 
                    uphill += 1
                exp_state = new_state
                if newCost < cost(best_state, eq, λ): 
                    best_state = exp_state # optimal state
            else:  
                reject += 1
        t *= r #reduce temperature
        if (reject/mt > 0.95) or (t < e): # TODO: add Timeout
            break
    return best_state

def optimalFP(pe: str, dimStr: str, doPrint = False):
    exp = Expression(pe, dimStr) # create expression object

    # MODIFIABLE VARIABLES
    p = 0.85 # initial probability for deciding starting temp
    e = 0.0001 # minimum temperature until annealing is performed
    r = 0.85 # temperature reducing factor, 0.85 has 'very satisfactory results'
    k = 5 # number of iterations per temp, keep between 5 - 10
    eq = '(h*w)+λ*(2*h+2*w)' # cost function; h = height and w = width
    λ = 0 # user-specified parameter for cost function, default = 0

    best = simulatedAnnealing(exp, p, e, r, k, eq, λ)
    new_pe = best.getPE()
    if doPrint:
        print(f'\nNew Polish Expression: {new_pe}')
    (roomHeight, roomWidth), best.rects = translate(new_pe.split(), best.rects, eq, λ)
    print_to_console(roomHeight, roomWidth, best.rects)

    # returns PE (str), enveloping area (int x int), and PE (Expression obj)
    return new_pe, (roomHeight, roomWidth), best