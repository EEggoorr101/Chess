import pyray as pr
import raylib
from raylib import *
from elements import *
#button - coordinates, width, heigh, main color, text, color when hovered, color when clicked, boarder color, text color, font, text color when clicked

class Menu():
    def __init__(self):
        self.text = 'Chess ultimate'
        self.game_b = Button([350, 800], 1500, 200, raylib.BLACK, 'Play the game', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, 100, raylib.BLACK)
        self.exit_b = Button([350, 1100], 1500, 200, raylib.BLACK, 'Exit the game', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, 100, raylib.BLACK)

    def act(self):
        pr.begin_drawing()
        self.draw()
        pr.end_drawing()
        scene = self.step()
        return scene

    def draw(self):
        pr.clear_background(raylib.BLACK)
        pr.draw_text(self.text, (2200-pr.measure_text(self.text,250))//2, 200, 250, raylib.WHITE)
        self.game_b.draw()
        self.exit_b.draw()

    def step(self):
        if (self.exit_b.step()):
            pr.close_window()
        if (self.game_b.step()):
            return 'game'
        return 'menu'

class Game():

    def generate_standart_board(self):
        self.board.tiles[0][0].occupied = True
        self.board.tiles[0][0].piece = Rook(1, self.board.tiles[0][0].l)
        self.board.tiles[1][0].occupied = True
        self.board.tiles[1][0].piece = Knight(1, self.board.tiles[0][0].l)
        self.board.tiles[2][0].occupied = True
        self.board.tiles[2][0].piece = Bishop(1, self.board.tiles[0][0].l)
        self.board.tiles[3][0].occupied = True
        self.board.tiles[3][0].piece = Quinn(1, self.board.tiles[0][0].l)
        self.board.tiles[4][0].occupied = True
        self.board.tiles[4][0].piece = King(1, self.board.tiles[0][0].l)
        self.board.tiles[5][0].occupied = True
        self.board.tiles[5][0].piece = Bishop(1, self.board.tiles[0][0].l)
        self.board.tiles[6][0].occupied = True
        self.board.tiles[6][0].piece = Knight(1, self.board.tiles[0][0].l)
        self.board.tiles[7][0].occupied = True
        self.board.tiles[7][0].piece = Rook(1, self.board.tiles[0][0].l)
        for i in range(self.board.num_len):
            self.board.tiles[i][1].occupied = True
            self.board.tiles[i][1].piece = Pawn(1, self.board.tiles[0][0].l, True)
        self.board.tiles[0][7].occupied = True
        self.board.tiles[0][7].piece = Rook(0, self.board.tiles[0][0].l)
        self.board.tiles[1][7].occupied = True
        self.board.tiles[1][7].piece = Knight(0, self.board.tiles[0][0].l)
        self.board.tiles[2][7].occupied = True
        self.board.tiles[2][7].piece = Bishop(0, self.board.tiles[0][0].l)
        self.board.tiles[3][7].occupied = True
        self.board.tiles[3][7].piece = Quinn(0, self.board.tiles[0][0].l)
        self.board.tiles[4][7].occupied = True
        self.board.tiles[4][7].piece = King(0, self.board.tiles[0][0].l)
        self.board.tiles[5][7].occupied = True
        self.board.tiles[5][7].piece = Bishop(0, self.board.tiles[0][0].l)
        self.board.tiles[6][7].occupied = True
        self.board.tiles[6][7].piece = Knight(0, self.board.tiles[0][0].l)
        self.board.tiles[7][7].occupied = True
        self.board.tiles[7][7].piece = Rook(0, self.board.tiles[0][0].l)
        for i in range(self.board.num_len):
            self.board.tiles[i][6].occupied = True
            self.board.tiles[i][6].piece = Pawn(0, self.board.tiles[0][0].l)

    def __init__(self):
        self.board = Board([30,30],1440,raylib.WHITE,raylib.BROWN, 8)
        self.exit_b = Button([1550, 1100], 600, 200, raylib.BLACK, 'Menu', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, 100, raylib.BLACK)
        self.players = []
        self.generate_standart_board()



    def act(self):
        scene = self.step()
        pr.begin_drawing()
        self.draw()
        pr.end_drawing()
        return scene

    def draw(self):
        pr.clear_background(raylib.BLACK)
        self.board.draw()
        self.exit_b.draw()

    def step(self):
        self.board.step()
        if (self.exit_b.step()):
            return 'menu'
        return 'game'

class EndGame():
    def __init__(self):
        pass