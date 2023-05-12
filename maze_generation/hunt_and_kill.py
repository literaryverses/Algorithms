# Performs the Hunt and Kill algorithm

from random import sample

def hunt_and_kill(grid):

    current = grid.getRandom()

    while current:
        neighbors = current.getNeighbors()

        unvisited_neighbors = [n for n in neighbors 
                               if not current.isLinked(n)]
        if unvisited_neighbors:
            neighbor = unvisited_neighbors.pop()
            current.link(neighbor)
            current = neighbor
        else:
            current = None # to break out while loop if all visited

            for cell in grid.each_cell():
                visited_neighbors = [n for n in neighbors
                                     if cell.isLinked(n)]

                # if visited neighbors exist and cell has no links
                if visited_neighbors and bool(cell.getLinks):
                    current = cell
                    neighbor = sample(visited_neighbors,1)
                    current.link(neighbor)
                    break