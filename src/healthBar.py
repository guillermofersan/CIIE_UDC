from observer import Observer, Subject
from resources import *


class HealthBar(Observer, pygame.sprite.Sprite):
    """
    
    Clase encargada de las barras de vida de enemigos y personaje principal
    
    """

    def __init__(self, x, y, w, h, maxHp, groups) -> None:
        """
        
        Inicia la barra de vida con posicion x,y altura y anchura, y vida maxima

        """
        super().__init__(groups)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = maxHp
        self.maxHp = maxHp
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surf, "green", (self.x, self.y, self.w, self.h))
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))

    # Dibuja la barra
    def draw(self, surface, offset):
        ratio = self.hp / self.maxHp
        x = self.x + offset
        pygame.draw.rect(surface, "red", (x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (x, self.y, self.w * ratio, self.h))

    # Mueve la barra de vida 
    def move(self, x, y):
        self.x = x
        self.y = y

    # Update de la barra de vida
    def update(self, subject: Subject) -> None:
        self.hp = subject.health
