import pygame
from pygame.math import Vector2 as vector
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
        super().__init__(groups)

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
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

        # ataque
        self.is_attacking = False
        self.is_shooting = False
        self.create_bullet = create_bullet

    def get_status(self):
        # idle
        if self.dir.x == 0 and self.dir.y == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # ataque
        if self.is_attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def import_assets(self, path):

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.is_attacking:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.dir.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.dir.x = -1
                self.status = 'left'
            else:
                self.dir.x = 0

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.dir.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.dir.y = 1
                self.status = 'down'
            else:
                self.dir.y = 0

            if keys[pygame.K_SPACE]:
                self.is_attacking = True
                self.dir = vector()
                self.frame_index = 0  # empieza la animación desde el primer frame
                self.is_shooting = False
                match self.status.split("_")[0]:
                    case "left": self.bullet_dir = vector(-1, 0)
                    case "right": self.bullet_dir = vector(1, 0)
                    case "up": self.bullet_dir = vector(0, -1)
                    case "down": self.bullet_dir = vector(0, 1)

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

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and not self.is_shooting:
            bullet_offset = self.rect.center + self.bullet_dir*13
            self.create_bullet(bullet_offset, self.bullet_dir)
            self.is_shooting = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]

    def collision(self, dir):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if dir == "horizontal":
                    if self.dir.x > 0:  # derecha
                        self.hitbox.right = sprite.hitbox.left
                    if self.dir.x < 0:  # izquierda
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:  # vertical
                    if self.dir.y > 0:  # arriba
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.dir.y < 0:  # arriba
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
