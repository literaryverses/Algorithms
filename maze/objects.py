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


class Grid: # orthogonal maze
    def __init__(self, rows: int, columns: int, shape = 4):
        self.rows = rows
        self.cols = columns
        self.grid = [[0 for c in range(columns)] for r in range(rows)]
        self.borders = {'north': '---', 'south': '---', 'west': '|', 'east': '|',
                        'vdoor': '   ', 'hdoor': ' '}
        self.__prepareGrid(shape)

    def __str__(self):
        maze = ''
        for row in self.each_row():
            row_layout = ['']*3
            for cell in row:
                row_layout = self._drawCell(row_layout, cell)
            maze += '\n'.join(row_layout)
        return maze

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
            north_diagonal = (lambda r, c: r if c%2 else r-1)(row, col)
            south_diagonal = (lambda r, c: r+1 if c%2 else r)(row, col)
            cell.neighbors['north'] = self.getCell(row-1, col)
            cell.neighbors['south'] = self.getCell(row+1, col)
            cell.neighbors['northwest'] = self.getCell(north_diagonal, col-1)
            cell.neighbors['southwest'] = self.getCell(south_diagonal, col-1)
            cell.neighbors['northeast'] = self.getCell(north_diagonal, col+1)
            cell.neighbors['southeast'] = self.getCell(south_diagonal, col+1)

    def _drawCell(self, row_layout, cell):
        top, middle, bottom = row_layout[0], row_layout[1], row_layout[2]
        top += self._cornerize(cell.coord[0], cell.coord[1])
        top += self._drawBorder(cell, 'north') # draw top wall
        middle += f"{self._drawBorder(cell, 'west')}   "
        if cell.coord[0] == self.rows-1: # if last row
            bottom += self._cornerize(cell.coord[0]+1, cell.coord[1])
            bottom += self._drawBorder(cell, 'south') # draw bottom wall
        if cell.coord[1] == self.cols-1: # if last column
            top += self._cornerize(cell.coord[0], cell.coord[1]+1)
            middle += self._drawBorder(cell, 'east') # draw right wall
        if sum(cell.coord) == self.cols + self.rows - 2: # last cell
            bottom += self._cornerize(self.rows, self.cols)
        return [top, middle, bottom]
    
    def _drawBorder(self, cell: Cell, direction: str) -> str:
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
                upRight = self.getCell(y-1, x)
                if not upRight.isLinked(upRight.neighbors['south']) or \
                not upRight.isLinked(upRight.neighbors['west']):
                    return '+'
            elif make_cell and order == 1: # Quadrant II
                upLeft = self.getCell(y-1, x-1)
                if not upLeft.isLinked(upLeft.neighbors['south']) or \
                not upLeft.isLinked(upLeft.neighbors['east']):
                    return '+'
            elif make_cell and order == 2: # Quadrant III
                downLeft = self.getCell(y, x-1)
                if not downLeft.isLinked(downLeft.neighbors['north']) or \
                not downLeft.isLinked(downLeft.neighbors['east']):
                    return '+'
            elif make_cell and order == 3: # Quadrant IV
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
            cell = self.grid[randint(0, self.rows-1)][randint(0, self.cols-1)]
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


