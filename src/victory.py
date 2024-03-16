import pygame, sys
from button import *
from resources import *



def victory(director):
    pygame.mixer.init()
    pygame.mixer.music.load("audio/victoria.mp3")
    pygame.mixer.music.play(-1,0.0) 
    
    BG = ResourceManager.load('victoria', type='image')
    while True:
        director.display_surface.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        BUTTON = Button(image=None, pos=(650, 760), text_input="salir▶", font=ResourceManager.load('menufont', type='font', fontsize=50), base_color="#ffffff", hovering_color="gray")
        BUTTON.changeColor(MENU_MOUSE_POS)
        BUTTON.update(director.display_surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()