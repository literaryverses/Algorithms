from random import randint

class Cell:
    def __init__(self, row: int, column: int):
        self.coord = (row, column)
        self.neighbors = {}
        self.links = {}

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
    
    def getNeighbors(self):
        return [v for v in self.neighbors.values() if v is not None]


class Grid:
    def __init__(self, rows: int, columns: int, sides: int):
        self.rows = rows
        self.cols = columns
        self.shape = sides # three options available: 3, 4, 6
        self.grid = [[0 for c in range(columns)] for r in range(rows)]
        self._prepareGrid()

    def __str__(self):
        if self.shape == 4:
            final = ''
            for row in self.each_row():
                top = middle = bottom = ''
                for cell in row:
                    wall = ' '
                    body = '   ' # 3 spaces
                    top += self._cornerize(cell.coord[0], cell.coord[1])
                    if not cell.isLinked(cell.neighbors['north']):
                        top += '---'
                    else: 
                        top += body
                    if not cell.isLinked(cell.neighbors['west']):
                        wall = '|'
                    if cell.coord[0] == self.rows-1: # if last row
                        bottom += self._cornerize(cell.coord[0]+1, cell.coord[1])
                        if not cell.isLinked(cell.neighbors['south']):
                            bottom += '---'
                        else: 
                            bottom += body
                    if cell.coord[1] == self.cols-1: # if last column
                        top += self._cornerize(cell.coord[0], cell.coord[1]+1)
                        if not cell.isLinked(cell.neighbors['east']):
                            body += '|'
                    middle += f'{wall}{body}'
                final += f'{top}\n{middle}\n{bottom}'
            final += self._cornerize(cell.coord[0]+1, cell.coord[1]+1) # most bottom right corner
            return final
        #elif self.shape == 6:
            #for row in self.each_row():
            '''
             +---+       +---+
            /     \\    /     \\
           +       +---+       +
            \     /     \\    /
             +---+       +---+
            /     \\    /     \\
           +       +---+

           +---+---+
            \ / \ /
            +---+
            '''

    def _prepareGrid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = Cell(row, col)
        for cell in self.each_cell():
            self._configureCells(cell)

    def _configureCells(self, cell):
        row, col = cell.coord
        if self.shape == 4:
            cell.neighbors['north'] = self.getCell(row-1, col)
            cell.neighbors['south'] = self.getCell(row+1, col)
            cell.neighbors['west'] = self.getCell(row, col-1)
            cell.neighbors['east'] = self.getCell(row, col+1)
        elif self.shape == 6:
            north_diagonal = (lambda r, c: r-1 if c%2 else r)(row, col)
            south_diagonal = (lambda r, c: r if c%2 else r+1)(row, col)
            cell.neighbors['north'] = self.getCell(row-1, col)
            cell.neighbors['south'] = self.getCell(row+1, col)
            cell.neighbors['northwest'] = self.getCell(north_diagonal, col-1)
            cell.neighbors['southwest'] = self.getCell(south_diagonal, col-1)
            cell.neighbors['northeast'] = self.getCell(north_diagonal, col+1)
            cell.neighbors['southeast'] = self.getCell(south_diagonal, col+1)
        else:
            raise Exception(f'{self.shape} is not available; try 3, 4, or 6')

    def _cornerize(self, q4_y: int, q4_x: int) -> str: # given two diagonal cells
        quadrants = [True, True, True, True] # QI, QII, QIII, QIV
        if q4_y == self.rows:
            quadrants[2] = quadrants[3] = False
        elif q4_y - 1 < 0:
            quadrants[0] = quadrants[1] = False
        if q4_x == self.cols:
            quadrants[0] = quadrants[3] = False
        elif q4_x - 1 <0:
            quadrants[1] = quadrants[2] = False

        for order, make_cell in enumerate(quadrants):
            if make_cell and order == 0: # Quadrant 1
                topRight = self.getCell(q4_y - 1, q4_x)
                if not topRight.isLinked(topRight.neighbors['south']) or \
                not topRight.isLinked(topRight.neighbors['west']):
                    return '+'
            if make_cell and order == 1: # Quadrant II
                topLeft = self.getCell(q4_y - 1, q4_x - 1)
                if not topLeft.isLinked(topLeft.neighbors['south']) or \
                not topLeft.isLinked(topLeft.neighbors['east']):
                    return '+'
            if make_cell and order == 2: # Quadrant III
                bottomLeft = self.getCell(q4_y, q4_x - 1)
                if not bottomLeft.isLinked(bottomLeft.neighbors['north']) or \
                not bottomLeft.isLinked(bottomLeft.neighbors['east']):
                    return '+'
            if make_cell and order == 3: # Quadrant IV
                bottomRight = self.getCell(q4_y, q4_x)
                if not bottomRight.isLinked(bottomRight.neighbors['north']) or \
                not bottomRight.isLinked(bottomRight.neighbors['west']):
                    return '+'
        return ' '

    def getCell(self, row: int, col: int) -> Cell:
        if row < 0 or col < 0 or row == self.rows or col == self.cols:
            return # if out of bounds
        else:
            return self.grid[row][col]
    
    def getRandom(self):
        return self.grid[randint(0, self.rows - 1)][randint(0, self.cols - 1)]

    def getSize(self):
        return self.rows*self.cols

    def each_row(self):
        for row in range(self.rows):
            yield self.grid[row]
    
    def each_col(self):
        for col in range(self.cols):
            yield self.grid[col]

    def each_cell(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield self.grid[row][col]
    
    def count_dead_ends(self): # total dead ends in a grid
        return [cell for cell in self.each_cell() if cell.getLinks() == 1]

    def mask(self, row: int, col: int):
        cell = self.getCell(row, col)
        cell.links[None] = True
        for neighbor in cell.getNeighbors():
            if neighbor.isLinked(None):
                cell.link(neighbor)

from recursive_backtracker import recursive_backtracker
grid = Grid(5,5,4)
grid.mask(0,0)
grid.mask(0,1)
grid.mask(1,1)
print(recursive_backtracker(grid))