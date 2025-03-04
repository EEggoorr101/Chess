import pyray as pr
import raylib
from raylib import *
# chess piece - type of move (0 - line, 1 - knight), dir 1 (-1 - up, 0 - stay, 1 - down), dir 2 (-1 - left, 0 - stay, 1 - right), len - 0 - unlim, other that number

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
    def __init__(self, dir1, dir2, len):
        self.d1 = dir1
        self.d2 = dir2
        self.l = len
        self.cl = Capture_Line(dir1,dir2,len)
        self.fl = Free_Line(dir1, dir2, len)

    def draw(self, i, j, board):
        self.cl.draw(i, j, board)
        self.fl.draw(i, j, board)

    def step(self,i,j, board):
        board = self.cl.step(i, j, board)
        board = self.fl.step(i, j, board)
        return board

class Capture_Line:
    def __init__(self, dir1, dir2, len):
        self.d1 = dir1
        self.d2 = dir2
        self.l = len

    def draw(self, i, j, board):
        if (self.l == 0):
            while True:
                i += self.d1
                j += self.d2
                try:
                    t = board[i][j]
                    if (i < 0 or j < 0):
                        break
                    elif (t.occupied == True):
                        pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.RED)
                        break
                    else:
                        continue
                except:
                    break
        else:
            for q in range(self.l):
                i += self.d1
                j += self.d2
                try:
                    t = board[i][j]
                    if (i < 0 or j < 0):
                        break
                    elif (t.occupied == True):
                        pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.RED)
                        break
                    else:
                        continue
                except:
                    break

    def step(self, i, j, board):
        if (self.l == 0):
            while True:
                i += self.d1
                j += self.d2
                try:
                    t = board[i][j]
                    if (i < 0 or j < 0):
                        break
                    elif (t.occupied == True):
                        t.possible = True
                        board[i][j] = t
                        break
                    else:
                        continue
                except:
                    break
        else:
            for q in range(self.l):
                i += self.d1
                j += self.d2
                try:
                    t = board[i][j]
                    if (i < 0 or j < 0):
                        break
                    elif (t.occupied == True):
                        t.possible = True
                        board[i][j] = t
                        break
                    else:
                        continue
                except:
                    break
        return board

class Free_Line:
    def __init__(self, dir1, dir2, len):
        self.d1 = dir1
        self.d2 = dir2
        self.l = len

    def draw(self, i, j, board):
        if (self.l == 0):
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
        else:
            for q in range(self.l):
                i += self.d1
                j += self.d2
                try:
                    t = board[i][j]
                    if (t.occupied == True or i < 0 or j < 0):
                        break
                    else:
                        pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.GRAY)
                except:
                    break

    def step(self,i,j, board):
        if (self.l == 0):
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
        else:
            for q in range(self.l):
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


class Jump:
    #0,1,2,3 - directions (0 - up, else clockwise); 0-both, -1,1 only one(-1, left; 1, right); len1 - distance of jump, len2
    def __init__(self, dir1, dir2, len1, len2):
        self.d1 = dir1
        self.d2 = dir2
        self.l1 = len1
        self.l2 = len2
        self.cj = Capture_Jump(dir1, dir2, len1, len2)
        self.fj = Free_Jump(dir1, dir2, len1, len2)

    def draw(self, i, j, board):
        self.cj.draw(i, j, board)
        self.fj.draw(i, j, board)

    def step(self, i, j, board):
        board = self.cj.step(i, j, board)
        board = self.fj.step(i, j, board)
        return board

