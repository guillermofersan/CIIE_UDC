import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import sin
from observer import Observer, Subject

class Entity(pygame.sprite.Sprite, Subject):


    def __init__(self, pos, groups, path, collision_sprites, health):
        super().__init__(groups)

        self.observers = []

        self.animations = {}
        self.import_assets(path)
        self.frame_index = 0
        self.status = "down_idle"

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movimiento
        self.pos = vector(self.rect.center)
        self.dir = vector()
        self.speed = 100

        # colisiones
        self.hitbox = self.rect.inflate(-self.rect.width * 0.6, -self.rect.height / 1.7)
        self.collision_sprites = collision_sprites

        # ataque
        self.is_attacking = False

        self.health = health
        self.is_vulnerable = True
        self.hit_time = None

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for ob in self.observers:
            ob.update(self)

    def blink(self):
        if not self.is_vulnerable:
             if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf
                    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def damage(self, ammount):
        if self.is_vulnerable:
            self.health -= ammount
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            self.notify()
    
    def check_death(self):
         if self.health <= 0:
             self.kill()

    def get_status(self):
        # idle
        if self.dir.x == 0 and self.dir.y == 0 and self.status != "death":
            self.status = self.status.split("_")[0] + "_idle"

        # ataque
        if self.is_attacking and self.status != "death":
            self.status = self.status.split("_")[0] + "_attack"

    def move(self, dt):
        # normalizar
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()

        # horizontal
        self.pos.x += self.dir.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # vertical
        self.pos.y += self.dir.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")
