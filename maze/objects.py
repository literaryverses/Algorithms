from random import randint, random, shuffle, choice

class Cell:
    def __init__(self, row: int, column: int, level = 0):
        self.coord = (row, column)
        self.neighbors = {}
        self.links = {}
        self.lvl = level

    def link(self, cell):
        self.links[cell] = True
        cell.links[self] = True

    def unlink(self, cell):
        self.links.pop(cell, None)
        cell.links.pop(self, None)

    def getLinks(self):
        return self.links.keys()

    def isLinked(self, cell):
        return self.links.get(cell)
    
    def isMasked(self):
        return self.isLinked(None)
    
    def getNeighbors(self, masking = True):
        neighbors = [n for n in self.neighbors.values() if n is not None]
        if not masking: # gets all existing neighbor cells
            return neighbors
        else: # applies masking by retrieving neighbors that are unmasked
            return list(filter(lambda n: not n.isMasked(), neighbors))

class Grid: # orthogonal maze
    def __init__(self, rows: int, columns: int, levels = 1, shape = 4):
        self.rows = rows
        self.cols = columns
        self.lvls = levels
        self.grid = [[[0 for c in range(columns)]
                      for r in range(rows)] for l in range(levels)]
        self.borders = {'north': '---', 'south': '---', 'west': '|', 'east': '|', 'up': 'O',
                        'vdoor': '   ', 'hdoor': ' ', 'down': '0', 'through': '@'}
        self.__prepareGrid(shape)

    def __str__(self):
        is_print_horizontal = False if 10 * self.rows < self.cols else True
        maze = ''
        for row in self.each_row():
            row_layout = ['']*3
            for cell in row:
                row_layout = self._drawCell(row_layout, cell)
            maze += '\n'.join(row_layout)
        if is_print_horizontal and self.lvls > 1:
            maze = maze.split('\n')
            length = len(max(maze, key = len))
            for i, maze_rows in enumerate(maze[:-1]):
                row_end = 2 * self.rows + 1
                if i > row_end - 1:
                    maze[i % (row_end)] += maze_rows.ljust(length+3)
                else: maze[i] = maze_rows.ljust(length+3)
            return '\n'.join(maze[:row_end])
        return maze

    def __prepareGrid(self, shape):
        for row in range(self.rows):
            for col in range(self.cols):
                for lvl in range(self.lvls):
                    self.grid[lvl][row][col] = Cell(row, col, lvl)
        for cell in self.each_cell(False):
            self.__configureCells(cell, shape)

    def __configureCells(self, cell, shape):
        row, col = cell.coord; lvl = cell.lvl
        if shape == 3:
            if sum(cell.coord) % 2:
                cell.neighbors['north'] = self.getCell(row-1, col, lvl)
                cell.neighbors['southeast'] = self.getCell(row, col+1, lvl)
                cell.neighbors['southwest'] = self.getCell(row, col-1, lvl)
            else:
                cell.neighbors['south'] = self.getCell(row+1, col, lvl)
                cell.neighbors['northeast'] = self.getCell(row, col+1, lvl)
                cell.neighbors['northwest'] = self.getCell(row, col-1, lvl)
        elif shape == 4:
            cell.neighbors['north'] = self.getCell(row-1, col, lvl)
            cell.neighbors['south'] = self.getCell(row+1, col, lvl)
            cell.neighbors['west'] = self.getCell(row, col-1, lvl)
            cell.neighbors['east'] = self.getCell(row, col+1, lvl)
        elif shape == 6:
            north_diagonal = (lambda r,c: r if c%2 else r-1)(row, col)
            south_diagonal = (lambda r,c: r+1 if c%2 else r)(row, col)
            cell.neighbors['north'] = self.getCell(row-1, col, lvl)
            cell.neighbors['south'] = self.getCell(row+1, col, lvl)
            cell.neighbors['northwest'] = self.getCell(north_diagonal, col-1, lvl)
            cell.neighbors['southwest'] = self.getCell(south_diagonal, col-1, lvl)
            cell.neighbors['northeast'] = self.getCell(north_diagonal, col+1, lvl)
            cell.neighbors['southeast'] = self.getCell(south_diagonal, col+1, lvl)
        if self.lvls > 1:
            cell.neighbors['up'] = self.getCell(row, col, lvl+1)
            cell.neighbors['down'] = self.getCell(row, col, lvl-1)

    def _drawCell(self, row_layout, cell):
        top, middle, bottom = row_layout[0], row_layout[1], row_layout[2]
        top += self._drawCorner(cell.coord[0], cell.coord[1], cell.lvl)
        top += self._drawBorder(cell, 'north') # draw top wall
        middle += f"{self._drawBorder(cell, 'west')} {self._drawBorder(cell, 'within')} "
        if cell.coord[0] == self.rows-1: # if last row
            bottom += self._drawCorner(cell.coord[0]+1, cell.coord[1], cell.lvl)
            bottom += self._drawBorder(cell, 'south') # draw bottom wall
        if cell.coord[1] == self.cols-1: # if last column
            top += self._drawCorner(cell.coord[0], cell.coord[1]+1, cell.lvl)
            middle += self._drawBorder(cell, 'east') # draw right wall
        if sum(cell.coord) == self.cols + self.rows - 2: # last cell
            bottom += f'{self._drawCorner(self.rows, self.cols, cell.lvl)}\n'
        return [top, middle, bottom]
    
    def __drawWithin(self, cell: Cell) -> str:
        directions = ['up', 'down']
        for i, direction in enumerate(directions):
            if direction in cell.neighbors.keys() and\
                cell.isLinked(cell.neighbors[direction]) and\
                    cell.neighbors[direction]!= None:
                directions[i] = self.borders[direction]
            else: directions[i] = False
        if directions[0] and directions[1]:
            return self.borders['through']
        elif directions[0]: return self.borders['up']
        elif directions[1]: return self.borders['down']
        else: return

    def _drawBorder(self, cell: Cell, direction: str) -> str:
        if direction == 'within':
            if (within := self.__drawWithin(cell)):
                return within
        elif (direction in cell.neighbors.keys() and\
            not cell.isLinked(cell.neighbors[direction])):
            return self.borders[direction]
        if len(direction) == 5: # north / south
            return self.borders['vdoor']
        else: # horizontal / diagonal
            return self.borders['hdoor']

    def _drawCorner(self, y: int, x: int, z = 0) -> str: # given two diagonal cells
        adjacents = [True] * 4
        if y == self.rows:
            adjacents[2] = adjacents[3] = False
        elif y - 1 < 0:
            adjacents[0] = adjacents[1] = False
        if x == self.cols:
            adjacents[0] = adjacents[3] = False
        elif x - 1 < 0:
            adjacents[1] = adjacents[2] = False

        for order, make_cell in enumerate(adjacents):
            if make_cell and order == 0: # Quadrant 1
                upRight = self.getCell(y-1, x, z)
                if not upRight.isLinked(upRight.neighbors['south']) or \
                    not upRight.isLinked(upRight.neighbors['west']):
                    return '+'
            elif make_cell and order == 1: # Quadrant II
                upLeft = self.getCell(y-1, x-1, z)
                if not upLeft.isLinked(upLeft.neighbors['south']) or \
                    not upLeft.isLinked(upLeft.neighbors['east']):
                    return '+'
            elif make_cell and order == 2: # Quadrant III
                downLeft = self.getCell(y, x-1, z)
                if not downLeft.isLinked(downLeft.neighbors['north']) or \
                    not downLeft.isLinked(downLeft.neighbors['east']):
                    return '+'
            elif make_cell and order == 3: # Quadrant IV
                downRight = self.getCell(y, x, z)
                if not downRight.isLinked(downRight.neighbors['north']) or \
                    not downRight.isLinked(downRight.neighbors['west']):
                    return '+'
        return ' '
    
    # disconnects from graph and other masked cells
    def mask_alone(self, row: int, col: int, lvl = 0):
        cell = self.getCell(row, col, lvl)
        cell.links[None] = True

    def getCell(self, row: int, col: int, lvl = 0) -> Cell:
        if row < 0 or col < 0 or lvl < 0 or \
            row == self.rows or col == self.cols or lvl == self.lvls:
            return # if out of bounds
        else:
            return self.grid[lvl][row][col]
    
    def getRandom(self) -> Cell:
        while (True):
            cell = self.grid[randint(0, self.lvls-1)][randint(0, self.rows-1)]\
                [randint(0, self.cols-1)]
            if not cell.isMasked():
                return cell

    def getSize(self, masking = True) -> int:
        if not masking:
            return self.lvls*self.rows*self.cols
        else: 
            return len(list(self.each_cell()))

    def each_row(self):
        for lvl in range(self.lvls):
            for row in range(self.rows):
                yield self.grid[lvl][row]
    
    def each_cell(self, masking = True):
        for lvl in range(self.lvls):
            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.grid[lvl][row][col]
                    if not masking:
                        yield cell
                    elif not cell.isMasked():
                        yield cell

    # avoid binary trees and sidewinder algos; recursive backtracker works best
    def mask(self, row: int, col: int, lvl = 0): # disconnects cell from rest of grid
        if row < 0 or row >= self.rows:
            raise Exception(f'Row {row} not within parameters')
        if col < 0 or col >= self.cols:
            raise Exception(f'Column {col} not within parameters')
        if lvl < 0 or lvl >= self.lvls:
            raise Exception(f'Level {lvl} not within parameters')
        cell = self.getCell(row, col, lvl)
        cell.links[None] = True
        for neighbor in cell.getNeighbors(False):
            if neighbor.isMasked() and neighbor != cell.neighbors.get('up')\
                and neighbor != cell.neighbors.get('down'): # prevent z-axis linking
                cell.link(neighbor)
    
    def braid(self, p = 1): # link up dead ends
        notLinked = (lambda n: True if n not in cell.links else False)
        deadEnds = (lambda c: True if len(c.links) == 1 else False)
        total_dead_ends = list(filter(deadEnds, self.each_cell()))
        shuffle(total_dead_ends)
        for cell in total_dead_ends:
            # p == proportion of dead ends allowed
            if len(cell.links) != 1 or random() > p:
                continue
            # get unlinked neighbors
            neighbors = list(filter(notLinked, cell.getNeighbors()))
            # best option is joining two dead ends
            best = list(filter(deadEnds, neighbors))
            if not best:
                best = neighbors
            neighbor = choice(best)
            cell.link(neighbor)


