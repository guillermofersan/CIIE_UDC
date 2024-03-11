import pygame, sys
from button import *
from resources import *

def main_menu(director):
    BG = ResourceManager.load('menuBG', type='image')
    while True:
        director.display_surface.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=ResourceManager.load('playbutton', type='image'), pos=(400, 520), 
                            text_input="JUGAR", font=ResourceManager.load('menufont', type='font', fontsize=70), base_color="#7500A5", hovering_color="Purple")
        QUIT_BUTTON = Button(image=ResourceManager.load('quitbutton', type='image'), pos=(400, 680), 
                            text_input="SALIR", font=ResourceManager.load('menufont', type='font', fontsize=45), base_color="#7500A5", hovering_color="Purple")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(director.display_surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    director.run()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()