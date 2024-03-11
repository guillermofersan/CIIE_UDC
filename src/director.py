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

class Director():
    def __init__(self):
        self.current_zone = Zone1(self)
        self.end_zone = False

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Los Secretos de FICrol")
        self.clock = pygame.time.Clock()

        arrow_surf = ResourceManager.load('arrow')
        self.arrow = []
        for i in range(4):
            self.arrow.append(get_image(arrow_surf, i, 0, 32, 32, 1, (0,0,0), 0, 0))
        self.bullet_surf = ResourceManager.load('fireball')
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
                    
                if self.scroll:
                    self.all_sprites.internal_offset.x -= 100
                    if self.all_sprites.internal_offset.x % 800 == 0:
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
        for x, y, surf in self.tmx_map.get_layer_by_name("intermedio").tiles():
            Sprite((x * 16, y * 16), surf, self.all_sprites)

        self.block = []
        for x, y, surf in self.tmx_map.get_layer_by_name("bloqueo").tiles():
            self.block.append(Sprite((x * 16, y * 16), surf, self.all_sprites))

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
                    animations=CROSSBOW_ANIMATIONS,
                    weapon_sprites=self.weapons,
                    enemies=self.enemy,
                    create_magic=self.create_fireball
                )
                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                self.player.attach(healthBar)
                self.player.healthBar = healthBar

    def create_arrow(self, pos, dir, status):
        match status.split("_")[0]:
            case "left": arrow = self.arrow[1]
            case "right": arrow = self.arrow[3]
            case "up": arrow = self.arrow[0]
            case "down": arrow = self.arrow[2]
        Bullet(pos, dir, arrow, [self.all_sprites, self.bullets])
    
    def create_fireball(self, pos, dir, status):
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

    def load_boss(self):
        for obj in self.tmx_map.get_layer_by_name("boss"):
            if obj.name == "Boss":
                self.monster = MonsterBoss(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.enemy],
                    path=PATHS["bossN"],
                    collision_sprites=self.colliders,
                    health = 3,
                    player=self.player,
                    shot_speed=500,
                    animations=AXE_ANIMATIONS
                )
                w = self.monster.image.get_size()[0]
                h = self.monster.image.get_size()[1]
                healthBar = HealthBar(obj.x-int(w/2), obj.y+int(h/2), w, 5, 3, self.healthBar)
                self.monster.attach(healthBar)
                self.monster.healthBar = healthBar

    def setup_weapons(self, w1, w2):
        for obj in self.tmx_map.get_layer_by_name("weapon"):
            if (WINDOW_WIDTH * w1) < obj.x < (WINDOW_WIDTH * w2):
                match obj.name:
                    case "sword": Weapon((obj.x, obj.y), pygame.image.load(PATHS["sword"]).convert_alpha(), [self.weapons, self.all_sprites], "sword")
                    case "latigo": Weapon((obj.x, obj.y), pygame.image.load(PATHS["latigo"]).convert_alpha(), [self.weapons, self.all_sprites], "latigo")
                    case "mace": Weapon((obj.x, obj.y), pygame.image.load(PATHS["mace"]).convert_alpha(), [self.weapons, self.all_sprites], "mace")
                    case "bow": Weapon((obj.x, obj.y), pygame.image.load(PATHS["bow"]).convert_alpha(), [self.weapons, self.all_sprites], "bow")
                    case "crossbow": Weapon((obj.x, obj.y), pygame.image.load(PATHS["crossbow"]).convert_alpha(), [self.weapons, self.all_sprites], "crossbow")
                    case "staff": Weapon((obj.x, obj.y), pygame.image.load(PATHS["staff"]).convert_alpha(), [self.weapons, self.all_sprites], "staff")
                    case "hacha": Weapon((obj.x, obj.y), pygame.image.load(PATHS["hacha"]).convert_alpha(), [self.weapons, self.all_sprites], "hacha")
                    case "spear": Weapon((obj.x, obj.y), pygame.image.load(PATHS["spear"]).convert_alpha(), [self.weapons, self.all_sprites], "spear")

    def setup_enemy(self, w1, w2):
        for obj in self.tmx_map.get_layer_by_name("enemy"):
            if (WINDOW_WIDTH * w1) < obj.x < (WINDOW_WIDTH * w2):
                match obj.name:
                    case "Humano1": path = PATHS["humano1"]
                    case "Humano2": path = PATHS["humano2"]
                    case "Momia": path = PATHS["momia"]
                    case "Zombie1": path = PATHS["zombie1"]
                    case "Zombie2": path = PATHS["zombie2"]
                    case "Esqueleto": path = PATHS["humano1"]
                match random.randint(0, 3):
                    case 0 :
                        self.monster = MonsterCrossBow(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=path+"crossbow.png",
                            collision_sprites=self.colliders,
                            create_bullet=self.create_arrow,
                            health = 5,
                            player=self.player,
                            shot_speed=1000,
                            animations=CROSSBOW_ANIMATIONS
                        )
                        health = 5
                    case 1 :
                        self.monster = MonsterSword(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=path+"sword.png",
                            collision_sprites=self.colliders,
                            health = 10,
                            player=self.player,
                            shot_speed=500,
                            animations=SWORD_ANIMATIONS
                        )
                        health = 10
                    case 2 :
                        self.monster = MonsterBow(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=path+"bow.png",
                            collision_sprites=self.colliders,
                            create_bullet=self.create_arrow,
                            health = 5,
                            player=self.player,
                            shot_speed=1000,
                            animations=BOW_ANIMATIONS
                        )
                        health = 5
                    case 3 :
                        self.monster = MonsterStaff(
                            pos=(obj.x, obj.y),
                            groups=[self.all_sprites, self.enemy],
                            path=path+"magicStaff.png",
                            collision_sprites=self.colliders,
                            create_bullet=self.create_fireball,
                            health = 5,
                            player=self.player,
                            shot_speed=1000,
                            animations=MAGIC_ANIMATIONS
                        )
                        health = 5
                w = self.monster.image.get_size()[0]
                h = self.monster.image.get_size()[1]
                healthBar = HealthBar(obj.x-int(w/2), obj.y+int(h/2), w, 5, health, self.healthBar)
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