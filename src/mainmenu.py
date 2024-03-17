import sys

from button import *
from resources import *


def main_menu(director):
    """
    
    Clase con el menu principal del videojuego. Presenta dos botones, botond e jugar y salir.
    
    """
    pygame.mixer.init()
    pygame.mixer.music.load("audio/mainmenu.mp3")
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.1)

    # Carga el fondo
    BG = ResourceManager.load('menuBG', type='image')

    while True:
        director.display_surface.blit(BG, (0, 0))

        # Coge la posicion del raton
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Botones de jugar y salir
        PLAY_BUTTON = Button(image=ResourceManager.load('playbutton', type='image'), pos=(400, 520),
                             text_input="JUGAR", font=ResourceManager.load('menufont', type='font', fontsize=70),
                             base_color="#7500A5", hovering_color="Purple")
        QUIT_BUTTON = Button(image=ResourceManager.load('quitbutton', type='image'), pos=(400, 680),
                             text_input="SALIR", font=ResourceManager.load('menufont', type='font', fontsize=45),
                             base_color="#7500A5", hovering_color="Purple")

        # Hover
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(director.display_surface)

        for event in pygame.event.get():

            # Sale directo
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Al clicar
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Lleva a la carta si se clica jugar
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    carta(director)

                # Sale si se clica salir
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def carta(director):
    """
    
    Clase que simplemente displayea una carta como modo de iniciar la historia, yc rea un boton que te lleva al inicio del primer nivel.

    """

    while True:

        # Coge la posicion
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        director.display_surface.fill("black")

        # Coge la imagen de la carta y la carga
        image = ResourceManager.load('carta', type='image')
        director.display_surface.blit(image, (0, 0))

        # Crea el boton para saltar de nivel
        BUTTON = Button(image=None, pos=(750, 750), text_input="▶",
                        font=ResourceManager.load('menufont', type='font', fontsize=70), base_color="#ffffff",
                        hovering_color="gray")
        BUTTON.changeColor(MENU_MOUSE_POS)
        BUTTON.update(director.display_surface)

        for event in pygame.event.get():

            # Sale
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Al clicar
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Si se clica en el boton, lanza el director (Y con ello, el juego)
                if BUTTON.checkForInput(MENU_MOUSE_POS):
                    director.run()

        pygame.display.update()
