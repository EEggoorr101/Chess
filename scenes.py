from elements import *
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
    def __init__(self):
        monitor = get_monitors()[0]
        self.w = monitor.width
        self.h = monitor.height
        self.exit_b = Button([self.h, 1100], 600, 200, raylib.BLACK, 'Menu', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, 100, raylib.BLACK)
        self.players = [Player(False, 0, 'White'), Player(True, 1, 'Black')]
        self.turn = 0

    def new_game(self):
        self.board = ChessBoard([self.h//20,self.h//20],self.h//10*9, self.players, [self.h//20 + self.h, self.h//20], self.h//10*9, self.h//10*4)

    def act(self):
        if (self.board.is_over):
            scene = self.end_screen.act()
            if (scene == 'new game'):
                self.new_game()
                return 'game'
            else:
                return scene
        else:
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
        event = self.board.is_over
        if (self.exit_b.step()):
            return 'menu'
        if (event):
            self.end_screen = EndGame(self.board.winner)
            return 'game'
        return 'game'

class EndGame():
        def __init__(self, winner):
            monitor = get_monitors()[0]
            self.w = monitor.width
            self.h = monitor.height
            self.text = 'Winner is ' + winner
            b_l = self.w // 7 * 5
            self.game_b = Button([(self.w - b_l) // 2, self.h // 7 * 3], b_l, self.h // 7, raylib.BLACK,
                                 'Play again', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, self.h // 14,
                                 raylib.BLACK)
            self.menu_b = Button([(self.w - b_l) // 2, self.h // 7 * 5], b_l, self.h // 7, raylib.BLACK,
                                 'Menu', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, self.h // 14,
                                 raylib.BLACK)

        def act(self):
            pr.begin_drawing()
            self.draw()
            pr.end_drawing()
            scene = self.step()
            return scene

        def draw(self):
            pr.clear_background(raylib.BLACK)
            font = self.h // 7
            pr.draw_text(self.text, (self.w - pr.measure_text(self.text, font)) // 2, self.h // 7, font, raylib.WHITE)
            self.game_b.draw()
            self.menu_b.draw()

        def step(self):
            if (self.menu_b.step()):
                return 'menu'
            if (self.game_b.step()):
                return 'new game'
            return 'game'