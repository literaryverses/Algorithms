from random import randint

class BinaryTree: # Binary Tree Algorithm
    def __init__(self, grid, skew):
        skewes = {
            'NW': ('north', 'west'),
            'NE': ('north', 'east'),
            'SW': ('south', 'west'),
            'SE': ('south', 'east'),}
        for cell in grid.each_cell():
            neighbors = []
            neighbors.append(cell.neighbors.get(skewes.get(skew)[0]))
            neighbors.append(cell.neighbors.get(skewes.get(skew)[1]))
            neighbors = [i for i in neighbors if i is not None]

            if len(neighbors) == 2:
                index = randint(0, 1)
            elif len(neighbors) == 1:
                index = 0
            else: # neighbors = 0
                continue

            neighbor = neighbors[index]
            cell.link(neighbor)        

def generateMaze(grid, skew):
    skewes = ('NE', 'NW', 'SW', 'SE')
    if skew.upper() not in skewes:
        skew = skewes[randint(0, 3)]
    BinaryTree(grid, skew.upper())
    return grid