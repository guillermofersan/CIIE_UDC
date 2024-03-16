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
from victory import *

class Director:
    def __init__(self):
        self.current_zone = Zone1(self)
        self.end_zone = False

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Los Secretos de FICrol")

        self.tmx_map = ResourceManager.load('bosque', type='map')

        # groups
        self.all_sprites = AllSprites('bosque')
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.healthBar = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.player_death = False
        self.scroll = False

        self.spriteList = []

    def run(self):

        self.clock = pygame.time.Clock()

        self.bosque_setup()

        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.current_zone = self.current_zone.next_zone()
        
        
        self.reset('tienda')
        
        self.shop_setup()
        
        self.current_zone = Zone3(self)
        

        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.current_zone = self.current_zone.next_zone()

        self.reset('pueblo')

        self.pueblo_setup()

        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.current_zone = self.current_zone.next_zone()

        self.reset('tienda')

        self.shop_setup()
        self.current_zone = Zone3(self)

        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.current_zone = self.current_zone.next_zone()

        self.reset('tumba')

        self.level_setup()

        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.current_zone = self.current_zone.next_zone()
            
        victory(self)


    def reset(self, map):

        for sprite in self.all_sprites:
            sprite.kill()
            self.all_sprites.remove(sprite)

        self.current_zone = Zone1(self)
        self.end_zone = False

        self.tmx_map = ResourceManager.load(map, type='map')

        # groups
        self.all_sprites = AllSprites(map)
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.healthBar = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        

        self.player_death = False
        self.scroll = False

        self.spriteList = []


    def loop(self):
        self.end_zone = False
        sound_death = False
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
                if not sound_death:
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("audio/death.mp3")
                    pygame.mixer.music.play(0,0.0)
                    sound_death = True
                self.display_surface.fill("black")
                self.all_sprites.shop_draw(self.spriteList, self.bullets, self.enemy, self.coins, self.hearts, self.weapons)
                fill_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                fill_color = (0, 0, 0, 120)
                fill_surface.fill(fill_color)
                self.display_surface.blit(fill_surface, (0,0))
                
                font = ResourceManager.load('font', type='font', fontsize=100)
                defeat_text = font.render("DERROTA", True, "White")
                defeat_rect = defeat_text.get_rect(center=(400, 400))
                self.display_surface.blit(defeat_text, defeat_rect)
                
                RETURN_BUTTON = Button(image=None, pos=(400, 500), 
                            text_input="VOLVER", font=ResourceManager.load('font', type='font', fontsize=20), base_color="#ffffff", hovering_color="gray")
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                RETURN_BUTTON.changeColor(MENU_MOUSE_POS)
                RETURN_BUTTON.update(self.display_surface)
                
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
                self.all_sprites.shop_draw(self.spriteList, self.bullets, self.enemy, self.coins, self.hearts, self.weapons)

                for bar in self.healthBar:
                    bar.draw(self.display_surface, self.all_sprites.internal_offset.x)
                
                font = ResourceManager.load('font', type='font', fontsize=15)
                defeat_text = font.render("x"+str(self.player.money), True, "White")
                defeat_rect = defeat_text.get_rect(center=(30, 8))
                self.display_surface.blit(defeat_text, defeat_rect)
                self.display_surface.blit(ResourceManager.load("coin"), (0, 0))

            pygame.display.update()

    def level_setup(self):
        temp = self.player.money
        temp2 = self.player.weapon
        temp3 = ANIMATIONS[temp2]
        
        self.block = []

        new_list = []
        for x, y, surf in self.get_map_layer("intermedio").tiles():
            sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
            new_list.append(sprite)
        self.spriteList.append(new_list)

        new_list = []
        for x, y, surf in self.get_map_layer("bloqueo").tiles():
            sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
            self.block.append(sprite)
            new_list.append(sprite)
        self.spriteList.append(new_list)

        new_list = []
        for x, y, surf in self.get_map_layer("objetos").tiles():
            sprite = Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])
            new_list.append(sprite)
        self.spriteList.append(new_list)

        new_list = []
        for x, y, surf in self.get_map_layer("runas").tiles():
            sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
            new_list.append(sprite)
        self.spriteList.append(new_list)

        new_list = []
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
                    animations=temp3,
                    weapon_sprites=self.weapons,
                    enemies=self.enemy,
                    bullet_groups=self.get_bullet_groups(),
                    hearts=self.hearts,
                    coins=self.coins,
                    money=temp,
                    weapon = temp2
                )

                new_list.append(self.player)


                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                self.player.attach(healthBar)
                self.player.healthBar = healthBar
                pygame.mixer.music.unload()
                pygame.mixer.music.load("audio/cementerio.mp3")
                pygame.mixer.music.play(-1,0.0) 

        self.spriteList.append(new_list)

    def shop_setup(self):
        temp = self.player.money
        temp2 = self.player.weapon
        temp3 = ANIMATIONS[temp2]
        self.block = []

        new_list = []
        for x, y, surf in self.get_map_layer("Fondo").tiles():
            sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
            new_list.append(sprite)
        self.spriteList.append(new_list)
        
        new_list = []
        for x, y, surf in self.get_map_layer("Base").tiles():
            sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
            new_list.append(sprite)
        self.spriteList.append(new_list)

        new_list = []
        for x, y, surf in self.get_map_layer("Colisionables").tiles():
            sprite = Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])
            new_list.append(sprite)
        self.spriteList.append(new_list)



        new_list = []
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
                    animations=temp3,
                    weapon_sprites=self.weapons,
                    enemies=self.enemy,
                    bullet_groups=self.get_bullet_groups(),
                    hearts=self.hearts,
                    coins=self.coins,
                    money=temp,
                    weapon = temp2
                )

                new_list.append(self.player)
                
                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                self.player.attach(healthBar)
                self.player.healthBar = healthBar

        self.spriteList.append(new_list)

    def bosque_setup(self):
            temp = 0
            temp2 = "crossbow"
            temp3 = ANIMATIONS[temp2]
            
            new_list = []
            for x, y, surf in self.get_map_layer("Hierba").tiles():
                sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
                new_list.append(sprite)
            self.spriteList.append(new_list)

            new_list = []
            for x, y, surf in self.get_map_layer("Coli_3").tiles():
                sprite = Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])
                new_list.append(sprite)
            self.spriteList.append(new_list)

            new_list = []
            for x, y, surf in self.get_map_layer("Coli_1").tiles():
                sprite = Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])
                new_list.append(sprite)
            self.spriteList.append(new_list)

            new_list = []
            for x, y, surf in self.get_map_layer("Puertas").tiles():
                sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
                new_list.append(sprite)
            self.spriteList.append(new_list)

            new_list = []
            for x, y, surf in self.get_map_layer("Acc_agua").tiles():
                sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
                new_list.append(sprite)
            self.spriteList.append(new_list)

            self.block = []

            new_list = []
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
                        animations=temp3,
                        weapon_sprites=self.weapons,
                        enemies=self.enemy,
                        bullet_groups=self.get_bullet_groups(),
                        hearts=self.hearts,
                        coins=self.coins,
                        money=temp,
                        weapon = temp2
                    )

                    new_list.append(self.player)
                    
                    healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                    self.player.attach(healthBar)
                    self.player.healthBar = healthBar
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("audio/bosque.mp3")
                    pygame.mixer.music.play(-1,0.0) 

            self.spriteList.append(new_list)
    
    def pueblo_setup(self):
            temp = self.player.money
            temp2 = self.player.weapon
            temp3 = ANIMATIONS[temp2]

            print(temp3)

            new_list = []
            for x, y, surf in self.get_map_layer("Segunda base").tiles():
                sprite = Sprite((x * 16, y * 16), surf, self.all_sprites)
                new_list.append(sprite)
            self.spriteList.append(new_list)

            new_list = []
            for x, y, surf in self.get_map_layer("Coli").tiles():
                sprite = Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])
                new_list.append(sprite)
            self.spriteList.append(new_list)


            self.block = []

            new_list = []
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
                        animations=temp3,
                        weapon_sprites=self.weapons,
                        enemies=self.enemy,
                        bullet_groups=self.get_bullet_groups(),
                        hearts=self.hearts,
                        coins=self.coins,
                        money=temp,
                        weapon = temp2
                    )

                    new_list.append(self.player)
                    
                    healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                    self.player.attach(healthBar)
                    self.player.healthBar = healthBar
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("audio/pueblo.mp3")
                    pygame.mixer.music.play(-1,0.0) 

            self.spriteList.append(new_list)


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
    def __init__(self, map):
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

        match map:
            case 'bosque': self.bg_surf = ResourceManager.load('background_bosque')
            case 'tienda': self.bg_surf = ResourceManager.load('background_bosque')
            case 'tumba': self.bg_surf = ResourceManager.load('background')
            case 'pueblo': self.bg_surf = ResourceManager.load('background_bosque')
            
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

    # def custom_draw(self, list):
    #     self.internal_surf.fill("black")

    #     bg_offset = self.bg_rect.topleft + self.internal_offset
    #     self.internal_surf.blit(self.bg_surf, bg_offset)

    #     # active elements
    #     for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
    #         offset_pos = sprite.rect.topleft + self.internal_offset
    #         self.internal_surf.blit(sprite.image, offset_pos)

    #     scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size * self.zoom_scale)
    #     scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

    #     self.display_surface.blit(scaled_surf, scaled_rect)

    def shop_draw(self, list, bullets, enemies, coins, hearts, weapons):
        self.internal_surf.fill("black")

        bg_offset = self.bg_rect.topleft + self.internal_offset
        self.internal_surf.blit(self.bg_surf, bg_offset)

        # active elements
        for layer in list:
            
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite in layer:
                    offset_pos = sprite.rect.topleft + self.internal_offset
                    self.internal_surf.blit(sprite.image, offset_pos)

        for sprite in bullets:
            offset_pos = sprite.rect.topleft + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        for sprite in enemies:
            offset_pos = sprite.rect.topleft + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)
        
        for sprite in coins:
            offset_pos = sprite.rect.topleft + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        for sprite in hearts:
            offset_pos = sprite.rect.topleft + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        for sprite in weapons:
            offset_pos = sprite.rect.topleft + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

