from director import *

if __name__ == "__main__":

    """
    
    Clase principal del programa

    Desde esta se inicializa pygame, se crea un director, el cual sera el que se encargue de manejar el loop principal del juego, y se llama al menu principal. Tras acabar el juego, se cerraria pygame, y el programa finalizaria.

    """

    pygame.init()
    director = Director()
    main_menu(director)
    pygame.quit()