class TriGrid(Grid): # delta grid
    def __init__(self, rows: int, columns: int, levels = 1):
        super().__init__(rows, columns, levels, shape = 3)
        self.borders = {'north': '---', 'south': '---', 'northwest': '/', 'northeast': '\\',
                        'southwest': '\\', 'southeast': '/', 'vdoor': '   ', 'hdoor': ' ',
                        'up': 'O', 'down': '0', 'through': '@'}
        
    def _drawCell(self, row_layout, cell):
        top, middle, bottom = row_layout[0], row_layout[1], row_layout[2]
        if sum(cell.coord) % 2:
            if cell.coord[1] == 0: # 1st column
                top += self._drawCorner(cell.coord[0], cell.coord[1]-1, cell.lvl)
                middle += f" {self._drawBorder(cell, 'southwest')}"
            top += self._drawBorder(cell, 'north')
            top += self._drawCorner(cell.coord[0], cell.coord[1]+1, cell.lvl)
            middle += f"{self._drawBorder(cell,'within')}{self._drawBorder(cell, 'southeast')}"
            if cell.coord[1] == 0 and cell.coord[0] == self.rows-1: # last cell in 1st column
                bottom += '  ' # indentation
            if sum(cell.coord) == self.cols + self.rows - 2: # last cell
                bottom += f'{self._drawCorner(cell.coord[0]+1, cell.coord[1], cell.lvl)}\n'
        else: # if is pointy
            if cell.coord[1] == 0: # 1st column
                top += f'  {self._drawCorner(cell.coord[0], cell.coord[1], cell.lvl)}'
                middle += f" {self._drawBorder(cell, 'northwest')}"
            if cell.coord[0] == self.rows-1: # last row
                bottom += self._drawCorner(cell.coord[0]+1, cell.coord[1]-1, cell.lvl)
                bottom += self._drawBorder(cell, 'south')
            middle += f"{self._drawBorder(cell,'within')}{self._drawBorder(cell, 'northeast')}"
            if sum(cell.coord) == self.cols + self.rows - 2: # last cell
                bottom += f'{self._drawCorner(cell.coord[0]+1, cell.coord[1]+1, cell.lvl)}\n'
        return [top, middle, bottom]
        '''
        if sum(cell.coord) % 2:
            top += self._drawBorder(cell, 'north')
            top += self._cornerize(cell.coord[0], cell.coord[1]+1, cell.lvl)
            if cell.coord[0] % 2 and cell.coord[1] == 0:
                middle += ' '
            middle += f"{self._drawBorder(cell, 'southwest')}"
            middle += f"{self._drawBorder(cell,'within')}{self._drawBorder(cell, 'southeast')}"
            if cell.coord[0] == self.rows-1 and cell.coord[1] == 0: # if 1st cell in last row
                bottom = '  '
            if sum(cell.coord) == self.rows + self.cols - 2: # if last cell
                bottom += f'{self._cornerize(cell.coord[0]+1, cell.coord[1], cell.lvl)}\n'
        else: # if is pointy
            if cell.coord[1] == 0 or cell.coord[0] == self.rows-1:
                bottom += self._cornerize(cell.coord[0]+1, cell.coord[1]-1, cell.lvl)
            if cell.coord[1] == 0: # if 1st column
                top += f'  {self._cornerize(cell.coord[0], cell.coord[1], cell.lvl)}'
                middle += f" {self._drawBorder(cell, 'northwest')}{self._drawBorder(cell,'within')}"
            else:
                middle += self._drawBorder(cell,'within')
            if cell.coord[0] == self.rows-1: # if last row
                bottom += self._drawBorder(cell,'south')
            if cell.coord[1] == self.cols-1: # if last column
                middle += self._drawBorder(cell, 'northeast')
            if sum(cell.coord) == self.rows + self.cols - 2: # if last cell
                bottom += f'{self._cornerize(cell.coord[0]+1, cell.coord[1]+1, cell.lvl)}\n'
        '''
        return [top, middle, bottom]

    def _drawCorner(self, y: int, x: int, z = 0) -> str: # given two diagonal cells
        adjacents = [True] * 6
        if y == self.rows:
            adjacents[0] = adjacents[1] = adjacents[5] = False
        elif y - 1 < 0:
            adjacents[2] = adjacents[3] = adjacents[4] = False
        if x == self.cols or x == -1:
            adjacents[0] = adjacents[3] = False
        if x + 1 >= self.cols:
            adjacents[1] = adjacents[2] = False
        elif x <= 0:
            adjacents[4] = adjacents[5] = False

        for order, make_cell in enumerate(adjacents):
            if make_cell and order == 0:
                downMid = self.getCell(y, x, z)
                if not downMid.isLinked(downMid.neighbors['northwest']) or \
                    not downMid.isLinked(downMid.neighbors['northeast']):
                    return 'x'
            elif make_cell and order == 1:
                downRight = self.getCell(y, x+1, z)
                if not downRight.isLinked(downRight.neighbors['north']) or \
                    not downRight.isLinked(downRight.neighbors['southwest']):
                    return 'x'
            elif make_cell and order == 2:
                upRight = self.getCell(y-1, x+1, z)
                if not upRight.isLinked(upRight.neighbors['south']) or \
                    not upRight.isLinked(upRight.neighbors['northwest']):
                    return 'x'
            elif make_cell and order == 3:
                upMid = self.getCell(y-1, x, z)
                if not upMid.isLinked(upMid.neighbors['southeast']) or \
                    not upMid.isLinked(upMid.neighbors['southwest']):
                    return 'x'
            elif make_cell and order == 4:
                upLeft = self.getCell(y-1, x-1, z)
                if not upLeft.isLinked(upLeft.neighbors['northeast']) or \
                    not upLeft.isLinked(upLeft.neighbors['south']):
                    return 'x'
            elif make_cell and order == 5:
                downLeft = self.getCell(y, x-1, z)
                if not downLeft.isLinked(downLeft.neighbors['north']) or \
                    not downLeft.isLinked(downLeft.neighbors['southeast']):
                    return 'x'
        return ' '


