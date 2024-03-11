import pygame
from mainmenu import *
from director import *

if __name__ == "__main__":
    pygame.init()
    director = Director()
    main_menu(director)
    #director.run()
    pygame.quit()
