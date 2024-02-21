import pygame
from pygame.math import Vector2 as vector
from entity import Entity
from os import walk

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





class Monster(Entity,Enemy):
    def __init__(self, pos, groups, path, collision_sprites, health, player, create_bullet, shot_speed):
        super().__init__(pos, groups, path, collision_sprites, health)

        self.player = player
        self.attack_radius = 50
        self.speed = 10
        self.shot_speed = shot_speed
        self.shoot_time = 0


        self.create_bullet = create_bullet
        self.is_shooting = False

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.is_attacking and (pygame.time.get_ticks() - self.shoot_time > self.shot_speed):
            self.is_attacking = True
            self.frame_index = 0
            self.is_shooting = False

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'


    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if  self.is_attacking and not self.is_shooting:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction*13
            self.create_bullet(bullet_offset, direction)
            self.shoot_time = pygame.time.get_ticks()
            self.is_shooting = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]

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

    def update(self, dt):

        self.face_player()
        self.walk_to_player()
        self.attack()

        
        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_death()