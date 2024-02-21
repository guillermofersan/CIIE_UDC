import pygame
from pygame.math import Vector2 as vector
from entity import Entity
from os import walk
from settings import *
from utilities import *

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet, health, death):
        super().__init__(pos, groups, path, collision_sprites, health)
        self.death = death
        self.is_shooting = False
        self.create_bullet = create_bullet

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


    def import_assets(self, path):

        surf = pygame.image.load(path).convert_alpha()

        for i in PLAYER_ANIMAIONS:
            status = PLAYER_ANIMAIONS[i].split('.')[0]
            frames = int(PLAYER_ANIMAIONS[i].split('.')[1])
            if status not in self.animations:
                self.animations[status] = []
            for j in range(frames):
                image = get_image(surf,j,round(float(i)),PLAYER_ANIMATIONSW, PLAYER_ANIMATIONSH, 1, (0,0,0))
                self.animations[status].append(image)
                



    def animate(self, dt):
        current_animation = self.animations[self.status]
        if self.status == "death":
            self.frame_index += 7 * dt
        else:
            self.frame_index += 14 * dt

        if self.is_attacking and not self.is_shooting and int(self.frame_index) == 6 and self.status != "death":
            bullet_offset = self.rect.center
            match self.status.split("_")[0]:
                    case "left":
                        bullet_offset += self.bullet_dir*35
                        bullet_offset[1] = bullet_offset[1]+round(bullet_offset[1]/10)
                    case "right":
                        bullet_offset += self.bullet_dir*35
                        bullet_offset[1] = bullet_offset[1]+round(bullet_offset[1]/10)
                    case "up":
                        bullet_offset += self.bullet_dir*30
                        bullet_offset[0] = bullet_offset[0]+round(bullet_offset[0]/17)
                    case "down":
                        bullet_offset += self.bullet_dir*45
                        bullet_offset[0] = bullet_offset[0]-round(bullet_offset[0]/17)
            self.create_bullet(bullet_offset, self.bullet_dir)
            self.is_shooting = True

        if self.frame_index >= len(current_animation):
            if self.status == "death":
                self.death()
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

    def vulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 200:
                self.is_vulnerable = True
    
    def check_death(self):
        if self.health <= 0:
            self.status = 'death'

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_death()
