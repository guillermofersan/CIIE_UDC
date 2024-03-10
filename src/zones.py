import pygame

from settings import *
from sprite import *
from player import *

class Zone:
    def __init__(self, director):
        self.director = director

class Zone1(Zone):
    def __init__(self, director):
        super().__init__(director)
        self.left_border = 0
        self.right_border = WINDOW_WIDTH

    def setup(self): 
        self.director.setup_enemy(0, 1)
        self.director.setup_weapons(0, 1)

    def next_zone(self):
        return Zone2(self.director)

class Zone2(Zone):
    def __init__(self, director):
        super().__init__(director)
        self.left_border = WINDOW_WIDTH
        self.right_border = WINDOW_WIDTH * 2

    def setup(self):
        self.director.setup_enemy(1, 2)

    def next_zone(self):
        return Zone3(self.director)

class Zone3(Zone):
    def __init__(self, director):
        super().__init__(director)
        self.left_border = WINDOW_WIDTH * 2
        self.right_border = WINDOW_WIDTH * 3

    def setup(self):
        self.director.setup_enemy(2, 4)
        self.director.load_boss()

    def next_zone(self):
        return None