class HexGrid(Grid): # sigma maze
    def __init__(self, rows: int, columns: int, levels = 1):
        super().__init__(rows, columns, levels, shape = 6)

    def __str__(self): # creates sigma maze from delta maze
        template = TriGrid(2*self.rows+1, self.cols*3, self.lvls)
        self.__hexify(template)
        for row in self.each_row():
            for cell in row:
                template = self.__reformat(cell, template)
        return str(template)
    
    # link up triangular grid to match the links of hexagonal maze
    def __reformat(self, hex_cell: Cell, triGrid: TriGrid) -> TriGrid:
        for direction in hex_cell.neighbors.keys():
            neighbor = hex_cell.neighbors[direction]
            if neighbor and hex_cell.isLinked(neighbor):
                triangle = self.__getTriangle(hex_cell, direction, triGrid)
                triangle.link(triangle.neighbors[direction])
            elif hex_cell.isLinked(None): # hex cell links to none, hence is masked
                triangle = self.__getTriangle(hex_cell, 'up', triGrid) # get corresp triangle
                self.__maskUp(triGrid, False, triangle.coord[0], triangle.coord[1], triangle.lvl)

            '''
         for direction in hex_cell.neighbors.keys():
            neighbor = hex_cell.neighbors[direction]
            if neighbor and hex_cell.isLinked(neighbor):
                triangle = self.__getTriangle(hex_cell, direction, triGrid)
                triangle.link(triangle.neighbors[direction])'''
        return triGrid

    # returns corresponding triangular cell according to direction of hexagonal cell
    def __getTriangle(self, hex_cell: Cell, direction: str, triGrid: TriGrid) -> Cell:
        row, col = hex_cell.coord; lvl = hex_cell.lvl
        adjust = (lambda c: 1 if c%2 else 0)(col)
        if direction == 'northwest':
            return triGrid.getCell(2*row+adjust, 3*col, lvl)
        elif direction == 'north':
            return triGrid.getCell(2*row+adjust, 3*col+1, lvl)
        elif direction == 'northeast':
            return triGrid.getCell(2*row+adjust, 3*col+2, lvl)
        elif direction == 'southeast':
            return triGrid.getCell(2*row+adjust+1, 3*col+2, lvl)
        elif direction == 'south':
            return triGrid.getCell(2*row+adjust+1, 3*col+1, lvl)
        elif direction == 'southwest':
            return triGrid.getCell(2*row+adjust+1, 3*col, lvl)
        elif direction == 'up' or direction == 'down': # returns corresponding triangular cell
            return triGrid.getCell(2*row+adjust, 3*col, lvl)
    
    # create hexagonal grid from triangular grid
    def __hexify(self, triGrid: TriGrid):
        for z in range(self.lvls):
            y = x = 0
            for _ in range(self.rows*self.cols): # make sigma maze
                if x == 3*self.cols:
                    x = 0; y += 2 # reset coord
                if x % 2:
                    self.__linkUp(triGrid, y+1, x, z)
                    if y == 0:
                        self.__maskUp(triGrid, True, y, x, z)
                else:
                    self.__linkUp(triGrid, y, x, z)
                    if y == 2*self.rows-2:
                        self.__maskUp(triGrid, True, y, x, z)
                x += 3

    # link triangular cells into hexagonal cell
    def __linkUp(self, triGrid: TriGrid, row: int, col: int, lvl = 0):
        current = triGrid.getCell(row, col, lvl)
        for _x in range(1,3):
            temp, current = current, triGrid.getCell(row, col+_x, lvl)
            temp.link(current)
        for _x in range(2,-1,-1):
            temp, current = current, triGrid.getCell(row+1, col+_x, lvl)
            temp.link(current)
        current.link(triGrid.getCell(row, col, lvl))

    def __maskUp(self, triGrid: TriGrid, isEdge: bool, row: int, col: int, lvl = 0):
        y_edge = (lambda r: 2 if r == triGrid.rows-3 else 0)(row)
        if isEdge: # if formating edge
            for x in range(3):
                triGrid.mask(row+y_edge, col+x, lvl)
        else:
            for x in range(3):
                triGrid.mask(row, col+x, lvl) # top row of hexagon
                triGrid.mask(row+1, col+x, lvl) # bottom row of hexagon