class TriGrid(Grid): # delta grid
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, shape = 3)
        self.borders = {'north': '---', 'south': '---', 'northwest': ' /', 'northeast': ' \\',
                        'southwest': ' \\', 'southeast': ' /', 'vdoor': '   ', 'hdoor': '  '}
        
    def _drawCell(self, row_layout, cell):
        top, middle, bottom = row_layout[0], row_layout[1], row_layout[2]
        if sum(cell.coord) % 2:
            top += self._drawBorder(cell, 'north') # draw top wall
            top += self._cornerize(cell.coord[0], cell.coord[1]+1)
            middle += self._drawBorder(cell, 'southwest')
            middle += self._drawBorder(cell, 'southeast') # draw right wall
            if cell.coord[0] == self.rows-1 and cell.coord[1] == 0: # if 1st cell in last row
                bottom = self._drawBorder(cell, 'spaces')
            if sum(cell.coord) == self.rows + self.cols - 2: # if last cell
                bottom += self._cornerize(cell.coord[0]+1, cell.coord[1])
        else: # if is pointy
            if cell.coord[1] == 0 or cell.coord[0] == self.rows-1:
                bottom += self._cornerize(cell.coord[0]+1, cell.coord[1]-1)
            if cell.coord[1] == 0: # if 1st column
                top += self._drawBorder(cell, 'spaces')
                top += self._cornerize(cell.coord[0], cell.coord[1])
                middle += self._drawBorder(cell, 'northwest')
            if cell.coord[0] == self.rows-1: # if last row
                bottom += self._drawBorder(cell,'south')
            if cell.coord[1] == self.cols-1: # if last column
                middle += self._drawBorder(cell, 'northeast') # draw right wall
            if sum(cell.coord) == self.rows + self.cols - 2: # if last cell
                bottom += self._cornerize(cell.coord[0]+1, cell.coord[1]+1)
        return [top, middle, bottom]

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
            elif make_cell and order == 1:
                downRight = self.getCell(y, x+1)
                if not downRight.isLinked(downRight.neighbors['north']) or \
                not downRight.isLinked(downRight.neighbors['southwest']):
                    return 'x'
            elif make_cell and order == 2:
                upRight = self.getCell(y-1, x+1)
                if not upRight.isLinked(upRight.neighbors['south']) or \
                not upRight.isLinked(upRight.neighbors['northwest']):
                    return 'x'
            elif make_cell and order == 3:
                upMid = self.getCell(y-1, x)
                if not upMid.isLinked(upMid.neighbors['southeast']) or \
                not upMid.isLinked(upMid.neighbors['southwest']):
                    return 'x'
            elif make_cell and order == 4:
                upLeft = self.getCell(y-1, x-1)
                if not upLeft.isLinked(upLeft.neighbors['northeast']) or \
                not upLeft.isLinked(upLeft.neighbors['south']):
                    return 'x'
            elif make_cell and order == 5:
                downLeft = self.getCell(y, x-1)
                if not downLeft.isLinked(downLeft.neighbors['north']) or \
                not downLeft.isLinked(downLeft.neighbors['southeast']):
                    return 'x'
        return ' '

class HexGrid(Grid): # sigma maze
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, shape = 6)

    def __str__(self):
        template = TriGrid(2*self.rows+1, self.cols*3)
        self.__hexify(template)
        for row in self.each_row():
            for cell in row:
                template = self.__reformat(cell, template)
        return str(template)
    
    # link up triangular grid to match the links of hexagonal maze
    def __reformat(self, hex_cell: Cell, tri_grid: TriGrid) -> TriGrid:
        for direction in hex_cell.neighbors.keys():
            if hex_cell.isLinked(hex_cell.neighbors[direction]):
                triangle = self.__getTriangle(hex_cell, direction, tri_grid)
                triangle.link(triangle.neighbors[direction])
        return tri_grid

    # returns corresponding triangular cell according to direction of hexagonal cell
    def __getTriangle(self, hex_cell: Cell, direction: str, tri_grid: TriGrid) -> Cell:
        row, col = hex_cell.coord
        adjust = (lambda c: 1 if c%2 else 0)(col)
        if direction == 'northwest':
            return tri_grid.getCell(2*row+adjust, 3*col)
        elif direction == 'north':
            return tri_grid.getCell(2*row+adjust, 3*col+1)
        elif direction == 'northeast':
            return tri_grid.getCell(2*row+adjust, 3*col+2)
        elif direction == 'southeast':
            return tri_grid.getCell(2*row+adjust+1, 3*col+2)
        elif direction == 'south':
            return tri_grid.getCell(2*row+adjust+1, 3*col+1)
        elif direction == 'southwest':
            return tri_grid.getCell(2*row+adjust+1, 3*col)
    
    # create hexagonal grid from triangular grid
    def __hexify(self, template: TriGrid):
        y = x = 0
        for _ in range(self.rows*self.cols): # make sigma maze
            if x == 3*self.cols:
                x = 0; y += 2 # reset coord
            if x % 2:
                self.__linkUp(template, y+1, x)
                if y == 0:
                    self.__maskUp(template, y, x, True)
            else:
                self.__linkUp(template, y, x)
                if y == 2*self.rows-2:
                    self.__maskUp(template, y, x, False)
            x += 3

    # link triangular cells into hexagonal cell
    def __linkUp(self, template: TriGrid, row: int, col: int):
        current = template.getCell(row, col)
        for _x in range(1,3):
            temp, current = current, template.getCell(row, col+_x)
            temp.link(current)
        for _x in range(2,-1,-1):
            temp, current = current, template.getCell(row+1, col+_x)
            temp.link(current)
        current.link(template.getCell(row, col))

    # mask triangular cells so only hexagonal cells remain
    def __maskUp(self, template: TriGrid, row: int, col: int, isAbove: bool):
        _y = (lambda _: 0 if _ else 2)(isAbove)
        for _x in range(3):
            template.mask(row+_y, col+_x)
