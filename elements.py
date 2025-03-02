import pyray as pr
import raylib
from raylib import *
# chess piece - type of move (0 - line, 1 - knight), dir 1 (-1 - up, 0 - stay, 1 - down), dir 2 (-1 - left, 0 - stay, 1 - right)

class Button:
    def __init__(self, corner, width, height, color, text, cwh, cwc, bc,tc,font,tch):
        self.coordinate = corner
        self.w = width
        self.h = height
        self.c = color
        self.t = text
        self.cwh = cwh
        self.cwc = cwc
        self.bc = bc
        self.tc = tc
        self.font = font
        self.tch = tch

    def is_in(self):
        pos = [pr.get_mouse_x(), pr.get_mouse_y()]
        return self.coordinate[0] <= pos[0] <= self.coordinate[0]+self.w and self.coordinate[1] <= pos[1] <= self.coordinate[1]+self.h

    def draw(self):
        pr.draw_rectangle(self.coordinate[0] - 5,self.coordinate[1] - 5,self.w + 10,self.h + 10,self.bc)
        if (self.is_in()):
            if (pr.is_mouse_button_down(0)):
                pr.draw_rectangle(self.coordinate[0],self.coordinate[1],self.w,self.h,self.cwc)
                length = pr.measure_text(self.t, self.font)
                if (length < self.w and self.font < self.h):
                    pr.draw_text(self.t, self.coordinate[0] + (self.w - length) // 2, self.coordinate[1] + (self.h - self.font) // 2, self.font, self.tch)
            else:
                pr.draw_rectangle(self.coordinate[0],self.coordinate[1],self.w,self.h,self.cwh)
                length = pr.measure_text(self.t, self.font)
                if (length < self.w and self.font < self.h):
                    pr.draw_text(self.t, self.coordinate[0] + (self.w - length) // 2, self.coordinate[1] + (self.h - self.font) // 2, self.font, self.tc)
        else:
            pr.draw_rectangle(self.coordinate[0],self.coordinate[1],self.w,self.h,self.c)
            length = pr.measure_text(self.t, self.font)
            if (length < self.w and self.font < self.h):
                pr.draw_text(self.t, self.coordinate[0] + (self.w - length) // 2, self.coordinate[1] + (self.h - self.font) // 2, self.font, self.tc)

    def step(self):
        if (pr.is_mouse_button_released(0) and self.is_in()):
            return True
        return False

class Line:
    def __init__(self, dir1, dir2):
        self.d1 = dir1
        self.d2 = dir2

    def draw(self, i, j, board):
        while True:
            i += self.d1
            j += self.d2
            try:
                t = board[i][j]
                if (t.occupied == True or i<0 or j<0):
                    break
                else:
                    pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.GRAY)
            except:
                break

    def step(self,i,j, board):
        while True:
            i += self.d1
            j += self.d2
            try:
                t = board[i][j]
                if (t.occupied == True or i<0 or j<0):
                    break
                else:
                    t.possible = True
                    board[i][j] = t
            except:
                break
        return board


class Knight:
    def __init__(self):
        pass

class Piece:
    def __init__(self, moves):
        self.moves = moves

    def draw(self, x, y, l):
        pr.draw_rectangle(x,y,l,l,raylib.BLACK)

    def step(self):
        pass

class Tile:
    def __init__(self, coord, side, color):
        self.coordinates = coord
        self.l = side
        self.c = color
        self.occupied = False
        self.piece = False
        self.possible = False

    def is_in(self):
        pos = [pr.get_mouse_x(), pr.get_mouse_y()]
        return self.coordinates[0] <= pos[0] <= self.coordinates[0] + self.l and self.coordinates[1] <= pos[1] <= self.coordinates[1] + self.l

    def draw(self):
        pr.draw_rectangle(self.coordinates[0], self.coordinates[1], self.l, self.l, self.c)
        if (self.occupied):
            self.piece.draw(self.coordinates[0],self.coordinates[1],self.l)
        if (self.is_in()):
            pr.draw_rectangle(self.coordinates[0], self.coordinates[1], self.l, self.l, (0,0,0,70))

    def step(self):
        if (self.is_in()):
            if (pr.is_mouse_button_pressed(0)):
                self.chosen=True
            return True
        return False

class Board:
    def __init__(self,coord,side,color1,color2):
        self.coordinate = coord
        self.l = side//8
        self.c1 = color1
        self.c2 = color2
        self.tiles = []
        self.chosen = False
        for i in range(8):
            row = []
            for j in range(8):
                if ((i+j)%2==0):
                    row.append(Tile([self.coordinate[0]+i*self.l,self.coordinate[1]+j*self.l],self.l,self.c1))
                else:
                    row.append(Tile([self.coordinate[0] + i * self.l, self.coordinate[1] + j * self.l], self.l, self.c2))
            self.tiles.append(row.copy())

    def drop(self):
        for x in self.tiles:
            for y in x:
                y.possible = False

    def draw(self):
        for i in range(8):
            for j in range(8):
                self.tiles[i][j].draw()
        if (self.chosen != False):
            pr.draw_rectangle(self.tiles[self.chosen[0]][self.chosen[1]].coordinates[0], self.tiles[self.chosen[0]][self.chosen[1]].coordinates[1], self.l, self.l, (255,255,0,100))
            tile = self.tiles[self.chosen[0]][self.chosen[1]]
            if (tile.occupied):
                for q in tile.piece.moves:
                    q.draw(self.chosen[0], self.chosen[1], self.tiles)

    def step(self):
        event = pr.is_mouse_button_pressed(0)
        self.drop()
        if (self.chosen != False):
            tile = self.tiles[self.chosen[0]][self.chosen[1]]
            if (tile.occupied):
                for q in tile.piece.moves:
                    self.tiles = q.step(self.chosen[0], self.chosen[1], self.tiles)
        for i in range(8):
            for j in range(8):
                if (self.tiles[i][j].possible and self.tiles[i][j].step() and event):
                    print([i,j],self.chosen)
                    self.tiles[i][j].occupied = True
                    self.tiles[self.chosen[0]][self.chosen[1]].occupied = False
                    self.tiles[i][j].piece = self.tiles[self.chosen[0]][self.chosen[1]].piece
        if (event):
            self.chosen = False
        for i in range(8):
            for j in range(8):
                if (self.tiles[i][j].step() and event):
                    self.chosen = [i, j]