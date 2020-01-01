from enum import Enum


class CellType(Enum):
    WHITE = 0
    GREEN = 1
    RED = 2
    BLUE = 3


class Cell:
    def __init__(self, x, y, cellType=0, free=True):
        self.x = x
        self.y = y
        self.cellType = cellType


    def getType(self):
        return self.cellType

    def getKey(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + self.cellType + "]"