# Testing and Demonstrations
###----main-----
from maze_generation import *
# Test algorithms
print(aldousBroder(Grid(5,5))) 
print(binaryTree(Grid(5,5)))
print(hunt_and_kill(Grid(5,5)))
print(recursive_backtracker(Grid(5,5)))
print(sidewinder(Grid(5,5)))
print(wilsons(Grid(5,5)))

# Test masking
grid = Grid(5,5)
grid.mask(2,2); grid.mask(0,0)
print(aldousBroder(grid))

# test 3D levels
grid1 = Grid(5,5,3)
grid1.mask(2,2,0); grid1.mask(2,2,1); grid1.mask(2,2,2)
print(wilsons(grid1))

# test grid classes
grid2 = TriGrid(3,2,8)
print(aldousBroder(grid2))

grid3 = HexGrid(3,4)
grid3.mask(0,0)
grid3.mask(1,0);grid3.mask(0,0);grid3.mask(2,0)
grid3.mask(2,1);grid3.mask(2,3)
print(grid3)

'''
+---+---+---+---+---+
|       |   |       |
+   +---+   +   +---+
|               |   |
+---+---+---+   +   +
|           |       |
+---+   +---+   +---+
|               |   |
+---+---+---+   +   +
|                   |
+---+---+---+---+---+

+---+---+---+---+---+
|           |   |   |
+---+---+   +   +   +
|               |   |
+---+---+---+   +   +
|   |           |   |
+   +---+---+   +   +
|   |       |       |
+   +---+   +---+   +
|                   |
+---+---+---+---+---+

+---+---+---+---+---+
|                   |
+---+   +---+---+   +
|           |       |
+   +---+---+   +---+
|           |       |
+---+---+---+---+   +
|   |               |
+   +   +---+---+---+
|                   |
+---+---+---+---+---+

+---+---+---+---+---+
|               |   |
+   +   +---+   +   +
|   |       |       |
+   +---+   +---+   +
|   |       |       |
+---+   +---+   +---+
|       |   |   |   |
+---+---+   +   +   +
|                   |
+---+---+---+---+---+

+---+---+---+---+---+
|                   |
+---+---+   +   +   +
|           |   |   |
+   +   +---+---+   +
|   |   |           |
+   +   +---+   +---+
|   |   |           |
+   +---+   +---+   +
|       |   |       |
+---+---+---+---+---+

+---+---+---+---+---+
|           |       |
+   +---+   +   +---+
|   |               |
+   +---+   +   +   +
|   |       |   |   |
+---+---+---+   +---+
|           |       |
+   +---+---+---+   +
|                   |
+---+---+---+---+---+

    +---+---+---+---+
    |   |   |       |
+---+   +   +   +---+
|       |       |   |
+   +---+---+   +   +
|       |   |   |   |
+   +   +---+   +   +
|   |       |       |
+   +---+   +---+   +
|       |           |
+---+---+---+---+---+

+---+---+---+---+---+   +---+---+---+---+---+   +---+---+---+---+---+   
|         O   O   O |   | O   O | 0 | 0 | @ |   | 0 | 0     |   | 0 |   
+   +   +---+   +---+   +---+---+   +---+---+   +   +---+---+   +---+   
|   | O | O | O     |   |   | @ | 0 | 0     |   |   | 0             |   
+   +   +---+   +   +   +   +---+---+---+---+   +   +   +---+   +---+   
|   | O |   |   |   |   |     0 |   |   | O |   |   |   |   |   | 0 |   
+---+---+---+   +---+   +---+---+---+   +   +   +   +---+---+   +---+   
| O |           | O |   | @ | O | O     | 0 |   | 0 | 0 | 0         |   
+---+   +   +   +   +   +---+   +---+   +---+   +   +---+   +   +---+   
| O |   |   |       |   | @     | O |       |   | 0       0 |       |   
+---+---+---+---+---+   +---+---+---+---+---+   +---+---+---+---+---+   
  x---x     x---x     x---x     x---x     x---x     x---x     x---x     x---x   
 / \O/     /O 0/     /@\O/     /0 0/     /  O/     / \@/     /O\@/     /0 0/    
x   x     x   x     x---x     x   x     x   x     x   x     x   x     x---x     
 \O/O\     \@/0\     \0 O\     \O/@\     \0/0\     \O  \     \0 O\     \  0\    
  x---x     x   x     x---x     x   x     x   x     x---x     x---x     x---x   
 /O  /     /@ O/     /@\@/     /0\0/     /  O/     /O\@/     /0 @/     /  0/    
x---x     x---x     x---x     x---x     x---x     x---x     x---x     x---x     
              x---x        
             /     \      
        x---x       x---x
       /     \     /     \
      x       x---x       x
       \     /     \     /
        x---x       x---x
       /     \     /     \
      x       x---x       x
       \     /     \     /
        x---x       x---x
             \     /      
              x---x  
'''