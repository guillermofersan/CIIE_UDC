import pygame
from director import *

if __name__ == "__main__":
    pygame.init()
    director = Director()
    director.run()
    pygame.quit()
