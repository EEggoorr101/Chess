import pyray as pr
from raylib import *

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

