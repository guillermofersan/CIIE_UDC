import pygame
from pytmx.util_pygame import load_pygame

from settings import *


class ResourceManager:
    """
    
    Clase que se dedica exclusivamente a cargar recursos
    
    """

    recursos = {}

    @classmethod
    def load(self, name, is_path=False, type='image', fontsize=50):
        # Carga los recursos

        path = name if is_path else PATHS[name]

        # Si ya ha sido cargado, te lo devuelve
        if path in self.recursos:
            return self.recursos[name]
        else:

            # Si no, lo carga dependiendo de el tipo de fichero que sea
            match type:
                case 'image':
                    resource = pygame.image.load(path).convert_alpha()
                case 'map':
                    resource = load_pygame(path)
                case 'font':
                    resource = pygame.font.Font(path, fontsize)
            self.recursos[name] = resource
            return resource
