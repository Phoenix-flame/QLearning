from source.cell import *
from source.direction import *

class Map:
    def __init__(self, _dir):
        self.map_dir = _dir
        self.map = {}
        self.cols = 0
        self.rows = 0

        self.start_point = None
        self.end_point = None
        self.cells = []
        self.createMap()

        self.n_actions = 4
        self.n_states = self.rows * self.cols
        
       

    def createMap(self):
        with open(self.map_dir) as map_file:
            lines = map_file.readlines()
        id = 0
        for i, line in enumerate(lines):
            self.rows += 1
            line = line.strip()
            line = line.split(',')  ## Check this line
            self.cols = len(line)
            
            for j, cell in enumerate(line):
                self.map[(j, i)] = Cell(j, i, cell, id=id)
                self.cells.append(self.map[(j, i)])
                id += 1
                if cell == '1':
                    self.start_point = self.getCell((j, i))
                elif cell == '3':
                    self.end_point = self.getCell((j, i))



    def getCell(self, x, y):
        return self.map[(x, y)]

    def getCell(self, size):
        return self.map[(size[0], size[1])]


    def getNextCell(self, curCell, direction):
        assert isinstance(curCell, Cell)
        assert isinstance(direction, Direction)
        
        _x = curCell.x
        _y = curCell.y
        if direction == Direction.UP:
            try:
                return self.map[(_x, _y - 1)]
            except KeyError:
                return None
        elif direction == Direction.DOWN:
            try:
                return self.map[(_x, _y + 1)]
            except KeyError:
                return None
        elif direction == Direction.RIGHT:
            try:
                return self.map[(_x + 1, _y)]
            except KeyError:
                return None
        elif direction == Direction.LEFT:
            try:
                return self.map[(_x - 1, _y)]
            except KeyError:
                return None

    def getAdjacents(self, curCell):
        assert isinstance(curCell, Cell)
        
        result = []
        for d in Direction:
            nextCell = self.getNextCell(curCell, d)
            if nextCell is not None:
                result.append(nextCell)
        return result


