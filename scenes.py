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
    def __init__(self):
        self.board = Board([50,50],1400,raylib.WHITE,raylib.BROWN)
        self.exit_b = Button([1550, 1100], 600, 200, raylib.BLACK, 'Menu', raylib.GRAY, raylib.WHITE, raylib.WHITE, raylib.WHITE, 100, raylib.BLACK)

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