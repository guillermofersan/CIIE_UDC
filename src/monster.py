import pygame
from pygame.math import Vector2 as vector
from entity import Entity
from os import walk
from healthBar import HealthBar
from settings import *
from settings import PATHS
from sprite import *

class Enemy:
    def get_player_distance_direction(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()
            
        return (distance, direction)

    def face_player(self):
        _, direction = self.get_player_distance_direction()

        if -0.5 < direction.y < 0.5:
            if direction.x < 0: # player to the left
                self.status = 'left_idle'
            elif direction.x > 0: # player to the right
                self.status = 'right_idle'
        else:
            if direction.y < 0: # player to the top
                self.status = 'up_idle'
            elif direction.y > 0: # player to the bottom
                self.status = 'down_idle'

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance:
            self.dir = direction
            self.status = self.status.split('_')[0]
        else:
            self.dir = vector()


class Melee:
    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'


class Distance:
    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.is_attacking and (pygame.time.get_ticks() - self.shoot_time > self.shot_speed):
            self.is_attacking = True
            self.frame_index = 0
            self.is_shooting = False

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'


class Monster(Entity, Enemy):
    def __init__(self, pos, groups, path, collision_sprites, health, player, shot_speed, animations):
        super().__init__(pos, groups, path, collision_sprites, health, animations)

        self.player = player
        self.shot_speed = shot_speed
        self.shoot_time = 0

        self.healthBar = None

        self.is_shooting = False
    
    def check_death(self):
        super().check_death()
        if self.health <= 0:
            self.healthBar.kill()

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
            if current_time - self.hit_time > 40:
                self.is_vulnerable = True
    
    def giveHealthBar(self, healthBar: HealthBar):
        self.healthBar = healthBar

    def update(self, dt):
        if self.player.status != "death":
            self.face_player()
            self.walk_to_player()
            self.attack()

            self.move(dt)
            self.animate(dt)
            self.blink()
            self.healthBar.move(self.rect.left, self.rect.bottom)

            self.vulnerability_timer()
            self.check_death()


class MonsterCrossBow(Monster, Distance):
    def __init__(self, pos, groups, name, collision_sprites, player, bullet_groups):
        print(name)
        path = PATHS[name] + "crossbow.png"
        health = 5
        shot_speed = 1000
        animations = CROSSBOW_ANIMATIONS
        super().__init__(pos, groups, path, collision_sprites, health, player, shot_speed, animations)

        self.attack_radius = 100
        self.speed = 10

        self.create_bullet = self.create_arrow
        self.bullet_groups = bullet_groups

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and not self.is_shooting and int(self.frame_index) == 5:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction*40
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
            self.create_bullet(bullet_offset, direction, self.status, self.bullet_groups)
            self.shoot_time = pygame.time.get_ticks()
            self.is_shooting = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


class MonsterBow(Monster, Distance):
    def __init__(self, pos, groups, name, collision_sprites, player, bullet_groups):
        print(name)
        path = PATHS[name] + "bow.png"
        health = 5
        shot_speed = 1000
        animations = BOW_ANIMATIONS
        super().__init__(pos, groups, path, collision_sprites, health, player, shot_speed, animations)

        self.attack_radius = 100
        self.speed = 10

        self.create_bullet = self.create_arrow
        self.bullet_groups = bullet_groups

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if  self.is_attacking and not self.is_shooting and int(self.frame_index) == 9:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction*35
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
            self.create_bullet(bullet_offset, direction, self.status, self.bullet_groups)
            self.shoot_time = pygame.time.get_ticks()
            self.is_shooting = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


class MonsterStaff(Monster, Distance):
    def __init__(self, pos, groups, name, collision_sprites, player, bullet_groups):
        print(name)
        path = PATHS[name] + "magicStaff.png"
        health = 5
        shot_speed = 1000
        animations = MAGIC_ANIMATIONS
        super().__init__(pos, groups, path, collision_sprites, health, player, shot_speed, animations)

        self.attack_radius = 100
        self.speed = 10

        self.create_bullet = self.create_fireball
        self.bullet_groups = bullet_groups

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if  self.is_attacking and not self.is_shooting and int(self.frame_index) == 6:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction*35
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
            self.create_bullet(bullet_offset, direction, self.status, self.bullet_groups)
            self.shoot_time = pygame.time.get_ticks()
            self.is_shooting = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


class MonsterSword(Monster, Melee):
    def __init__(self, pos, groups, name, collision_sprites, player):
        print(name)
        path = PATHS[name] + "sword.png"
        health = 10
        shot_speed = 500
        animations = SWORD_ANIMATIONS
        super().__init__(pos, groups, path, collision_sprites, health, player, shot_speed, animations)

        self.attack_radius = 50
        self.speed = 10

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if  self.is_attacking and int(self.frame_index) == 4:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage(2)

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


class MonsterBoss(Monster, Melee):
    def __init__(self, pos, groups, path, collision_sprites, health, player,shot_speed, animations):
        
        super().__init__(pos, groups, path, collision_sprites, health, player,shot_speed, animations)

        self.attack_radius = 100
        self.speed = 20
        self.transformation = False
        self.maxHealth = health

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if  self.is_attacking and int(self.frame_index) == 4:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage(2)

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
    
    def check_death(self):
        if not self.transformation and self.health < (self.maxHealth/2):
            self.transformation = True
            print("ouch")
            self.changeSprite(PATHS["bossH"], AXE_ANIMATIONS)
        super().check_death()