class Capture_Jump:
    def __init__(self, dir1, dir2, len1, len2):
        self.d1 = dir1
        self.d2 = dir2
        self.l1 = len1
        self.l2 = len2

    def draw(self, i, j, board):
            if (self.d1 == 0):
                j -= self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i+self.l2][j]
                        if (j < 0 or i+self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i-self.l2][j]
                        if (j < 0 or i-self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.RED))
                    except:
                        pass
            elif (self.d1 == 1):
                i += self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i][j + self.l2]
                        if (i < 0 or j + self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i][j - self.l2]
                        if (i < 0 or j - self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
            elif (self.d1 == 2):
                j += self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i - self.l2][j]
                        if (j < 0 or i - self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i + self.l2][j]
                        if (j < 0 or i + self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
            else:
                i -= self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i][j - self.l2]
                        if (i < 0 or j - self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i][j + self.l2]
                        if (i < 0 or j + self.l2 < 0):
                            pass
                        elif (t.occupied == True):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass

    def step(self,i,j,board):
        if (self.d1 == 0):
            j -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i + self.l2][j]
                    if (j < 0 or i + self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i + self.l2][j] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i - self.l2][j]
                    if (j < 0 or i - self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i - self.l2][j] = t
                except:
                    pass
        elif (self.d1 == 1):
            i += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j + self.l2]
                    if (i < 0 or j + self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i][j + self.l2] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j - self.l2]
                    if (i < 0 or j - self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i][j - self.l2] = t
                except:
                    pass
        elif (self.d1 == 2):
            j += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i - self.l2][j]
                    if (j < 0 or i - self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i - self.l2][j] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i + self.l2][j]
                    if (j < 0 or i + self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i + self.l2][j] = t
                except:
                    pass
        else:
            i -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j - self.l2]
                    if (i < 0 or j - self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i][j - self.l2] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j + self.l2]
                    if (i < 0 or j + self.l2 < 0):
                        pass
                    elif (t.occupied == True):
                        t.possible = True
                        board[i][j + self.l2] = t
                except:
                    pass
        return board

class Free_Jump:
    def __init__(self, dir1, dir2, len1, len2):
        self.d1 = dir1
        self.d2 = dir2
        self.l1 = len1
        self.l2 = len2

    def draw(self, i, j, board):
            if (self.d1 == 0):
                j -= self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i+self.l2][j]
                        if (t.occupied == True or j < 0 or i+self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.GRAY))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i-self.l2][j]
                        if (t.occupied == True or j < 0 or i-self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.GRAY))
                    except:
                        pass
            elif (self.d1 == 1):
                i += self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i][j + self.l2]
                        if (t.occupied == True or i < 0 or j + self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.GRAY))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i][j - self.l2]
                        if (t.occupied == True or i < 0 or j - self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.GRAY))
                    except:
                        pass
            elif (self.d1 == 2):
                j += self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i - self.l2][j]
                        if (t.occupied == True or j < 0 or i - self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.GRAY))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i + self.l2][j]
                        if (t.occupied == True or j < 0 or i + self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.GRAY))
                    except:
                        pass
            else:
                i -= self.l1
                if (self.d2 != -1):
                    try:
                        t = board[i][j - self.l2]
                        if (t.occupied == True or i < 0 or j - self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.GRAY))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i][j + self.l2]
                        if (t.occupied == True or i < 0 or j + self.l2 < 0):
                            pass
                        else:
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.GRAY))
                    except:
                        pass

    def step(self,i,j,board):
        if (self.d1 == 0):
            j -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i + self.l2][j]
                    if (t.occupied == False or j < 0 or i + self.l2 < 0):
                        t.possible = True
                        board[i + self.l2][j] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i - self.l2][j]
                    if (t.occupied == False or j < 0 or i - self.l2 < 0):
                        t.possible = True
                        board[i - self.l2][j] = t
                except:
                    pass
        elif (self.d1 == 1):
            i += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j + self.l2]
                    if (t.occupied == False or i < 0 or j + self.l2 < 0):
                        t.possible = True
                        board[i][j + self.l2] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j - self.l2]
                    if (t.occupied == False or i < 0 or j - self.l2 < 0):
                        t.possible = True
                        board[i][j - self.l2] = t
                except:
                    pass
        elif (self.d1 == 2):
            j += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i - self.l2][j]
                    if (t.occupied == False or j < 0 or i - self.l2 < 0):
                        t.possible = True
                        board[i - self.l2][j] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i + self.l2][j]
                    if (t.occupied == False or j < 0 or i + self.l2 < 0):
                        t.possible = True
                        board[i + self.l2][j] = t
                except:
                    pass
        else:
            i -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j - self.l2]
                    if (t.occupied == False or i < 0 or j - self.l2 < 0):
                        t.possible = True
                        board[i][j - self.l2] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j + self.l2]
                    if (t.occupied == False or i < 0 or j + self.l2 < 0):
                        t.possible = True
                        board[i][j + self.l2] = t
                except:
                    pass
        return board

class Piece:
    def __init__(self, moves):
        self.moves = moves

    def draw(self, x, y, l):
        pr.draw_rectangle(x,y,l,l,raylib.BLACK)

    def draw_pos(self,i,j,board):
        for q in self.moves:
            q.draw(i, j, board)

    def step(self, i,j,board):
        for q in self.moves:
            board = q.step(i, j, board)
        return board

