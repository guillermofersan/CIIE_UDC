import pygame
from pytmx.util_pygame import load_pygame

from settings import *

class ResourceManager:
    recursos = {}

    @classmethod
    def load(self, name, type='image', fontsize=50):
        path = PATHS[name]
        if path in self.recursos:
            return self.recursos[name]
        else:
            match type:
                case 'image':
                    resource = pygame.image.load(path).convert_alpha()
                case 'map':
                    resource = load_pygame(path)
                case 'font':
                    resource = pygame.font.Font(path, fontsize)
            self.recursos[name] = resource
            return resource
