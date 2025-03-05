from elements import *
from pieces import *
from screeninfo import get_monitors
#button - coordinates, width, heigh, main color, text, color when hovered, color when clicked, boarder color, text color, font, text color when clicked

class Menu():
    def __init__(self):
        monitor = get_monitors()[0]
        self.w = monitor.width
        self.h = monitor.height
        self.text = 'Chess ultimate'
        b_l = self.w // 7 * 5
        self.game_b = Button([(self.w-b_l)//2, self.h // 7 * 3], b_l, self.h // 7, raylib.BLACK, 'Play the game', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, self.h//14, raylib.BLACK)
        self.exit_b = Button([(self.w-b_l)//2, self.h // 7 * 5], b_l, self.h // 7, raylib.BLACK, 'Exit the game', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, self.h//14, raylib.BLACK)

    def act(self):
        pr.begin_drawing()
        self.draw()
        pr.end_drawing()
        scene = self.step()
        return scene

    def draw(self):
        pr.clear_background(raylib.BLACK)
        font = self.h // 7
        pr.draw_text(self.text, (self.w-pr.measure_text(self.text,font))//2, self.h // 7, font, raylib.WHITE)
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
        self.board.tiles[0][0].piece = Rook(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[1][0].occupied = True
        self.board.tiles[1][0].piece = Knight(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[2][0].occupied = True
        self.board.tiles[2][0].piece = Bishop(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[3][0].occupied = True
        self.board.tiles[3][0].piece = Quinn(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[4][0].occupied = True
        self.board.tiles[4][0].piece = King(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[5][0].occupied = True
        self.board.tiles[5][0].piece = Bishop(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[6][0].occupied = True
        self.board.tiles[6][0].piece = Knight(1, self.board.tiles[0][0].l, self.players[1])
        self.board.tiles[7][0].occupied = True
        self.board.tiles[7][0].piece = Rook(1, self.board.tiles[0][0].l, self.players[1])
        for i in range(self.board.num_len):
            self.board.tiles[i][1].occupied = True
            self.board.tiles[i][1].piece = Pawn(1, self.board.tiles[0][0].l, self.players[1], True)
        self.board.tiles[0][7].occupied = True
        self.board.tiles[0][7].piece = Rook(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[1][7].occupied = True
        self.board.tiles[1][7].piece = Knight(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[2][7].occupied = True
        self.board.tiles[2][7].piece = Bishop(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[3][7].occupied = True
        self.board.tiles[3][7].piece = Quinn(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[4][7].occupied = True
        self.board.tiles[4][7].piece = King(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[5][7].occupied = True
        self.board.tiles[5][7].piece = Bishop(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[6][7].occupied = True
        self.board.tiles[6][7].piece = Knight(0, self.board.tiles[0][0].l, self.players[0])
        self.board.tiles[7][7].occupied = True
        self.board.tiles[7][7].piece = Rook(0, self.board.tiles[0][0].l, self.players[0])
        for i in range(self.board.num_len):
            self.board.tiles[i][6].occupied = True
            self.board.tiles[i][6].piece = Pawn(0, self.board.tiles[0][0].l, self.players[0])

    def __init__(self):
        monitor = get_monitors()[0]
        self.w = monitor.width
        self.h = monitor.height
        self.board = Board([self.h//20,self.h//20],self.h//10*9,raylib.WHITE,raylib.BROWN, 8)
        self.exit_b = Button([self.h, 1100], 600, 200, raylib.BLACK, 'Menu', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, 100, raylib.BLACK)
        self.players = [Player(False, 0), Player(True, 1)]
        self.turn = 0
        self.generate_standart_board()



    def act(self):
        if (self.players[self.turn%2].turned):
            self.board.turn_board()
        scene = self.step()
        pr.begin_drawing()
        self.draw()
        pr.end_drawing()
        if (self.players[self.turn%2].turned):
            self.board.turn_board()
        if (self.board.moved):
            self.turn += 1
            self.board.moved = False
        return scene

    def draw(self):
        pr.clear_background(raylib.BLACK)
        self.board.draw()
        self.exit_b.draw()

    def step(self):
        self.board.step(self.players[self.turn%2])
        if (self.exit_b.step()):
            return 'menu'
        return 'game'

class EndGame():
    def __init__(self):
        pass