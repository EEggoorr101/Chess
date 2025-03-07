import pyray as pr
import raylib
from elements import *

class Castle:
    #eligibility is 0-to move,1-to swap,2-for king
    def __init__(self):
        pass

    def drop(self, i, j, board, player):
        pass

    def step(self, i, j, board, player):
        x = 0

        while True:
            try:
                if (board[x][j].occupied and 0 in board[x][j].piece.elig and board[x][j].piece.player.f == player.f):
                    if (x < i):
                        check = True
                        for y in range(x+1,i):
                            if (board[y][j].occupied):
                                check = False
                                break
                        if check:
                            board[i-2][j].possible = True
                            if (not 1 in board[i][j].piece.elig):
                                board[i][j].piece.elig.append(1)
                    else:
                        check = True
                        for y in range(i + 1, x):
                            if (board[y][j].occupied):
                                check = False
                                break
                        if check:
                            board[i + 2][j].possible = True
                            if (not 1 in board[i][j].piece.elig):
                                board[i][j].piece.elig.append(1)
                x += 1
            except:
                break
        return board

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

    def step(self,i,j, board, player):
        board = self.cl.step(i, j, board, player)
        board = self.fl.step(i, j, board, player)
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

    def step(self, i, j, board, player):
        if (self.l == 0):
            while True:
                i += self.d1
                j += self.d2
                try:
                    t = board[i][j]
                    if (i < 0 or j < 0):
                        break
                    elif (t.occupied == True and player.f == t.piece.player.f):
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
                    elif (t.occupied == True and player.f == t.piece.player.f):
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

    def step(self,i,j, board, color):
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

    def step(self, i, j, board, player):
        board = self.cj.step(i, j, board, player)
        board = self.fj.step(i, j, board, player)
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
                        elif (t.occupied == True and color != t.piece.color):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10, raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i-self.l2][j]
                        if (j < 0 or i-self.l2 < 0):
                            pass
                        elif (t.occupied == True and color != t.piece.color):
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
                        elif (t.occupied == True and color != t.piece.color):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i][j - self.l2]
                        if (i < 0 or j - self.l2 < 0):
                            pass
                        elif (t.occupied == True and color != t.piece.color):
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
                        elif (t.occupied == True and color != t.piece.color):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i + self.l2][j]
                        if (j < 0 or i + self.l2 < 0):
                            pass
                        elif (t.occupied == True and color != t.piece.color):
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
                        elif (t.occupied == True and color != t.piece.color):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass
                if (self.d2 != 1):
                    try:
                        t = board[i][j + self.l2]
                        if (i < 0 or j + self.l2 < 0):
                            pass
                        elif (t.occupied == True and color != t.piece.color):
                            pr.draw_circle(pr.draw_circle(t.coordinates[0] + t.l // 2, t.coordinates[1] + t.l // 2, 10,
                                                          raylib.RED))
                    except:
                        pass

    def step(self,i,j,board,player):
        if (self.d1 == 0):
            j -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i + self.l2][j]
                    if (t.occupied == True and player.f != t.piece.player.f and j>=0 and i + self.l2 >= 0):
                        board[i + self.l2][j].possible = True
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i - self.l2][j]
                    if (t.occupied == True and player.f != t.piece.player.f and j>=0 and i - self.l2 >= 0):
                        board[i - self.l2][j].possible = True
                except:
                    pass
        elif (self.d1 == 1):
            i += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j + self.l2]
                    if (t.occupied == True and player.f != t.piece.player.f and i>=0 and j + self.l2 >= 0):
                        board[i][j + self.l2].possible = True
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j - self.l2]
                    if (t.occupied == True and player.f != t.piece.player.f and i>=0 and j - self.l2>=0):
                        board[i][j - self.l2].possible = True
                except:
                    pass
        elif (self.d1 == 2):
            j += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i - self.l2][j]
                    if (t.occupied == True and player.f != t.piece.player.f and j>=0 and i - self.l2 >= 0):
                        board[i - self.l2][j].possible = True
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i + self.l2][j]
                    if (t.occupied == True and player.f != t.piece.player.f and j>=0 and i + self.l2 >= 0):
                        board[i + self.l2][j].possible = True
                except:
                    pass
        else:
            i -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j - self.l2]
                    if (t.occupied == True and player.f != t.piece.player.f and i>=0 and j - self.l2 >= 0):
                        board[i][j - self.l2].possible = True
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j + self.l2]
                    if (t.occupied == True and player.f != t.piece.player.f and i>=0 and j + self.l2 >= 0):
                        board[i][j + self.l2].possible = True
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

    def step(self,i,j,board,color):
        if (self.d1 == 0):
            j -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i + self.l2][j]
                    if (t.occupied == False and j >= 0 and i + self.l2 >= 0):
                        t.possible = True
                        board[i + self.l2][j] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i - self.l2][j]
                    if (t.occupied == False and j >= 0 and i - self.l2 >= 0):
                        t.possible = True
                        board[i - self.l2][j] = t
                except:
                    pass
        elif (self.d1 == 1):
            i += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j + self.l2]
                    if (t.occupied == False and i >= 0 and j + self.l2 >= 0):
                        t.possible = True
                        board[i][j + self.l2] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j - self.l2]
                    if (t.occupied == False and i >= 0 and j - self.l2 >= 0):
                        t.possible = True
                        board[i][j - self.l2] = t
                except:
                    pass
        elif (self.d1 == 2):
            j += self.l1
            if (self.d2 != -1):
                try:
                    t = board[i - self.l2][j]
                    if (t.occupied == False and j >= 0 and i - self.l2 >= 0):
                        t.possible = True
                        board[i - self.l2][j] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i + self.l2][j]
                    if (t.occupied == False and j >= 0 and i + self.l2 >= 0):
                        t.possible = True
                        board[i + self.l2][j] = t
                except:
                    pass
        else:
            i -= self.l1
            if (self.d2 != -1):
                try:
                    t = board[i][j - self.l2]
                    if (t.occupied == False and i >= 0 and j - self.l2 >= 0):
                        t.possible = True
                        board[i][j - self.l2] = t
                except:
                    pass
            if (self.d2 != 1):
                try:
                    t = board[i][j + self.l2]
                    if (t.occupied == False and i >= 0 and j + self.l2 >= 0):
                        t.possible = True
                        board[i][j + self.l2] = t
                except:
                    pass
        return board

