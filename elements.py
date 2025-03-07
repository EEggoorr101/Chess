import pyray as pr
import raylib
from pieces import *
# chess piece - type of move (0 - line, 1 - knight), dir 1 (-1 - up, 0 - stay, 1 - down), dir 2 (-1 - left, 0 - stay, 1 - right), len - 0 - unlim, other that number

class Player:
    def __init__(self, turned, faction, nick):
        self.nick = nick
        self.turned = turned
        self.f = faction

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

class List:
    def __init__(self, coord, color_fill, color_text, color_boarder, color_hover, color_clicked, color_text_clicked, points, width, height):
        self.coordinates = coord
        self.c1 = color_fill
        self.c2 = color_hover
        self.c3 = color_clicked
        self.c4 = color_boarder
        self.c5 = color_text
        self.c6 = color_text_clicked
        self.points = points
        self.width = width
        self.height = height
        h = self.height // (3 * len(points) - 1)
        self.buttons = []
        x = 0
        for i in points:
            self.buttons.append(Button([coord[0],coord[1]+x],width,h,color_fill,i,color_hover,color_clicked,color_boarder,color_text,h//8*9,color_text_clicked))

    def draw(self):
        for i in self.buttons:
            i.draw()

    def step(self):
        for i in range(len(self.buttons)):
            if (self.buttons[i].step()):
                return i

class Pawn_Promotion_Menu:
    def __init__(self, coord, height, width):
        self.coordinates = coord
        self.c1 = raylib.BLACK
        self.c2 = raylib.GRAY
        self.c3 = raylib.WHITE
        self.c4 = raylib.WHITE
        self.c5 = raylib.WHITE
        self.c6 = raylib.BLACK
        self.points = ['Quinn', 'Rook', 'Bishop', 'Knight']
        self.width = width
        self.height = height
        h = self.height // (3 * len(self.points) - 1)
        self.buttons = []
        x = 0
        for i in self.points:
            self.buttons.append(
                Button([coord[0], coord[1] + x], width, h, self.c1, i, self.c2, self.c3, self.c4,
                       self.c5, h // 9 * 8, self.c6))
            x += h//2*3

    def draw(self):
        for i in self.buttons:
            i.draw()

    def step(self):
        for i in range(len(self.buttons)):
            if (self.buttons[i].step()):
                return i+1
        return 0

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
            self.piece.draw(self.coordinates[0],self.coordinates[1])
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
        self.moved = False
        self.is_over = False
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

    def check(self, player):
        self.drop()
        for i in range(self.num_len):
            for j in range(self.num_len):
                y = self.tiles[i][j]
                if (y.occupied and y.piece.player != player):
                    self.tiles = y.piece.step(i,j,self.tiles)
        for i in self.tiles:
            for j in i:
                if (j.occupied and j.piece.important and j.possible):
                    self.drop()
                    return True
        self.drop()
        return False

    def turn_board(self):
        if (self.num_len % 2 == 1):
            for i in range(self.num_len//2):
                j = self.num_len//2
                self.tiles[i][j].coordinates, self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates = self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates, self.tiles[i][j].coordinates
        for i in range(self.num_len):
            for j in range(self.num_len//2):
                self.tiles[i][j].coordinates, self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates = self.tiles[self.num_len - 1 - i][self.num_len - 1 - j].coordinates, self.tiles[i][j].coordinates

    def draw_board(self):
        for i in range(self.num_len):
            for j in range(self.num_len):
                self.tiles[i][j].draw()
        if (self.chosen != False):
            pr.draw_rectangle(self.tiles[self.chosen[0]][self.chosen[1]].coordinates[0], self.tiles[self.chosen[0]][self.chosen[1]].coordinates[1], self.l, self.l, (255,255,0,100))
            tile = self.tiles[self.chosen[0]][self.chosen[1]]

    def draw(self):
        self.draw_board()
            #if (tile.occupied):
                #tile.piece.draw_pos(self.chosen[0], self.chosen[1], self.tiles)

    #move the piece
    def move(self, player):
        for i in range(self.num_len):
            for j in range(self.num_len):
                if (self.tiles[i][j].possible and self.tiles[i][j].step() and self.event and self.tiles[self.chosen[0]][self.chosen[1]].piece.player == player):
                    if (self.tiles[i][j].occupied and self.tiles[i][j].piece.important):
                        self.is_over = True
                        self.winner = player.nick
                    if (1 in self.tiles[self.chosen[0]][self.chosen[1]].piece.elig and abs(self.chosen[0]-i)==2):
                        if (i < self.chosen[0]):
                            self.tiles[i+1][j].occupied = True
                            self.tiles[0][j].occupied = False
                            self.tiles[i+1][j].piece = self.tiles[0][j].piece
                        else:
                            self.tiles[i - 1][j].occupied = True
                            self.tiles[7][j].occupied = False
                            self.tiles[i - 1][j].piece = self.tiles[7][j].piece
                    self.tiles[i][j].occupied = True
                    self.tiles[self.chosen[0]][self.chosen[1]].occupied = False
                    self.tiles[i][j].piece = self.tiles[self.chosen[0]][self.chosen[1]].piece
                    if (0 in self.tiles[i][j].piece.elig):
                        self.tiles[i][j].piece.elig.remove(0)
                    if (2 in self.tiles[i][j].piece.elig):
                        self.tiles[i][j].piece.elig.remove(2)
                        self.tiles[i][j].piece.moves.pop(-1)
                    self.moved = True
                    self.chosen = False
                    self.event = False
        if (self.event):
            self.chosen = False

    #check of promotions
    def prom(self):
        for i in  range(self.num_len):
            for j in [0,-1]:
                if (self.tiles[i][j].occupied and 3 in self.tiles[i][j].piece.elig):
                    self.moved = False
                    if (not self.chosen):
                        self.chosen = [i,j]
                    return True
        return False

    def step(self, player):
        if (self.prom()):
            self.drop()
        else:
            self.event = pr.is_mouse_button_pressed(0)
            self.drop()
            if (self.chosen != False):
                tile = self.tiles[self.chosen[0]][self.chosen[1]]
                if (tile.occupied):
                    self.tiles = tile.piece.step(self.chosen[0], self.chosen[1], self.tiles)
            self.move(player)
            for i in range(self.num_len):
                for j in range(self.num_len):
                    if (self.tiles[i][j].step() and self.event):
                        self.chosen = [i, j]

class ChessBoard(Board):

    def generate_standart_board(self, players):
        self.tiles[0][0].occupied = True
        self.tiles[0][0].piece = Rook(1, self.tiles[0][0].l, players[1])
        self.tiles[1][0].occupied = True
        self.tiles[1][0].piece = Knight(1, self.tiles[0][0].l, players[1])
        self.tiles[2][0].occupied = True
        self.tiles[2][0].piece = Bishop(1, self.tiles[0][0].l, players[1])
        self.tiles[3][0].occupied = True
        self.tiles[3][0].piece = Quinn(1, self.tiles[0][0].l, players[1])
        self.tiles[4][0].occupied = True
        self.tiles[4][0].piece = King(1, self.tiles[0][0].l, players[1])
        self.tiles[5][0].occupied = True
        self.tiles[5][0].piece = Bishop(1, self.tiles[0][0].l, players[1])
        self.tiles[6][0].occupied = True
        self.tiles[6][0].piece = Knight(1, self.tiles[0][0].l, players[1])
        self.tiles[7][0].occupied = True
        self.tiles[7][0].piece = Rook(1, self.tiles[0][0].l, players[1])
        for i in range(self.num_len):
            self.tiles[i][1].occupied = True
            self.tiles[i][1].piece = Pawn(1, self.tiles[0][0].l, players[1], True)
        self.tiles[0][7].occupied = True
        self.tiles[0][7].piece = Rook(0, self.tiles[0][0].l, players[0])
        self.tiles[1][7].occupied = True
        self.tiles[1][7].piece = Knight(0, self.tiles[0][0].l, players[0])
        self.tiles[2][7].occupied = True
        self.tiles[2][7].piece = Bishop(0, self.tiles[0][0].l, players[0])
        self.tiles[3][7].occupied = True
        self.tiles[3][7].piece = Quinn(0, self.tiles[0][0].l, players[0])
        self.tiles[4][7].occupied = True
        self.tiles[4][7].piece = King(0, self.tiles[0][0].l, players[0])
        self.tiles[5][7].occupied = True
        self.tiles[5][7].piece = Bishop(0, self.tiles[0][0].l, players[0])
        self.tiles[6][7].occupied = True
        self.tiles[6][7].piece = Knight(0, self.tiles[0][0].l, players[0])
        self.tiles[7][7].occupied = True
        self.tiles[7][7].piece = Rook(0, self.tiles[0][0].l, players[0])
        for i in range(self.num_len):
            self.tiles[i][6].occupied = True
            self.tiles[i][6].piece = Pawn(0, self.tiles[0][0].l, players[0])

    def __init__(self, coord, side, players, menu_coord, w, h):
        self.moved = False
        self.is_over = False
        self.coordinate = coord
        self.num_len = 8
        self.l = side // self.num_len
        self.c1 = raylib.WHITE
        self.c2 = raylib.BROWN
        self.tiles = []
        self.chosen = False
        self.pawn_menu = Pawn_Promotion_Menu(menu_coord, w, h)
        for i in range(self.num_len):
            row = []
            for j in range(self.num_len):
                if ((i + j) % 2 == 0):
                    row.append(
                        Tile([self.coordinate[0] + i * self.l, self.coordinate[1] + j * self.l], self.l, self.c1))
                else:
                    row.append(
                        Tile([self.coordinate[0] + i * self.l, self.coordinate[1] + j * self.l], self.l, self.c2))
            self.tiles.append(row.copy())
        self.generate_standart_board(players)

    def draw(self):
        self.draw_board()
        if (self.prom()):
            self.pawn_menu.draw()

    def prommote(self, res):
        for i in  range(self.num_len):
            for j in [0,-1]:
                if (self.tiles[i][j].occupied and 3 in self.tiles[i][j].piece.elig):
                    if (res == 1):
                        piece = self.tiles[i][j].piece
                        self.tiles[i][j].piece = Quinn(piece.color,self.l,piece.player)
                    elif (res == 2):
                        piece = self.tiles[i][j].piece
                        self.tiles[i][j].piece = Rook(piece.color, self.l, piece.player)
                    elif (res == 3):
                        piece = self.tiles[i][j].piece
                        self.tiles[i][j].piece = Bishop(piece.color, self.l, piece.player)
                    elif (res == 4):
                        piece = self.tiles[i][j].piece
                        self.tiles[i][j].piece = Knight(piece.color, self.l, piece.player)
                    self.moved = True
                    self.chosen = False
                    return 0

    def step(self,player):
        self.drop()
        if (self.prom()):
            result = self.pawn_menu.step()
            if (result != 0):
                self.prommote(result)
        else:
            self.event = pr.is_mouse_button_pressed(0)
            if (self.chosen != False):
                tile = self.tiles[self.chosen[0]][self.chosen[1]]
                if (tile.occupied):
                    self.tiles = tile.piece.step(self.chosen[0], self.chosen[1], self.tiles)
            self.move(player)
            for i in range(self.num_len):
                for j in range(self.num_len):
                    if (self.tiles[i][j].step() and self.event):
                        self.chosen = [i, j]