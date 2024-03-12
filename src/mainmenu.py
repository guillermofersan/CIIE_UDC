import pygame, sys
from button import *
from resources import *



def main_menu(director):
    pygame.mixer.init()
    pygame.mixer.music.load("audio/mainmenu.mp3")
    pygame.mixer.music.play(-1,0.0) 
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
                    carta(director)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
def carta(director):
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        director.display_surface.fill("black")
        image=ResourceManager.load('carta', type='image')
        director.display_surface.blit(image, (0, 0))
        
        BUTTON = Button(image=None, pos=(750, 750), text_input="▶", font=ResourceManager.load('menufont', type='font', fontsize=70), base_color="#ffffff", hovering_color="gray")
        BUTTON.changeColor(MENU_MOUSE_POS)
        BUTTON.update(director.display_surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON.checkForInput(MENU_MOUSE_POS):
                    director.run()

        pygame.display.update()