class Piece:
    #eligibility - array of numbers to indicate which wariants of moves of other pieces are possible
    def __init__(self, moves, PNG, l, color, is_important, player, eligibility):
        self.player = player
        self.important = is_important
        self.color = color
        self.moves = moves
        self.elig = eligibility
        self.PNG = pr.load_image(PNG)
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(0, 0, l, l)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

    def draw(self, x, y):
        pr.draw_texture(self.texture, x, y, raylib.WHITE)

    def draw_pos(self,i,j,board):
        for q in self.moves:
            q.draw(i, j, board)

    def step(self, i,j,board):
        for q in self.moves:
            board = q.step(i, j, board, self.player)
        return board

class Quinn(Piece):
    def __init__(self, color,l, player):
        self.elig = []
        self.player = player
        self.important = False
        self.color = color
        self.moves = [Line(1,1,0),Line(-1,-1,0),Line(-1,1,0),Line(1,-1,0),Line(-1,0,0),Line(0,-1,0),Line(0,1,0),Line(1,0,0)]
        if (color == 0):
            self.PNG = pr.load_image('images/WQ.png')
        else:
            self.PNG = pr.load_image('images/BQ.png')
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(15, 15, l - 30, l - 30)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

class Knight(Piece):
    def __init__(self, color,l, player):
        self.elig = []
        self.player = player
        self.important = False
        self.color = color
        self.moves = [Jump(0,0,2,1),Jump(1,0,2,1),Jump(2,0,2,1),Jump(3,0,2,1)]
        if (color == 0):
            self.PNG = pr.load_image('images/WKn.png')
        else:
            self.PNG = pr.load_image('images/BKn.png')
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(15, 15, l - 30, l - 30)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

class Bishop(Piece):
    def __init__(self, color,l, player):
        self.elig = []
        self.player = player
        self.important = False
        self.color = color
        self.moves = [Line(1,1,0),Line(-1,-1,0),Line(-1,1,0),Line(1,-1,0)]
        if (color == 0):
            self.PNG = pr.load_image('images/WB.png')
        else:
            self.PNG = pr.load_image('images/BB.png')
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(15, 15, l - 30, l - 30)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

class Rook(Piece):
    def __init__(self,color,l, player):
        self.elig = [0]
        self.player = player
        self.important = False
        self.color = color
        self.moves = [Line(-1,0,0),Line(0,-1,0),Line(0,1,0),Line(1,0,0)]
        if (color == 0):
            self.PNG = pr.load_image('images/WR.png')
        else:
            self.PNG = pr.load_image('images/BR.png')
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(15, 15, l - 30, l - 30)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

class King(Piece):
    def __init__(self, color,l, player):
        self.elig = [2]
        self.player = player
        self.important = True
        self.color = color
        self.moves = [Line(1,1,1),Line(-1,-1,1),Line(-1,1,1),Line(1,-1,1),Line(-1,0,1),Line(0,-1,1),Line(0,1,1),Line(1,0,1),Castle()]
        if (color == 0):
            self.PNG = pr.load_image('images/WK.png')
        else:
            self.PNG = pr.load_image('images/BK.png')
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(15, 15, l - 30, l - 30)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

#need is_turned(turned - black; not turned - white)
class Pawn(Piece):
    def __init__(self, color, l, player, is_turned = False):
        #3-promotion elig
        self.elig = [3]
        self.player = player
        self.important = False
        self.color = color
        self.is_turned = is_turned
        if (is_turned):
            self.moves = [Capture_Line(-1, 1, 1), Capture_Line(1, 1, 1), Free_Line(0, 1, 1)]
        else:
            self.moves = [Capture_Line(1,-1,1),Capture_Line(-1,-1,1),Free_Line(0,-1,1)]
        if (color == 0):
            self.PNG = pr.load_image('images/WP.png')
        else:
            self.PNG = pr.load_image('images/BP.png')
        src_rect = pr.Rectangle(0, 0, self.PNG.width, self.PNG.height)
        dst_rect = pr.Rectangle(15, 15, l - 30, l - 30)
        background = pr.gen_image_color(l, l, (255, 255, 255, 0))
        pr.image_draw(background, self.PNG, src_rect, dst_rect, pr.WHITE)
        self.texture = pr.load_texture_from_image(background)
        pr.unload_image(background)

    def step(self, i, j, board):
        if (not self.is_turned and j == 6 or self.is_turned and j == 1):
            self.moves[2].l = 2
        for q in self.moves:
            board = q.step(i, j, board, self.player)
        if (not self.is_turned and j == 6 or self.is_turned and j == 1):
            self.moves[2].l = 1
        return board
