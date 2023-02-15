from random import randint

class BinaryTree: # Binary Tree Algorithm
    def __init__(self, grid):
        for cell in grid.each_cell():
            neighbors = []
            neighbors.append(cell.neighbors.get('north'))
            neighbors.append(cell.neighbors.get('east'))
            neighbors = [i for i in neighbors if i is not None]

            if len(neighbors) == 2:
                index = randint(0, 1)
            elif len(neighbors) == 1:
                index = 0
            else: # neighbors = 0
                continue

            neighbor = neighbors[index]
            cell.link(neighbor)

def generateMaze(grid):
    BinaryTree(grid)
    return grid

from objects import Grid
print(generateMaze(Grid(24, 18)))