class Quinn(Piece):
    def __init__(self):
        self.moves = [Line(1,1,0),Line(-1,-1,0),Line(-1,1,0),Line(1,-1,0),Line(-1,0,0),Line(0,-1,0),Line(0,1,0),Line(1,0,0)]

class Knight(Piece):
    def __init__(self):
        self.moves = [Jump(0,0,2,1),Jump(1,0,2,1),Jump(2,0,2,1),Jump(3,0,2,1)]

class Bishop(Piece):
    def __init__(self):
        self.moves = [Line(1,1,0),Line(-1,-1,0),Line(-1,1,0),Line(1,-1,0)]

class Rook(Piece):
    def __init__(self):
        self.moves = [Line(-1,0,0),Line(0,-1,0),Line(0,1,0),Line(1,0,0)]

class King(Piece):
    def __init__(self):
        self.moves = [Line(1,1,1),Line(-1,-1,1),Line(-1,1,1),Line(1,-1,1),Line(-1,0,1),Line(0,-1,1),Line(0,1,1),Line(1,0,1)]

#need is_turned(turned - black; not turned - white)
class Pawn(Piece):
    def __init__(self,is_turned = False):
        if (is_turned):
            self.moves = [Capture_Line(-1, 1, 1), Capture_Line(1, 1, 1), Free_Line(0, 1, 1)]
        else:
            self.moves = [Capture_Line(1,-1,1),Capture_Line(-1,-1,1),Free_Line(0,-1,1)]

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
        if (self.possible and self.occupied):
            pr.draw_circle(self.coordinates[0] + self.l // 2, self.coordinates[1] + self.l // 2, 10, raylib.RED)
        elif (self.possible):
            pr.draw_circle(self.coordinates[0] + self.l // 2, self.coordinates[1] + self.l // 2, 10, raylib.GRAY)

    def step(self):
        if (self.is_in()):
            if (pr.is_mouse_button_pressed(0)):
                self.chosen=True
            return True
        return False

class Board:
    def __init__(self,coord,side,color1,color2,num_len):
        self.coordinate = coord
        self.num_len = num_len
        self.l = side//self.num_len
        self.c1 = color1
        self.c2 = color2
        self.tiles = []
        self.chosen = False
        for i in range(self.num_len):
            row = []
            for j in range(self.num_len):
                if ((i+j)%2==0):
                    row.append(Tile([self.coordinate[0]+i*self.l,self.coordinate[1]+j*self.l],self.l,self.c1))
                else:
                    row.append(Tile([self.coordinate[0] + i * self.l, self.coordinate[1] + j * self.l], self.l, self.c2))
            self.tiles.append(row.copy())

    def drop(self):
        for x in self.tiles:
            for y in x:
                y.possible = False

    def turn_board(self):
        if (self.num_len % 2 == 1):
            for i in range(self.num_len//2):
                j = self.num_len//2
                self.tiles[i][j].coordinates, self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates = self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates, self.tiles[i][j].coordinates
        for i in range(self.num_len):
            for j in range(self.num_len//2):
                self.tiles[i][j].coordinates, self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates = self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates, self.tiles[i][j].coordinates

    def draw(self):
        for i in range(self.num_len):
            for j in range(self.num_len):
                self.tiles[i][j].draw()
        if (self.chosen != False):
            pr.draw_rectangle(self.tiles[self.chosen[0]][self.chosen[1]].coordinates[0], self.tiles[self.chosen[0]][self.chosen[1]].coordinates[1], self.l, self.l, (255,255,0,100))
            tile = self.tiles[self.chosen[0]][self.chosen[1]]
            #if (tile.occupied):
                #tile.piece.draw_pos(self.chosen[0], self.chosen[1], self.tiles)

    def step(self):
        event = pr.is_mouse_button_pressed(0)
        self.drop()
        if (self.chosen != False):
            tile = self.tiles[self.chosen[0]][self.chosen[1]]
            if (tile.occupied):
                tile.piece.step(self.chosen[0], self.chosen[1], self.tiles)
        for i in range(self.num_len):
            for j in range(self.num_len):
                if (self.tiles[i][j].possible and self.tiles[i][j].step() and event):
                    self.tiles[i][j].occupied = True
                    self.tiles[self.chosen[0]][self.chosen[1]].occupied = False
                    self.tiles[i][j].piece = self.tiles[self.chosen[0]][self.chosen[1]].piece
                    self.chosen = False
                    event = False
        if (event):
            self.chosen = False
        for i in range(self.num_len):
            for j in range(self.num_len):
                if (self.tiles[i][j].step() and event):
                    self.chosen = [i, j]