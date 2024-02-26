import sys

import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from monster import Monster
from settings import *
from sprite import Bullet
from sprite import Sprite
from utilities import *
from healthBar import HealthBar


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Cálculo del factor de escala basado en el tamaño de la ventana y el tamaño del fondo
        self.bg_size = 50  # Cuadrado 16x16
        self.tile_size = 16  # El tamaño original de cada tile (16x16)
        self.zoom_scale = WINDOW_HEIGHT / (self.bg_size * self.tile_size)

        # Ajustes para la cámara y el zoom
        self.offset = pygame.math.Vector2()
        self.half_w, self.half_h = self.display_surface.get_size()[0] // 2, WINDOW_HEIGHT // 2
        self.internal_surf_size = (self.bg_size * self.tile_size, self.bg_size * self.tile_size)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(topleft=(0, 0))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2(self.internal_surf_size[0] // 2 - 25 * self.tile_size,
                                                   self.internal_surf_size[1] // 2 - 25 * self.tile_size)

        self.bg_surf = pygame.image.load('graphics/other/tumba.png').convert_alpha()
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

    def custom_draw(self):
        self.internal_surf.fill("black")

        bg_offset = self.bg_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.bg_surf, bg_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("demo")
        self.clock = pygame.time.Clock()
        arrow_surf = pygame.image.load(PATHS["arrow"]).convert_alpha()
        self.arrow = []
        for i in range(4):
            self.arrow.append(get_image(arrow_surf, i, 0, 32, 32, 1, (0,0,0)))
        self.bullet_surf = pygame.image.load("graphics/weapon/bullet.png").convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.healthBar = pygame.sprite.Group()

        self.player_death = False
        self.scroll = False

        self.setup()

    def create_arrow(self, pos, dir):
        match self.player.status.split("_")[0]:
            case "left": arrow = self.arrow[1]
            case "right": arrow = self.arrow[3]
            case "up": arrow = self.arrow[0]
            case "down": arrow = self.arrow[2]
        Bullet(pos, dir, arrow, [self.all_sprites, self.bullets])
    
    def create_bullet(self, pos, dir):
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

    def setup(self):
        tmx_map = load_pygame("data/tumba.tmx")

        for x, y, surf in tmx_map.get_layer_by_name("intermedio").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        for x, y, surf in tmx_map.get_layer_by_name("objetos").tiles():
            Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])

        for x, y, surf in tmx_map.get_layer_by_name("runas").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name("player"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["player"],
                    collision_sprites=self.colliders,
                    create_bullet=self.create_arrow,
                    health = 5,
                    death = self.death,
                    start_scroll = self.start_scroll
                )
                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 5, self.healthBar)
                self.player.attach(healthBar)
                

        for obj in tmx_map.get_layer_by_name("enemy"):
            if obj.name == "Enemy":
                self.monster = Monster(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.enemy],
                    path=PATHS["enemy"],
                    collision_sprites=self.colliders,
                    create_bullet=self.create_bullet,
                    health = 5,
                    player=self.player,
                    shot_speed=500
                )
                w = self.monster.image.get_size()[0]
                h = self.monster.image.get_size()[1]
                healthBar = HealthBar(obj.x-int(w/2), obj.y+int(h/2), w, 5, 5, self.healthBar)
                self.monster.attach(healthBar)
                self.monster.healthBar = healthBar

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
                    font = pygame.font.Font(PATHS["font"],50)
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
                    self.all_sprites.internal_offset.x -= 10
                    self.all_sprites.bg_surf = pygame.image.load('graphics/other/tumba.png').convert_alpha()
                    if self.all_sprites.internal_offset.x % 800 == 0:
                        self.scroll = False
                # keys = pygame.key.get_pressed()
                # if keys[pygame.K_x] and self.all_sprites.half_w < self.display_surface.get_size()[0] // 2:
                #     self.all_sprites.internal_offset.x += 10
                #     self.all_sprites.bg_surf = pygame.image.load('graphics/other/tumba.png').convert_alpha()
                # if keys[pygame.K_z]:
                #     self.all_sprites.internal_offset.x -= 10
                #     self.all_sprites.bg_surf = pygame.image.load('graphics/other/tumba.png').convert_alpha()

                dt = self.clock.tick() / 1000
        
                # update groups
                self.all_sprites.update(dt)
                self.bullet_collision()


                # draw groups
                self.display_surface.fill("black")
                self.all_sprites.custom_draw()

                for a in self.healthBar:
                    a.draw(self.display_surface)

            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.run()
