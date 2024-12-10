from collections import Counter


class Path:
    def __init__(self, start):
        self.path = [start]

    def append(self, cell):  # add cell to path
        self.path.append(cell)

    def getCoords(self):  # get only coordinates of path
        for cell in self.path:
            yield cell.coord

    def cleanup(self):  # remove backtracking
        repeats = [item for item, count in Counter(self.path).items() if count > 1]
        for repeat in repeats:
            while self.path.count(repeat) > 1:
                i1 = self.path.index(repeat)
                i2 = self.path.index(repeat, i1 + 1)
                self.path = self.path[:i1] + self.path[i2:]
        return self.path
