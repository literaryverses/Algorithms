# Performs maze generation algorithm

from random import randint, sample, shuffle

def aldousBroder(grid): # Aldous-Broder algo
    cell = grid.getRandom()
    unvisited = grid.getSize() - 1

    while unvisited > 0:
        neighbor = sample(cell.getNeighbors(), 1)[0]

        if not neighbor.links: # checks if neighbor has no links
            cell.link(neighbor)
            unvisited -= 1
        cell = neighbor

    return grid

def binaryTree(grid, skew: str): # binary tree algo
    skews = {
        'NW': ('north', 'west'),
        'NE': ('north', 'east'),
        'SW': ('south', 'west'),
        'SE': ('south', 'east'),}
        
    if (skew:=skew.upper()) not in skews: # randomized skew if input skew is incorrect
        skew = sample(skews.keys(), 1)[0]

    for cell in grid.each_cell():
        neighbors = []
        neighbors.append(cell.neighbors.get(skews.get(skew)[0]))
        neighbors.append(cell.neighbors.get(skews.get(skew)[1]))
        neighbors = [i for i in neighbors if i is not None]

        if len(neighbors) == 2:
            index = randint(0, 1)
        elif len(neighbors) == 1:
            index = 0
        else: # len(neighbors) = 0
            continue

        neighbor = neighbors[index]
        cell.link(neighbor)
    return grid

def hunt_and_kill(grid): # hunt and kill algo
    current = grid.getRandom()

    while current:
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
    return grid

def recursive_backtracker(grid): # performs backtracker recursively
    stack = []
    stack.append(grid.getRandom())

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

            should_close_out = at_eastern_boundary or (not at_northern_boundary and randint(0, 1) == 0)

            if should_close_out:
                member = run[randint(0, len(run)-1)]
                northerner = member.neighbors.get('north')
                if northerner:
                    member.link(northerner)
                run.clear()
            else:
                easterner = cell.neighbors.get('east')
                cell.link(easterner)
    return grid

def wilsons(grid): # Wilson's algo
    isNotMasked = lambda cell: not cell.isLinked(None)
    unvisited = list(filter(isNotMasked, grid.each_cell()))
    shuffle(unvisited)

    unvisited.pop() # set first goal cell

    while unvisited:
        path = unvisited[0:1]
        cell = path[0]

        while cell in unvisited: # create path
            cell = sample(list(filter(isNotMasked, cell.getNeighbors())), 1)[0]
            
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