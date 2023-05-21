# Performs maze generation algorithms

from random import randint, choice, shuffle, random

'''
Aldous-Broder: breaks down walls between unvisited cells until all the cells
in the grid are visited
'''
def aldousBroder(grid):
    cell = grid.getRandom()
    unvisited = grid.getSize() - 1
    while unvisited > 0:
        neighbor = choice(cell.getNeighbors())
        if not neighbor.getLinks(): # checks if neighbor has no links
            cell.link(neighbor)
            unvisited -= 1
        cell = neighbor
    return grid

'''
Binary Tree: destroys either a longitudinal or latitudinal wall in each cell,
using an equiprobable random selection
'''
def binaryTree(grid, skew = ''):
    # randomized skew if input skew is unspecified or incorrect
    skews = { # preferred directions to move for orthogonal maze
        'NW': ('north', 'west'),
        'NE': ('north', 'east'),
        'SW': ('south', 'west'),
        'SE': ('south', 'east')}
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
Eller's:
'''
def ellers(grid):
    return

from objects import Grid
grid = Grid(10,10)
print(ellers(grid))



'''
Growing Tree: implements both simplified and true Prim's algorithms proport
proportionally based on input from 0 (random selection, Prim's) to 1 (last
selection, recursive backtracking). The Default is set to 0.5, meaning the 
two options are equiprobable.
'''
def growingTree(grid, slider = 0.5):
    isAvailable = lambda n: True if not n.getLinks() else False
    active = []
    active.append(grid.getRandom())
    while active:
        randomly = (lambda l: choice(l))(active) # Prim's (simplified)
        last = (lambda l: l[-1])(active) # Recursive backtracker
        cell = [randomly, last][random() < slider]
        neighbors = list(filter(isAvailable,cell.getNeighbors()))
        if neighbors:
            neighbor = choice(neighbors)
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)
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
Kruskal's: randomly (since no path cost assigned) merges a pair neighboring
cells as long as they are not already linked
'''
def kruskals(grid):
    # randomized skew if input skew is unspecified or incorrect
    neighbors = [] # track pairs of neighboring cells
    set_for_cell = {} # maps cells to corresponding set identifiers
    cells_in_set = {} # maps set identifiers to cells belonging to those sets    
    can_merge = lambda l,r: set_for_cell[l] != set_for_cell[r]

    def merge(left, right):
        left.link(right)
        winner = set_for_cell[left]
        loser = set_for_cell[right]
        losers = cells_in_set[loser]
        for cell in losers:
            cells_in_set[winner].add(cell)
            set_for_cell[cell] = winner
        cells_in_set.pop(loser)  

    for i,cell in enumerate(grid.each_cell()):
        set_for_cell[cell] = i # assign each cell to own set
        cells_in_set[i] = {cell}
        if cell.neighbors.get('south'):
            neighbors.append([cell, cell.neighbors['south']])
        if cell.neighbors.get('east'):
            neighbors.append([cell, cell.neighbors['east']])

    shuffle(neighbors)
    while neighbors:
        left, right = neighbors.pop() # chooses pair of neighboring cells 
        if can_merge(left, right): # if belong to different sets, merge
            merge(left, right) 
    return grid

'''
Prim's (simplified): Prim's algorithm if every path had equal weight, 
in which a random neighboring cell is added to the path one-by-one
'''
def prims_sim(grid):
    isAvailable = lambda n: True if not n.getLinks() else False
    active = []
    active.append(grid.getRandom())
    while active:
        cell = choice(active)
        neighbors = list(filter(isAvailable,cell.getNeighbors()))
        if neighbors:
            neighbor = choice(neighbors)
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)
    return grid

'''
Prim's (true): randomly assigns weights to cells and adds neighboring
cells according to those costs
'''
def prims_true(grid):
    isAvailable = lambda n: True if not n.getLinks() else False
    active = []
    active.append(grid.getRandom())
    costs = {}
    for cell in grid.each_cell():
        costs[cell] = randint(0,100)
    while active:
        cell = min(active, key=costs.get)
        neighbors = list(filter(isAvailable,cell.getNeighbors()))
        if neighbors:
            neighbor = min(neighbors, key=costs.get)
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)
    return grid

'''
Recursive backtracker: DFS that recursively backtracks from dead ends
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
Recursive division:
'''
def recursive_division(grid):
    return

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