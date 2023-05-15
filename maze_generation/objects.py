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


class Grid: # 2D rectangular grid
    def __init__(self, rows: int, columns: int, shape = 4):
        self.rows = rows
        self.cols = columns
        self.grid = [[0 for c in range(columns)] for r in range(rows)]
        self.borders = {'north': '---', 'south': '---', 'west': '|', 'east': '|',
                        'vdoor': '   ', 'hdoor': ' '}
        self.__prepareGrid(shape)

    def __str__(self):
        final = ''
        for row in self.each_row():
            top = middle = bottom = ''
            for cell in row:
                top, middle, bottom = self._drawCell(top, middle, bottom, cell)
            final += f'{top}\n{middle}\n{bottom}'
        final += self._cornerize(cell.coord[0]+1, cell.coord[1]+1) # most bottom right corner
        return final

    def __prepareGrid(self, shape):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = Cell(row, col)
        for cell in self.each_cell():
            self.__configureCells(cell, shape)

    def __configureCells(self, cell, shape):
        row, col = cell.coord
        if shape == 3:
            if sum(cell.coord) % 2:
                cell.neighbors['north'] = self.getCell(row-1, col)
                cell.neighbors['southeast'] = self.getCell(row, col+1)
                cell.neighbors['southwest'] = self.getCell(row, col-1)
            else:
                cell.neighbors['south'] = self.getCell(row+1, col)
                cell.neighbors['northeast'] = self.getCell(row, col+1)
                cell.neighbors['northwest'] = self.getCell(row, col-1)
        elif shape == 4:
            cell.neighbors['north'] = self.getCell(row-1, col)
            cell.neighbors['south'] = self.getCell(row+1, col)
            cell.neighbors['west'] = self.getCell(row, col-1)
            cell.neighbors['east'] = self.getCell(row, col+1)
        elif shape == 6:
            north_diagonal = (lambda r, c: r-1 if c%2 else r)(row, col)
            south_diagonal = (lambda r, c: r if c%2 else r+1)(row, col)
            cell.neighbors['north'] = self.getCell(row-1, col)
            cell.neighbors['south'] = self.getCell(row+1, col)
            cell.neighbors['northwest'] = self.getCell(north_diagonal, col-1)
            cell.neighbors['southwest'] = self.getCell(south_diagonal, col-1)
            cell.neighbors['northeast'] = self.getCell(north_diagonal, col+1)
            cell.neighbors['southeast'] = self.getCell(south_diagonal, col+1)

    def _drawCell(self, top, middle, bottom, cell):
        top += self._cornerize(cell.coord[0], cell.coord[1])
        top += self._drawBorder(cell, 'north') # draw top wall
        middle += self._drawBorder(cell, 'west') # draw left wall
        middle += '   ' # draw cellular space
        if cell.coord[0] == self.rows-1: # if last row
            bottom += self._cornerize(cell.coord[0]+1, cell.coord[1])
            bottom += self._drawBorder(cell, 'south') # draw bottom wall
        if cell.coord[1] == self.cols-1: # if last column
            top += self._cornerize(cell.coord[0], cell.coord[1]+1)
            middle += self._drawBorder(cell, 'east') # draw right wall
        return top, middle, bottom
    
    def _drawBorder(self, cell: Cell, direction: str):
        if (direction in cell.neighbors.keys() and not cell.isLinked(cell.neighbors[direction])):
            return self.borders[direction]
        if len(direction) == 5: # north / south
            return self.borders['vdoor']
        else: # horizontal / diagonal
            return self.borders['hdoor']

    def _cornerize(self, y: int, x: int) -> str: # given two diagonal cells
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
                upRight = self.getCell(y - 1, x)
                if not upRight.isLinked(upRight.neighbors['south']) or \
                not upRight.isLinked(upRight.neighbors['west']):
                    return '+'
            if make_cell and order == 1: # Quadrant II
                upLeft = self.getCell(y - 1, x - 1)
                if not upLeft.isLinked(upLeft.neighbors['south']) or \
                not upLeft.isLinked(upLeft.neighbors['east']):
                    return '+'
            if make_cell and order == 2: # Quadrant III
                downLeft = self.getCell(y, x - 1)
                if not downLeft.isLinked(downLeft.neighbors['north']) or \
                not downLeft.isLinked(downLeft.neighbors['east']):
                    return '+'
            if make_cell and order == 3: # Quadrant IV
                downRight = self.getCell(y, x)
                if not downRight.isLinked(downRight.neighbors['north']) or \
                not downRight.isLinked(downRight.neighbors['west']):
                    return '+'
        return ' '

    def getCell(self, row: int, col: int) -> Cell:
        if row < 0 or col < 0 or row == self.rows or col == self.cols:
            return # if out of bounds
        else:
            return self.grid[row][col]
    
    def getRandom(self):
        while (True):
            cell = self.grid[randint(0, self.rows - 1)][randint(0, self.cols - 1)]
            if not cell.isLinked(None):
                return cell

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

    def mask(self, row: int, col: int): # do not use masking with binary trees, sidewinder
        cell = self.getCell(row, col)
        cell.links[None] = True
        for neighbor in cell.getNeighbors():
            if neighbor.isLinked(None):
                cell.link(neighbor)


