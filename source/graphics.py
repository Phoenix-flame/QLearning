import pygame as pg


COLOR_WHITE = 255, 255, 255
COLOR_GREEN = 44, 234, 44
COLOR_RED = 236, 43, 43
COLOR_BLUE = 44, 44, 234
COLOR_VISITED = 200, 200, 200
COLOR_FOOD1 = 240, 234, 54
COLOR_FOOD2 = 241, 90, 207
COLOR_FOOD3 = 37, 138, 213

map_state = {0: COLOR_WHITE,
             1: COLOR_GREEN,
             2: COLOR_RED,
             3: COLOR_BLUE
             }


class Graphics:
    def __init__(self, screen, size):

        self.screen = screen
        self.cols = size['col']
        self.rows = size['row']
        self.size = 30
        self.screen = pg.display.set_mode([self.cols*self.size + 5, self.rows*self.size + 5], pg.RESIZABLE)

    def drawCells(self, _map):
        pg.font.init()
        _cell_offset = 5
        myfont = pg.font.SysFont('FreeSans', 20)
        for cell in _map.cells:
            _x1 = (self.size - 0) * cell.x
            _y1 = (self.size - 0) * cell.y


            pg.draw.rect(self.screen, map_state[int(cell.getType())], (_x1 + _cell_offset, _y1 + _cell_offset,
                                                                  self.size - _cell_offset, self.size - _cell_offset))
      

    def drawBoard(self):
        self.screen.fill(COLOR_VISITED)

    def drawLines(self):
        for i in range(self.cols):
            pg.draw.line(self.screen, COLOR_VISITED, (self.size*i, 0), (self.size*i, 500))
        for j in range(self.rows):
            pg.draw.line(self.screen, COLOR_VISITED, (0, self.size*j), (300, self.size*j))

