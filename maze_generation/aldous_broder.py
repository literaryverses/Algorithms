from random import sample

def AldousBroder(grid):

    cell = grid.getRandom()
    unvisited = grid.getSize() - 1

    while unvisited > 0:
        neighbor = sample(cell.getNeighbors(), 1)[0]

        if not neighbor.links: # checks if neighbor has no links
            cell.link(neighbor)
            unvisited -= 1
        cell = neighbor

    return grid

import objects
AldousBroder(objects.Grid(5,5))