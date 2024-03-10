import sys
import random

import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from monster import *
from settings import *
from sprite import Bullet
from sprite import Sprite
from utilities import *
from healthBar import HealthBar
from recursos import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Cálculo del factor de escala basado en el tamaño de la ventana y el tamaño del fondo
        self.bg_size = 50  # 50x50 tiles cada pantalla
        self.tile_size = 16  # El tamaño original de cada tile (16x16)
        self.zoom_scale = WINDOW_HEIGHT / (self.bg_size * self.tile_size)

        # Ajustes para la cámara y el zoom
        self.half_w, self.half_h = self.display_surface.get_size()[0] // 2, WINDOW_HEIGHT // 2
        self.internal_surf_size = pygame.math.Vector2(self.bg_size * self.tile_size, self.bg_size * self.tile_size)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_offset = pygame.math.Vector2(0,0)
        self.bg_surf = GestorRecursos.load('background')
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

    def custom_draw(self):
        self.internal_surf.fill("black")

        bg_offset = self.bg_rect.topleft + self.internal_offset
        self.internal_surf.blit(self.bg_surf, bg_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("demo")
        self.clock = pygame.time.Clock()
        arrow_surf = GestorRecursos.load('arrow')
        self.arrow = []
        for i in range(4):
            self.arrow.append(get_image(arrow_surf, i, 0, 32, 32, 1, (0,0,0)))
        self.bullet_surf = GestorRecursos.load('bullet')
        self.tmx_map = GestorRecursos.load('map', type='map')
        self.zona_actual = 1

        # groups
        self.all_sprites = AllSprites()
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.healthBar = pygame.sprite.Group()

        self.player_death = False
        self.scroll = False

        self.setup()

    def create_arrow(self, pos, dir, status):
        match status.split("_")[0]:
            case "left": arrow = self.arrow[1]
            case "right": arrow = self.arrow[3]
            case "up": arrow = self.arrow[0]
            case "down": arrow = self.arrow[2]
        Bullet(pos, dir, arrow, [self.all_sprites, self.bullets])
    
    def create_bullet(self, pos, dir, status):
        Bullet(pos, dir, self.bullet_surf, [self.all_sprites, self.bullets])
    
    def death(self):
        self.player_death = True

    def bullet_collision(self):
        for wall in self.colliders:
            pygame.sprite.spritecollide(wall, self.bullets, True,  pygame.sprite.collide_mask)

        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet, self.enemy, False, pygame.sprite.collide_mask)

            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage(1)

        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.damage(1)

    def start_scroll(self):
        self.scroll = True

    def setup_enemy(self, w1, w2):
        for obj in self.tmx_map.get_layer_by_name("enemy"):
            if obj.name == "Enemy" and (WINDOW_WIDTH * w1) < obj.x < (WINDOW_WIDTH * w2):
                match random.randint(0, 2):
                    case 0 :
                        self.monster = MonsterRange(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=PATHS["esqueletoCrossbow"],
                            collision_sprites=self.colliders,
                            create_bullet=self.create_arrow,
                            health = 5,
                            player=self.player,
                            shot_speed=1000,
                            animations=CROSSBOW_ANIMATIONS
                        )
                    case 1 :
                        self.monster = MonsterCloseRange(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=PATHS["esqueletoSword"],
                            collision_sprites=self.colliders,
                            health = 10,
                            player=self.player,
                            shot_speed=500,
                            animations=SWORD_ANIMATIONS
                        )
                    case 2 :
                        self.monster = MonsterRange(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=PATHS["esqueletoBow"],
                            collision_sprites=self.colliders,
                            create_bullet=self.create_arrow,
                            health = 5,
                            player=self.player,
                            shot_speed=1000,
                            animations=BOW_ANIMATIONS
                        )
                w = self.monster.image.get_size()[0]
                h = self.monster.image.get_size()[1]
                healthBar = HealthBar(obj.x-int(w/2), obj.y+int(h/2), w, 5, 5, self.healthBar)
                self.monster.attach(healthBar)
                self.monster.healthBar = healthBar

    def setup_zona2(self):
        self.zona_actual = 2
        self.setup_enemy(1, 2)

    def setup_zona3(self):
        self.zona_actual = 3
        self.setup_enemy(2, 4)
        for obj in self.tmx_map.get_layer_by_name("boss"):
            if obj.name == "Boss":
                self.monster = MonsterCloseRange(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.enemy],
                    path=PATHS["esqueletoSword"],
                    collision_sprites=self.colliders,
                    create_bullet=self.create_bullet,
                    health = 20,
                    player=self.player,
                    shot_speed=500,
                    animations=SWORD_ANIMATIONS
                )
                w = self.monster.image.get_size()[0]
                h = self.monster.image.get_size()[1]
                healthBar = HealthBar(obj.x-int(w/2), obj.y+int(h/2), w, 5, 20, self.healthBar)
                self.monster.attach(healthBar)
                self.monster.healthBar = healthBar

    def setup(self):
        for x, y, surf in self.tmx_map.get_layer_by_name("intermedio").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        for x, y, surf in self.tmx_map.get_layer_by_name("objetos").tiles():
            Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])

        for x, y, surf in self.tmx_map.get_layer_by_name("runas").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        for obj in self.tmx_map.get_layer_by_name("player"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["player"],
                    collision_sprites=self.colliders,
                    create_bullet=self.create_arrow,
                    health = 10,
                    death = self.death,
                    start_scroll = self.start_scroll,
                    animations=CROSSBOW_ANIMATIONS
                )
                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                self.player.attach(healthBar)
                self.player.healthBar = healthBar
                
        self.setup_enemy(0, 1)

    def run(self):
        one = True
        while True:
            if self.player_death:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if one:
                    fill_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                    fill_color = (0, 0, 0, 120)
                    fill_surface.fill(fill_color)
                    self.display_surface.blit(fill_surface, (0,0))
                    font = GestorRecursos.load('font', type='font')
                    text_surf = font.render("DEFEAT", True, (255,255,255))
                    self.display_surface.blit(text_surf,(int(WINDOW_WIDTH/2)-100,int(WINDOW_HEIGHT/2)-20))
                    one = False
            else:
                # event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                if self.scroll:
                    self.all_sprites.internal_offset.x -= 100
                    if self.all_sprites.internal_offset.x % 800 == 0:
                        self.scroll = False
                        self.setup_zona2() if self.zona_actual == 1 else self.setup_zona3()

                dt = self.clock.tick() / 1000
        
                # update groups
                self.all_sprites.update(dt)
                self.bullet_collision()

                # draw groups
                self.display_surface.fill("black")
                self.all_sprites.custom_draw()

                for bar in self.healthBar:
                    bar.draw(self.display_surface, self.all_sprites.internal_offset.x)

            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.run()
