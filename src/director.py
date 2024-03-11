import sys
import random
import pygame

from settings import *
from resources import *
from zones import *
from utilities import *
from healthBar import *
from monster import *
from button import *
from mainmenu import *

class Director:
    def __init__(self):
        self.current_zone = Zone1(self)
        self.end_zone = False

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Los Secretos de FICrol")
        self.clock = pygame.time.Clock()

        self.tmx_map = ResourceManager.load('map', type='map')
        self.zona_actual = 1

        # groups
        self.all_sprites = AllSprites()
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.healthBar = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()

        self.player_death = False
        self.scroll = False

    def run(self):
        self.level_setup()
        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.current_zone = self.current_zone.next_zone()

    def loop(self):
        self.end_zone = False
        pygame.event.clear()

        while not self.end_zone:
            if self.player_death:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                            director = Director()
                            main_menu(director)

                self.display_surface.fill("black")
                self.all_sprites.custom_draw()
                fill_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                fill_color = (0, 0, 0, 120)
                fill_surface.fill(fill_color)
                self.display_surface.blit(fill_surface, (0,0))
                font = ResourceManager.load('font', type='font')
                text_surf = font.render("DEFEAT", True, (255,255,255))
                RETURN_BUTTON = Button(image=None, pos=(400, 500), 
                            text_input="VOLVER", font=ResourceManager.load('font', type='font', fontsize=20), base_color="#ffffff", hovering_color="gray")
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                RETURN_BUTTON.changeColor(MENU_MOUSE_POS)
                RETURN_BUTTON.update(self.display_surface)
                self.display_surface.blit(text_surf,(int(WINDOW_WIDTH/2)-100,int(WINDOW_HEIGHT/2)-20))
            else:
                # event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                if self.current_zone.enemy_counter == 0:
                    for obj in self.block:
                        if obj.rect.right <= self.current_zone.right_border:
                            obj.kill()
                            self.all_sprites.remove(obj)
                    if self.scroll:
                        self.all_sprites.internal_offset.x -= 100
                        if self.all_sprites.internal_offset.x % 800 == 0:
                            self.player.pos.x += 180
                            self.player.healthBar.x += WINDOW_WIDTH
                            self.scroll = False
                            break

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

    def level_setup(self):
        for x, y, surf in self.get_map_layer("intermedio").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        self.block = []
        for x, y, surf in self.get_map_layer("bloqueo").tiles():
            self.block.append(Sprite((x * 16, y * 16), surf, self.all_sprites))

        for x, y, surf in self.get_map_layer("objetos").tiles():
            Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])

        for x, y, surf in self.get_map_layer("runas").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        for obj in self.get_map_layer("player"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["player"],
                    collision_sprites=self.colliders,
                    health = 10,
                    death = self.death,
                    start_scroll = self.start_scroll,
                    animations=CROSSBOW_ANIMATIONS,
                    weapon_sprites=self.weapons,
                    enemies=self.enemy,
                    bullet_groups=self.get_bullet_groups()
                )
                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                self.player.attach(healthBar)
                self.player.healthBar = healthBar
    
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
        if self.current_zone.enemy_counter == 0:
            self.scroll = True

    def get_map_layer(self, name):
        return self.tmx_map.get_layer_by_name(name)
    
    def get_enemy_groups(self):
        return [self.all_sprites, self.enemy]
    
    def get_colliders(self):
        return self.colliders
    
    def get_health_bar(self):
        return self.healthBar
    
    def get_player(self):
        return self.player
    
    def get_bullet_groups(self):
        return [self.all_sprites, self.bullets]

    def load_boss(self):
        for obj in self.tmx_map.get_layer_by_name("boss"):
            if obj.name == "Boss":
                self.monster = MonsterBoss(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.enemy],
                    path=PATHS["bossN"],
                    collision_sprites=self.colliders,
                    health = 20,
                    player=self.player,
                    shot_speed=500,
                    animations=AXE_ANIMATIONS
                )
                w = self.monster.image.get_size()[0]
                h = self.monster.image.get_size()[1]
                healthBar = HealthBar(obj.x-int(w/2), obj.y+int(h/2), w, 5, 20, self.healthBar)
                self.monster.attach(healthBar)
                self.monster.healthBar = healthBar


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
        self.bg_surf = ResourceManager.load('background')
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
