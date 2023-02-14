from random import randint

class Cell:
    def __init__(self, row, column):
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
        return self.links.keys

    def isLinked(self, cell):
        return self.links[cell]

    def getNeighbors(self):
        return self.neighbors.values

    def setNeighbor(self, cell, direction):
        self.neighbors[direction] = cell

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.grid[rows][columns]
        self.prepareGrid()

    def prepareGrid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = Cell(row, col)
        for cell in self.each_cell():
            self.configureCells(cell)

    def configureCells(self, cell):
        row, col = cell.coord
        cell.neighbors['north'] = self.getCell(row-1, col)
        cell.neighbors['south'] = self.getCell(row+1, col)
        cell.neighbors['west'] = self.getCell(row, col-1)
        cell.neighbors['east'] = self.getCell(row, col+1)

    def getCell(self, row, col):
        if row < 0 or col < 0 or row > self.rows or col > self.cols:
            return None # if out of bounds
        else:
            return self.grid[row][col]
    
    def getRandom(self):
        return self[randint(0, self.rows)][randint(0, self.cols)]

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