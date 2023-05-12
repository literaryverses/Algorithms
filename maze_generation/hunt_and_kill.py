# Performs the Hunt and Kill algorithm

from random import sample

def hunt_and_kill(grid):

    current = grid.getRandom()

    while current:
        print(grid) #proofreading
        neighbors = current.getNeighbors()

        unvisited_neighbors = [n for n in neighbors 
                               if not n.getLinks()]
        if unvisited_neighbors:
            neighbor = sample(unvisited_neighbors,1)[0]
            current.link(neighbor)
            current = neighbor
        else:
            current = None # to break out while loop if all visited

            for cell in grid.each_cell():
                neighbors = cell.getNeighbors()
                visited_neighbors = [n for n in neighbors
                                     if n.getLinks()]

                # if visited neighbors exist and cell has no links
                if visited_neighbors and not cell.getLinks():
                    current = cell
                    neighbor = sample(visited_neighbors,1)[0]
                    current.link(neighbor)
                    break

from board import Grid
grid = Grid(4,4)
hunt_and_kill(grid)
print("DONE")