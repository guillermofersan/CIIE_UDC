
import pygame
from pytmx.util_pygame import load_pygame
from observer import Observer, Subject

class HealthBar(Observer, pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, maxHp, groups) -> None:
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
        self.rect = self.image.get_rect(center=(x,y))
    
    def draw(self, surface):
        ratio = self.hp / self.maxHp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    def move(self, x, y):
        self.x += x
        self.y += y
    

    def update(self, subject: Subject) -> None:
        self.hp = subject.health

