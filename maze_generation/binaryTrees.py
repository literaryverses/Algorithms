from random import randint
from objects import Cell, Grid

class BinaryTree: # Binary Tree Algorithm
    def __init__(self, grid):
        for cell in grid.each_cell():
            neighbors = []
            neighbors.append(cell.getNeighbor('north'))
            neighbors.append(cell.getNeighbor('east'))
            neighbors = [i for i in neighbors if i is not None]

            if len(neighbors) == 2:
                index = randint(0, 1) # randint 0 or 1
            elif len(neighbors) == 1:
                index = 0
            else:
                continue

            neighbor = neighbors[index]
            cell.link(neighbor)