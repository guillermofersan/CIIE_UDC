import pygame
from pygame.math import Vector2 as vector
from entity import Entity
from os import walk
from settings import *

class Player(Entity):

    def __init__(self, pos, groups, path, collision_sprites, health, death, start_scroll, animations, weapon_sprites, enemies, bullet_groups):
        super().__init__(pos, groups, path, collision_sprites, health, animations)
        self.death = death
        self.is_shooting = False
        self.create_bullet = self.create_arrow
        self.create_magic = self.create_fireball
        self.start_scroll = start_scroll
        self.healthBar = None
        self.weapon = "crossbow"
        self.weapon_sprites = weapon_sprites
        self.enemies = enemies
        self.bullet_groups = bullet_groups

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
                 match self.weapon:
                    case "bow":
                        self.is_attacking = True
                        self.dir = vector()
                        self.frame_index = 0  # empieza la animación desde el primer frame
                        self.is_shooting = False
                        match self.status.split("_")[0]:
                            case "left": self.bullet_dir = vector(-1, 0)
                            case "right": self.bullet_dir = vector(1, 0)
                            case "up": self.bullet_dir = vector(0, -1)
                            case "down": self.bullet_dir = vector(0, 1)
                        
                    case "crossbow":
                        self.is_attacking = True
                        self.dir = vector()
                        self.frame_index = 0  # empieza la animación desde el primer frame
                        self.is_shooting = False
                        match self.status.split("_")[0]:
                            case "left": self.bullet_dir = vector(-1, 0)
                            case "right": self.bullet_dir = vector(1, 0)
                            case "up": self.bullet_dir = vector(0, -1)
                            case "down": self.bullet_dir = vector(0, 1)
                    case "sword":
                        self.is_attacking = True
                        self.frame_index = 0 
                    case "mace":
                        self.is_attacking = True
                        self.frame_index = 0 
                    case "staff":
                        self.is_attacking = True
                        self.dir = vector()
                        self.frame_index = 0  # empieza la animación desde el primer frame
                        self.is_shooting = False
                        match self.status.split("_")[0]:
                            case "left": self.bullet_dir = vector(-1, 0)
                            case "right": self.bullet_dir = vector(1, 0)
                            case "up": self.bullet_dir = vector(0, -1)
                            case "down": self.bullet_dir = vector(0, 1)
                    case "hacha":
                        self.is_attacking = True
                        self.frame_index = 0 
                    case "latigo":
                        self.is_attacking = True
                        self.frame_index = 0 
                    case "spear":
                        self.is_attacking = True
                        self.frame_index = 0 
            if keys[pygame.K_e]:
                for sprite in self.weapon_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        self.changeWeapon(sprite.name)



    def changeWeapon(self, name):
        self.weapon = name
        self.changeSprite(PATHS[(name+"P")], ANIMATIONS[name])


    def animate(self, dt):
        current_animation = self.animations[self.status]
        if self.status == "death":
            self.frame_index += 7 * dt
        else:
            self.frame_index += 14 * dt

        match self.weapon:
            case "bow":
                if self.is_attacking and not self.is_shooting and int(self.frame_index) == 6 and self.status != "death":
                    bullet_offset = self.rect.center + self.bullet_dir*35
                    match self.status.split("_")[0]:
                            case "left":
                                bullet_offset[1] = bullet_offset[1]+10
                            case "right":
                                bullet_offset[1] = bullet_offset[1]+10
                            case "up":
                                bullet_offset[0] = bullet_offset[0]+5
                            case "down":
                                bullet_offset[0] = bullet_offset[0]-5
                                bullet_offset[1] = bullet_offset[1]+5
                    self.create_bullet(bullet_offset, self.bullet_dir, self.status, self.bullet_groups)
                    self.is_shooting = True
            case "crossbow":
                if self.is_attacking and not self.is_shooting and int(self.frame_index) == 6 and self.status != "death":
                    bullet_offset = self.rect.center + self.bullet_dir*35
                    match self.status.split("_")[0]:
                            case "left":
                                bullet_offset[1] = bullet_offset[1]+10
                            case "right":
                                bullet_offset[1] = bullet_offset[1]+10
                            case "up":
                                bullet_offset[0] = bullet_offset[0]+5
                            case "down":
                                bullet_offset[0] = bullet_offset[0]-5
                                bullet_offset[1] = bullet_offset[1]+5
                    self.create_bullet(bullet_offset, self.bullet_dir, self.status, self.bullet_groups)
                    self.is_shooting = True
            case "sword":
                if self.is_attacking and  int(self.frame_index) == 4 and self.status != "death":
                    collisions = pygame.sprite.spritecollide(self, self.enemies, False)
                    if collisions:
                        collisions[0].damage(2)
            case "spear":
                if self.is_attacking and  int(self.frame_index) == 6 and self.status != "death":
                    collisions = pygame.sprite.spritecollide(self, self.enemies, False)
                    if collisions:
                        collisions[0].damage(2)
            case "mace":
                if self.is_attacking and  int(self.frame_index) == 4 and self.status != "death":
                    collisions = pygame.sprite.spritecollide(self, self.enemies, False)
                    if collisions:
                        collisions[0].damage(2)
            case "staff":
                if self.is_attacking and not self.is_shooting and int(self.frame_index) == 6 and self.status != "death":
                    bullet_offset = self.rect.center + self.bullet_dir*35
                    match self.status.split("_")[0]:
                        case "left":
                            bullet_offset[1] = bullet_offset[1]+10
                            bullet_offset[0] = bullet_offset[0]-10
                        case "right":
                            bullet_offset[1] = bullet_offset[1]+10
                            bullet_offset[0] = bullet_offset[0]+10
                        case "up":
                            bullet_offset[0] = bullet_offset[0]+5
                        case "down":
                            bullet_offset[0] = bullet_offset[0]-5
                            bullet_offset[1] = bullet_offset[1]+5
                    self.create_magic(bullet_offset, self.bullet_dir, self.status, self.bullet_groups)
                    self.is_shooting = True
            case "hacha":
                if self.is_attacking and  int(self.frame_index) == 4 and self.status != "death":
                    collisions = pygame.sprite.spritecollide(self, self.enemies, False)
                    if collisions:
                        collisions[0].damage(2)
            case "latigo":
                if self.is_attacking and  int(self.frame_index) == 4 and self.status != "death":
                    collisions = pygame.sprite.spritecollide(self, self.enemies, False)
                    if collisions:
                        collisions[0].damage(2)
            
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.status == "death":
                self.death()
                self.frame_index = len(current_animation)-1
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self, dir):
        if ((WINDOW_WIDTH - 80 < self.pos.x < WINDOW_WIDTH
             or WINDOW_WIDTH * 2 - 80 < self.pos.x < WINDOW_WIDTH * 2)
            and WINDOW_HEIGHT / 2 - 15 < self.pos.y < WINDOW_HEIGHT / 2 + 15):
            self.start_scroll()
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
                    if self.dir.y > 0:  # abajo
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
