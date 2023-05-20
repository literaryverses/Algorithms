# Performs maze generation algorithms

from random import randint, choice, shuffle

'''
Aldous-Broder: breaks down walls between unvisited cells until all the cells
in the grid are visited
'''
def aldousBroder(grid):
    cell = grid.getRandom()
    unvisited = grid.getSize() - 1
    while unvisited > 0:
        neighbor = choice(cell.getNeighbors())
        if not neighbor.links: # checks if neighbor has no links
            cell.link(neighbor)
            unvisited -= 1
        cell = neighbor
    return grid

'''
Binary Tree: destroys either a longitudinal or latitudinal wall in each cell,
using an equiprobable random selection
'''
def binaryTree(grid, skew = ''):
    skews = { # preferred directions to move
        'NW': ('north', 'west'),
        'NE': ('north', 'east'),
        'SW': ('south', 'west'),
        'SE': ('south', 'east'),}
    # randomized skew if input skew is incorrect
    if (skew:=skew.upper()) not in skews:
        skew = choice(list(skews.keys()))
    for cell in grid.each_cell():
        neighbors = []
        neighbors.append(cell.neighbors.get(skews.get(skew)[0]))
        neighbors.append(cell.neighbors.get(skews.get(skew)[1]))
        neighbors = [n for n in neighbors if n is not None]
        if len(neighbors) == 2: # select neighbor to link to
            index = randint(0, 1)
        elif len(neighbors) == 1:
            index = 0
        else: # len(neighbors) == 0
            continue
        neighbor = neighbors[index]
        cell.link(neighbor)
    return grid

'''
Hunt and Kill: a random-walk based algorithm similar to Aldous-Broder except 
it only allows steps into unvisited cells only
'''
def hunt_and_kill(grid):
    current = grid.getRandom()
    while current:
        neighbors = current.getNeighbors()
        unvisited_neighbors = [n for n in neighbors 
                               if not n.getLinks()]
        if unvisited_neighbors:
            neighbor = choice(unvisited_neighbors)
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
                    neighbor = choice(visited_neighbors)
                    current.link(neighbor)
                    break
    return grid

'''
Recursive backtracker: recursively backtracks from dead ends
'''
def recursive_backtracker(grid):
    stack = [] # stack to recurse through
    stack.append(grid.getRandom())
    while stack:
        cell = stack[-1]
        neighbors = [n for n in cell.getNeighbors() if not n.getLinks()]
        if neighbors:
            neighbor = choice(neighbors)
            cell.link(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()
    return grid

'''
Sidewinder: decides to destroy the right wall or not for every cell based
on equiprobable random choice. If the wall is not destroyed, then any cell
preceding the current one within that row will destroy its northern wall.
'''
def sidewinder(grid): # sidewinder algo
    for row in grid.each_row():
        run = []
        for cell in row:
            run.append(cell)
            at_eastern_boundary = True # end of row
            if cell.neighbors.get('east'):
                at_eastern_boundary = False
            at_northern_boundary = True # top of grid
            if cell.neighbors.get('north'):
                at_northern_boundary = False
            # decide to walk east or north
            should_close_out = at_eastern_boundary or \
                (not at_northern_boundary and randint(0, 1) == 0)
            if should_close_out: # create dead end
                # select any preceding cell in row of current cell
                member = run[randint(0, len(run)-1)]
                northerner = member.neighbors.get('north')
                if northerner:
                    member.link(northerner)
                run.clear()
            else:
                easterner = cell.neighbors.get('east')
                cell.link(easterner)
    return grid

'''
Wilson's: draws multiple paths from unvisited cells to a visited one until
there are no more unvisited cells.
'''
def wilsons(grid):
    unvisited = list(grid.each_cell())
    shuffle(unvisited)
    unvisited.pop() # set first goal cell
    while unvisited:
        path = unvisited[0:1]
        cell = path[0]
        while cell in unvisited: # create path
            cell = choice(cell.getNeighbors())
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