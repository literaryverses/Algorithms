# Performs the binary tree algorithm

from random import randint, sample

def binaryTree(grid, skew: str):
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