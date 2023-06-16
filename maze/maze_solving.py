# Performs maze generation algorithms. 
# These are made specifically for 2D orthogonal mazes

from random import choice
from collections import Counter

## utilities
class  Compass:
    def __init__(self, direct: str):
        if direct == 'right':
            self.orientations = 'north west south east'.split()
        elif direct == 'left':
            self.orientations = 'north east south west'.split()
    def getOriented(self, cell):
        if cell.coord[0] == 0:
            return 'south'
        if cell.coord[1] == 0:
            return 'east'
        if cell.coord[1] > cell.coord[0]:
            return 'west'
        else: # cell.coord[1] <= cell.coord[0]
            return 'north'
    def getOptions(self, facing: str):
        index = self.orientations.index(facing) - 1
        for i in range(index, index+4):
            yield self.orientations[i%4]

class Path:
    def __init__(self, start):
        self.path = [start]
    
    def append(self, cell): # add cell to path
        self.path.append(cell)
    
    def getCoords(self): # get only coordinates of path
        for cell in self.path:
            yield cell.coord
    
    def cleanup(self): # remove backtracking
        repeats = [item for item, count in Counter(self.path).items() if count > 1]
        for repeat in repeats:
            while (self.path.count(repeat) > 1):
                i1 = self.path.index(repeat)
                i2 = self.path.index(repeat, i1+1)
                self.path = self.path[:i1] + self.path[i2:]
        return self.path

## Inside algorithms
'''
Random Mouse: stimulates a mouse moving inside maze. 
Very inefficent, especially with no memory.
'''
def randomMouse(start, end):
    cell = start
    path = Path(cell)
    while (cell != end):
        cell = choice(cell.getNeighbors())
        path.append(cell)
    return path

'''
Wall Follower: follows on the side of the wall. This not guarenteed to solve if the starting 
position starts inside the maze (as opposed to a cell on the very edge of the grid)
'''
def wallFollower(start, end, direct = 'right'):
    path = Path(start)
    cell = start
    compass = Compass(direct)
    facing = compass.getOriented(start)
    while (cell != end):
        directions = list(compass.getOptions(facing))
        for direction in directions:
            if cell.isLinked(next := cell.neighbors.get(direction)):
                facing = direction
                cell = next
                path.append(cell)
                break
    return path

'''
Pledge: runs a straight direction until it hits a wall. Afterwards, follows a wall follower
algorithm until the number of clockwise turns is equal to the number of counterclockwise turns, 
at which it resumes running a straight direction again.
'''
def pledge(start, end):
    direct = choice(start.neighbors.keys())

def tremaux(start, end):
    pass

## Outside algorithms
def dead_end(grid):
    pass

def cul_de_sa(grid):
    pass

def blind_alley_filler(grid):
    pass

def blind_alley_sealer(grid):
    pass

## Other algorithms
def recursive_backtracer(grid):
    pass

def collision_solver(grid):
    pass

def shortest_path_finder(grid):
    pass

def shortest_paths_finder(grid):
    pass