class TriGrid(Grid): # 2D triangular grid
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, shape = 3)
        self.borders = {'north': '---', 'south': '---', 'northwest': ' /', 'northeast': ' \\',
                        'southwest': ' \\', 'southeast': ' /', 'vdoor': '   ', 'hdoor': '  '}
 
    def __str__(self):
        final = ''
        for row in self.each_row():
            top = '  '; bottom = middle = ''
            for cell in row:
                top, middle, bottom = self._drawCell(top, middle, bottom, cell)
            final += f'{top}\n{middle}\n'
        final += bottom
        return final

    def _drawCell(self, top, middle, bottom, cell):
        if cell.coord[0] % 2 and cell.coord[1] == 0: # even rows, first column
            top, bottom = bottom, top
        if sum(cell.coord) % 2:
            #top += 'o'
            top += self._cornerize(cell.coord[0], cell.coord[1] - 1)
            top += self._drawBorder(cell, 'north') # draw top wall
            middle += self._drawBorder(cell, 'southwest') # draw left wall
        else:
            middle += self._drawBorder(cell, 'northwest') # draw left wall
            if cell.coord[0] == self.rows-1: # if last row
                #bottom += '0' # leftmost corners
                bottom += self._cornerize(cell.coord[0] + 1, cell.coord[1] - 1)          
                bottom += self._drawBorder(cell, 'south')
        if cell.coord[1] == self.cols-1: # if last column
            #top += 'x'
            if sum(cell.coord) % 2: # draw right wall
                top += self._cornerize(cell.coord[0], cell.coord[1] + 1)
                middle += self._drawBorder(cell, 'southeast')
            else:
                top += self._cornerize(cell.coord[0], cell.coord[1])
                middle += self._drawBorder(cell, 'northeast')
        if cell.coord[1] == self.cols-1 and cell.coord[0] == self.rows-1: # if last cell
            #bottom += '+'
            if sum(cell.coord) % 2: 
                bottom += self._cornerize(cell.coord[0] + 1, cell.coord[1])
            else:
                bottom += self._cornerize(cell.coord[0] + 1, cell.coord[1] + 1)
        return top, middle, bottom

    def _cornerize(self, y: int, x: int) -> str: # given two diagonal cells
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
                downMid = self.getCell(y, x)
                if not downMid.isLinked(downMid.neighbors['northwest']) or \
                not downMid.isLinked(downMid.neighbors['northeast']):
                    return 'x'
            if make_cell and order == 1:
                downRight = self.getCell(y, x + 1)
                if not downRight.isLinked(downRight.neighbors['north']) or \
                not downRight.isLinked(downRight.neighbors['southwest']):
                    return 'x'
            if make_cell and order == 2:
                upRight = self.getCell(y - 1, x + 1)
                if not upRight.isLinked(upRight.neighbors['south']) or \
                not upRight.isLinked(upRight.neighbors['northeast']):
                    return 'x'
            if make_cell and order == 3:
                upMid = self.getCell(y - 1, x)
                if not upMid.isLinked(upMid.neighbors['southeast']) or \
                not upMid.isLinked(upMid.neighbors['southwest']):
                    return 'x'
            if make_cell and order == 4:
                upLeft = self.getCell(y - 1, x - 1)
                if not upLeft.isLinked(upLeft.neighbors['northeast']) or \
                not upLeft.isLinked(upLeft.neighbors['south']):
                    return 'x'
            if make_cell and order == 5:
                downLeft = self.getCell(y, x - 1)
                if not downLeft.isLinked(downLeft.neighbors['north']) or \
                not downLeft.isLinked(downLeft.neighbors['southwest']):
                    return 'x'

        return ' '

class HexGrid(Grid): # 2D hexagonal grid
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, shape = 6)
        '''
               x---x
              /     \\
         x---x       x---x
        /     \\    /     \\
       x       x---x       x
        \     /     \\    /
         x---x       x---x
        /     \\    /     \\
       x       x---x       x
       \\     /     \\    /
         x---x       x---x
              \\    /
               x---x
'''


from recursive_backtracker import recursive_backtracker
grid = TriGrid(4,4)
print(grid)
grid.mask(3,3)
grid.mask(1,1)
print(recursive_backtracker(grid))