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
        length = len(self.orientations)
        index = self.orientations.index(facing) - 1
        for i in range(4):
            i += index
            if i < 0:
                i += length
            elif i > length-1:
                i -= length
            yield self.orientations[i]

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
Wall Follower: follows on the side of the wall. 
This not guarenteed to solve if the starting position starts inside the maze
(as opposed to a cell on the very edge of the grid)
'''
def wallFollower(start, end, direct):
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

from objects import Grid
from maze_generation import aldousBroder
'''
grid = aldousBroder(Grid(5,5))
print(grid)
path = wallFollower(grid.getCell(0,0), grid.getCell(4,4), 'right')
print(list(path.getCoords()))
path.cleanup()
print(list(path.getCoords()))'''