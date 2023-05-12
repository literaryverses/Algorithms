# Performs a backtracker recursively

from random import sample

def recursive_backtracker(grid):
    stack = []
    stack.append(grid.getRandom())

    while stack:
        print(grid)
        cell = stack[-1]
        neighbors = [n for n in cell.getNeighbors() if not n.getLinks()]

        if neighbors:
            neighbor = sample(neighbors,1)[0]
            cell.link(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()
    return grid

from objects import Grid
grid = Grid(4,4)
print(recursive_backtracker(grid))