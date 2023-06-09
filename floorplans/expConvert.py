# Conversions between postfix and infix notation

from expandFP import isRoot

stack = []
mathOP = {'(': 1, ')': 1, '^': 2, '**': 2, '/': 3,'//': 3, '%': 3, '*': 3,
    '+': 4, '-': 4}
boolOP = {'(': 1, ')': 1, '!': 2, '~': 2, '&': 3, '|': 4}
separator = {','}

def isOperator(op): # checks if op is operator
    return op in mathOP or op in boolOP

def isPreceding(op1, op2): # checks if op2 precedes op1
    types = [mathOP, boolOP]
    for typeOP in types:
        if op1 in typeOP and op2 in typeOP:
            if typeOP[op1] >= typeOP[op2]:
                return True
            return False
    raise TypeError('Operators do not match')

def infixFormat(infix: str): # converts any infix input into a list
    infix = list(filter(lambda x: not x.isspace(), list(infix)))
    fixed = []
    i = j = 0
    while(i < len(infix)):
        if infix[j].isalnum(): # this assumes all operands are alphanums
            j += 1
        elif i == j:
            fixed.append(infix[j])
            i += 1
            j += 1
        else:
            fixed.append(''.join(infix[i:j]))
            i = j
    return fixed

def peEval(pe): # simple algo that converts PE to infix notation
    for e in pe.split():
        if isOperator(e):
            stack.append(f'({stack.pop(-2)} {e} {stack.pop()})')
        else:
            stack.append(e)
    return stack.pop()[1:-1] # remove outer parentheses

def rpnAlgo(infix): # Reverse Polish Notation algo: infix -> postfix
    pe = ''
    infix = infixFormat(infix)
    stack.append('(')
    infix.append(' )')
    for e in infix:
        if e == '(':
            stack.append(e)
        elif e == ')':
            while(stack[-1:][0] != '('):
                pe += f' {stack.pop()}'
            stack.pop() # remove '('
        elif isOperator(e): # operator
            while(isPreceding(e, op := stack[-1:][0]) 
            and op != '('):
                pe += f' {stack.pop()}'
            stack.append(e)
        else: # operand
            pe += f' {e}'
    return pe.lstrip() # remove whitespace on leftmost index

# Dijkstra's Shunting-Yard algo: infix -> postfix
# only one to deal with separators
def syAlgo(infix):
    queue = []
    infix = infixFormat(infix)
    for e in infix:
        if e == '(':
            stack.append(e)
        elif e == ')':
            while(stack[-1:][0] != '('):
                queue.append(stack.pop())
            stack.pop() # remove '('
        elif isOperator(e): # operator
            while(stack and isPreceding(e, op := stack[-1:][0])
            and op != '('):
                queue.append(stack.pop())
            stack.append(e)
        elif e in separator:
            while(stack and stack[-1:][0] != '('):
                queue.append(stack.pop())
        else: # operand
            queue.append(e)
    while(stack):
        queue.append(stack.pop())
    return ' '.join(queue)

def pkrAlgo(infix): # PKR algo: infix -> postfix
    queue = []
    infix = infixFormat(infix)
    for e in infix:
        stack.append(e)
        if e == '(':
            continue
        if e == ')':
            stack.pop() # remove ')'
            while(stack[-1:][0] != '('):
                queue.append(stack.pop())
            stack.pop() # remove '('
        elif isOperator(e):
            if len(stack) > 1 and isOperator(op := stack[-2:-1][0]):
                if isPreceding(e, op) and op != '(':
                    queue.append(stack.pop(-2))
        else: # operand
            queue.append(stack.pop())
    while(stack):
        queue.append(stack.pop())
    return ' '.join(queue)