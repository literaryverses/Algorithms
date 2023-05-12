# Perform Wilson's algorithm

from random import shuffle, sample

def wilsons(grid):
    unvisited = list(grid.each_cell())
    shuffle(unvisited)

    unvisited.pop() # set first goal cell

    while unvisited:
        path = unvisited[0:1]
        cell = path[0]

        while cell in unvisited: # create path
            cell = sample(cell.getNeighbors(), 1)[0]
            
            if cell in path: # remove loops
                path = path[:path.index(cell)+1]
            else:
                path.append(cell)
        
        for index, cell in enumerate(path): 
            if index < len(path)-1:
                cell.link(path[index+1]) # link the cells in path

                unvisited.remove(cell) # set path as visited

        path.clear() # clear path

    return grid