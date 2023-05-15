# Generates letters (5x5) within a 7x7 frame

from objects import Grid
from random import sample

def alphabet(phrase: str):
    coord_letters = []
    coord_holes = []
    y,x = 1,1 # set original coordinates
    
    for letter in phrase.upper():
        if letter == 'A':
            for _x in range(x+0, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
            for _y in range(y+3, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            for _y in range(y+1, y+2):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            coord_holes.append((y+1, x+1))
        if letter == 'B':
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
            for _x in range(x+1, x+5):
                coord_letters.append((y+4, _x))
                coord_letters.append((y+2, _x))
            coord_letters.append((y+1, x+2))
            coord_letters.append((y+3, x+4))
            coord_letters.append((y, x+1))
            coord_letters.append((y, x+2))
            coord_holes.append((y+3, x+1))
        if letter == 'C':
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
            for _x in range(x+1, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+4, _x))
            coord_letters.append((y+3, x+4))
            coord_letters.append((y+1, x+4))
        if letter == 'D':
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
            for _x in range(x+1, x+4):
                coord_letters.append((y, _x))
                coord_letters.append((y+4, _x))
            for _y in range(y+1, y+4):
                coord_letters.append((_y, x+4))
            coord_letters.append((y+1, x+3))
            coord_letters.append((y+3, x+3))
            coord_holes.append((y+1, x+1))
        if letter == 'E':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
                coord_letters.append((y+4, _x))
            coord_letters.append((y+1, x))
            coord_letters.append((y+3, x))
        if letter == 'F':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
            coord_letters.append((y+1, x))
            coord_letters.append((y+3, x))
            coord_letters.append((y+4, x))
        if letter == 'G':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+4, _x))
            for _y in range(y+2, y+4):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            coord_letters.append((y+1, x))
            coord_letters.append((y+2, x+3))
        if letter == 'H':
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            for _x in range(x+1, x+5):
                coord_letters.append((y+2, _x))
        if letter == 'I':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+4, _x))
            for _y in range(y+1, y+5):
                coord_letters.append((_y, x+2))
        if letter == 'J':
            for _x in range(x, x+4):
                coord_letters.append((y, _x))
                coord_letters.append((y+4, _x))
            for _y in range(y+1, y+5):
                coord_letters.append((_y, x+3))
            coord_letters.append((y, x+4))
            coord_letters.append((y+3, x))
        if letter == 'K':
            for _y in range(y, y+3):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+2))
            for _y in range(y+3, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
                coord_letters.append((_y-1, x+3))
            coord_letters.append((y+2, x+1))
            coord_letters.append((y, x+3))
        if letter == 'L':
            for _x in range(x, x+5):
                coord_letters.append((y+4, _x))
            for _y in range(y, y+4):
                coord_letters.append((_y, x))
        if letter == 'M':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
            for _y in range(y+1, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+2))
                coord_letters.append((_y, x+4))
        if letter == 'N':
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            #for _y in range(y, y+2):
            for _y in range(y+1, y+3):
                coord_letters.append((_y, x+1))
                coord_letters.append((_y+1, x+2))
                coord_letters.append((_y+2, x+3))
        if letter == 'O':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+4, _x))
            for _y in range(y+1, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            coord_holes.append((y+1, x+1))
        if letter == 'P':
            for _x in range(x+1, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
            coord_letters.append((y+1, x+4))
            coord_holes.append((y+1, x+1))
        if letter == 'Q':
            for _x in range(x, x+4):
                coord_letters.append((y, _x))
                coord_letters.append((y+3, _x))
            for _y in range(y+1, y+3):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+3))
            coord_letters.append((y+4, x+3))
            coord_letters.append((y+4, x+4))
            coord_holes.append((y+1, x+1))
        if letter == 'R':
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
            for _x in range(x+1, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
            coord_letters.append((y+1, x+4))
            for _x in range(x+2, x+5):
                coord_letters.append((y+4, _x))
            coord_letters.append((y+3, x+2))
            coord_holes.append((y+1, x+1))
        if letter == 'S':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
                coord_letters.append((y+4, _x))
            coord_letters.append((y+1, x))
            coord_letters.append((y+3, x+4))
        if letter == 'T':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
            for _y in range(y+1, y+5):
                coord_letters.append((_y, x+2))
        if letter == 'U':
            for _x in range(x, x+4):
                coord_letters.append((y+4, _x))
            for _y in range(y, y+5):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
        if letter == 'V':
            for _y in range(y, y+3):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            for _y in range(y+2, y+4):
                coord_letters.append((_y, x+1))
                coord_letters.append((_y+1, x+2))
                coord_letters.append((_y, x+3))
        if letter == 'W':
            for _x in range(x+1, x+5):
                coord_letters.append((y+4, _x))
            for _y in range(y, y+4):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+2))
                coord_letters.append((_y, x+4))
        if letter == 'X':
            for _y in range(y, y+2):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
                coord_letters.append((_y+3, x))
                coord_letters.append((_y+3, x+4))
            for _y in range(y+1, y+4):
                coord_letters.append((_y, x+1))
                coord_letters.append((_y, x+3))
            coord_letters.append((y+2, x+2))
        if letter == 'Y':
            for _y in range(y, y+2):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            for _x in range(x, x+5):
                coord_letters.append((y+2, _x))
                coord_letters.append((y+4, _x))
            coord_letters.append((y+3, x+4))
        if letter == 'Z':
            for _x in range(x, x+5):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x))
                coord_letters.append((y+4, _x))
            coord_letters.append((y+1, x+4))
            coord_letters.append((y+3, x))
        if letter == '?':
            for _x in range(x+1, x+4):
                coord_letters.append((y, _x))
                coord_letters.append((y+2, _x+1))
            for _y in range(y, y+2):
                coord_letters.append((_y, x))
                coord_letters.append((_y, x+4))
            coord_letters.append((y+4, x+2))
        if letter == '!':
            for _y in range(y, y+3):
                coord_letters.append((_y, x+2))
            coord_letters.append((y+4, x+2))
        if letter == '.':
            coord_letters.append((y+4, x+2))
        if letter == '\n': # space operates as newline
            x = -5; y += 6 # reset pointer
        x+=6 # increment for next word
    return coord_letters, coord_holes

def mask_word(phrase: str):
    words = phrase.split('\n')
    total_rows = 6 * len(words) + 1
    total_cols = 6 * len(max(words, key = len)) + 1
    grid = Grid(total_rows,total_cols)
    coord_mask, coord_holes = alphabet(phrase)
    for coord in coord_mask:
        grid.mask(coord[0], coord[1])
    grid = recursive_backtracker(grid, None)
    for coord in coord_holes:
        recursive_backtracker(grid, coord)
    return grid

def recursive_backtracker(grid, coord):
    stack = []
    if not coord:
        stack.append(grid.getRandom())
    else:
        stack.append(grid.getCell(coord[0],coord[1]))
    while stack:
        cell = stack[-1]
        neighbors = [n for n in cell.getNeighbors() if not n.getLinks()]

        if neighbors:
            neighbor = sample(neighbors,1)[0]
            cell.link(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()
    return grid

words = 'hello world!' # write anything to print on maze
print(mask_word(words))