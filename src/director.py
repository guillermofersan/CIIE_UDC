from mainmenu import *
from player import *
from victory import *
from zones import *


class Director:

    """
    
    Clase encargada del loop principal del juego, y llamar a las clases correspondientes para el cargado de sprites/mecanicas correspondientes
    
    """
        
    def __init__(self):

        """
        
        Inicializa la clase con sus respectivos parametros
        
        """

        # Variables respectivas a la zona 
        self.current_zone = Zone1(self)
        self.end_zone = False

        # Crea la ventana, y un caption
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Los Secretos de FICrol")
        
        # Carga el mapa
        self.tmx_map = ResourceManager.load('bosque', type='map')

        # Se crean los grupos
        self.all_sprites = AllSprites('bosque')
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.healthBar = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        # Variables necesarias para funcionamiento
        self.player_death = False
        self.scroll = False
        self.shop = False
        self.tutorial = True

        self.spriteList = []

    def run(self):

        """
        
        Hace el set-up de los niveles y los lanza en orden.

        """

        # Inicializa el reloj
        self.clock = pygame.time.Clock()

        # Nivel del bosque
        self.level_setup('bosque')
        while self.current_zone != None:
            self.current_zone.setup()
            self.loop()
            self.tutorial = False
            self.current_zone = self.current_zone.next_zone()

        # Niveles de tienda, pueblo, tienda otra vez y tumba
        for level in ['tienda', 'pueblo', 'tienda', 'tumba']:
            self.reset(level)
            self.shop = not self.shop
            self.level_setup(level, self.player.money, self.player.weapon)
            if self.shop:
                self.current_zone = Zone3(self)
            while self.current_zone != None:
                self.current_zone.setup()
                self.loop()
                self.current_zone = self.current_zone.next_zone()
        
        # Mensaje de victoria
        victory(self)

    # Set up del nivel.
    def level_setup(self, level, money=0, weapon='crossbow'):
        self.block = []

        # Coge las layers del nivel correspondiente, crea sus sprites
        for layer, has_collisions in MAP_LAYERS[level]:
            temp_list = []
            groups = [self.all_sprites, self.colliders] if has_collisions else self.all_sprites
            block = layer == 'bloqueo'
            for x, y, surf in self.get_map_layer(layer).tiles():
                sprite = Sprite((x * 16, y * 16), surf, groups)
                temp_list.append(sprite)
                if block:
                    self.block.append(sprite)
            self.spriteList.append(temp_list)

        temp_list = []

        # Crea el player
        for obj in self.get_map_layer("player"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS[weapon+"P"],
                    collision_sprites=self.colliders,
                    health = 10,
                    death = self.death,
                    start_scroll = self.start_scroll,
                    animations = ANIMATIONS[weapon],
                    weapon_sprites=self.weapons,
                    enemies=self.enemy,
                    bullet_groups=self.get_bullet_groups(),
                    hearts=self.hearts,
                    coins=self.coins,
                    money=money,
                    weapon = weapon
                )
                temp_list.append(self.player)

                # Crea la barra de vida y la pega al player
                healthBar = HealthBar(0, WINDOW_HEIGHT-25, 250, 50, 10, self.healthBar)
                self.player.attach(healthBar)
                self.player.healthBar = healthBar
        
        # Lista para el dibujado
        self.spriteList.append(temp_list)

        # Si no es tienda, musica distinta
        if not self.shop:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(f"audio/{level}.mp3")
            pygame.mixer.music.play(-1,0.0) 


    def reset(self, map):

        """

        Resetea el nivel anterior, y se prepara para cargar el nivel siguiente pasado por parametro

        """

        # Mata todos los sprites
        for sprite in self.all_sprites:
            sprite.kill()
            self.all_sprites.remove(sprite)

        self.current_zone = Zone1(self)
        self.end_zone = False

        # Carga el mapa
        self.tmx_map = ResourceManager.load(map, type='map')

        # Grupos (Probablemente no necesario)
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

        """
        
        Loop principal de un nivel.
        
        """

        self.end_zone = False
        sound_death = False
        pygame.event.clear()

        # Mientras que siga habiendo zonas
        while not self.end_zone:

            # Si el jugador esta muerto
            if self.player_death:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Boton para la restauracion tras muerte
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                            director = Director()
                            main_menu(director)
                if not sound_death:
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("audio/death.mp3")
                    pygame.mixer.music.play(0,0.0)
                    sound_death = True

                # El siguiente codigo se utiliza para la creacion del menu post mortem
                            
                # Crea un difuminado negro de fondo, y escribe las palabras defeat en una font cargada
                    
                self.display_surface.fill("black")
                self.all_sprites.shop_draw(self.spriteList, self.bullets, self.enemy, self.coins, self.hearts, self.weapons)
                fill_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                fill_color = (0, 0, 0, 120)
                fill_surface.fill(fill_color)
                self.display_surface.blit(fill_surface, (0,0))
                
                # Carga la fuente y displayea el texto derrota
                font = ResourceManager.load('font', type='font', fontsize=100)
                defeat_text = font.render("DERROTA", True, "White")
                defeat_rect = defeat_text.get_rect(center=(400, 400))
                self.display_surface.blit(defeat_text, defeat_rect)

                # Displayea los botones necesarios, y chequea si se clica
                RETURN_BUTTON = Button(image=None, pos=(400, 500), 
                            text_input="VOLVER", font=ResourceManager.load('font', type='font', fontsize=20), base_color="#ffffff", hovering_color="gray")
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                RETURN_BUTTON.changeColor(MENU_MOUSE_POS)
                RETURN_BUTTON.update(self.display_surface)
                
            # Si el jugador no esta muerto
            else:
                
                for event in pygame.event.get():

                    # Evento de salida
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                # Si no hay enemigos
                level_arrow = None
                if self.current_zone.enemy_counter == 0:
                    level_arrow = ResourceManager.load('level_arrow')
                    for obj in self.block:
                        if obj.rect.right <= self.current_zone.right_border:
                            obj.kill()
                            self.all_sprites.remove(obj)
                    # Si se da el caso del scroll, mueve todo hacia el lado correspondiente
                    if self.scroll:
                        level_arrow = None
                        self.all_sprites.internal_offset.x -= 100
                        if self.all_sprites.internal_offset.x % 800 == 0:
                            self.player.pos.x += 180
                            self.player.healthBar.x += WINDOW_WIDTH
                            self.scroll = False
                            break

                # Delta times -> No depender de los FPS
                dt = self.clock.tick() / 1000
        
                # Actualizar los grupos
                self.all_sprites.update(dt)
                self.bullet_collision(self.player.weapon)

                # Dibujar los grupos
                self.display_surface.fill("black")
                self.all_sprites.shop_draw(self.spriteList, self.bullets, self.enemy, self.coins, self.hearts, self.weapons)
                if level_arrow != None:
                    self.display_surface.blit(level_arrow, (WINDOW_WIDTH - 135, WINDOW_HEIGHT / 2 - 30))

                # Dibuja todas las barras de vida dentro del grupo de healthBar
                for bar in self.healthBar:
                    bar.draw(self.display_surface, self.all_sprites.internal_offset.x)
                
                # Textos varios que aparecen en la pantalla 
                font = ResourceManager.load('font', type='font', fontsize=15)
                coin_text = font.render("x"+str(self.player.money), True, "White")
                coin_rect = coin_text.get_rect(center=(30, 8))
                self.display_surface.blit(coin_text, coin_rect)
                self.display_surface.blit(ResourceManager.load("coin"), (0, 0))

                # Texto para el precio de la tienda
                if self.shop:
                    font = ResourceManager.load('menufont', type='font', fontsize=30)
                    shop_text = font.render("Todo a 3", True, "White")
                    shop_rect = shop_text.get_rect(center=(390, 100))
                    self.display_surface.blit(ResourceManager.load("coin"), (510, 92))
                    self.display_surface.blit(shop_text, shop_rect)
                    image_tutorial = ResourceManager.load("tutorialtienda")
                    image_rect = image_tutorial.get_rect(center=(400,730))
                    self.display_surface.blit(image_tutorial, image_rect)

                # Texto para el ptutorial
                if self.tutorial:
                    image_tutorial = ResourceManager.load("tutorial")
                    image_rect = image_tutorial.get_rect(center=(400,700))
                    self.display_surface.blit(image_tutorial, image_rect)

            pygame.display.update()

    def death(self):
        self.player_death = True

    def bullet_collision(self, weapon):
        for wall in self.colliders:
            pygame.sprite.spritecollide(wall, self.bullets, True,  pygame.sprite.collide_mask)

        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet, self.enemy, False, pygame.sprite.collide_mask)

            if sprites:
                bullet.kill()
                for sprite in sprites:
                    match weapon:
                        case "staff":
                            sprite.damage(2)
                        case "crossbow":
                            sprite.damage(1)
                        case "bow":
                            sprite.damage(1)
                    

        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.damage(1)

    def start_scroll(self):
        """
        
        Setupea el scroll a true si se cumplen las condiciones
        
        """
        if self.current_zone.enemy_counter == 0:
            self.scroll = True

    def get_map_layer(self, name):
        """
        
        Coge la capa pasada por parametro de un mapa
        
        """
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


class AllSprites(pygame.sprite.Group):

    """
    
    Carga todos los sprites

    """

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

        # Carga el background correspondiente (Tienda lo carga, pero no lo utiliza)
        match map:
            case 'bosque': self.bg_surf = ResourceManager.load('background_bosque')
            case 'tienda': self.bg_surf = ResourceManager.load('background_bosque')
            case 'tumba': self.bg_surf = ResourceManager.load('background')
            case 'pueblo': self.bg_surf = ResourceManager.load('background_bosque')
            
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

    def shop_draw(self, list, bullets, enemies, coins, hearts, weapons):

        """
        
        Funcion de dibujado por capas
        
        """

        self.internal_surf.fill("black")

        bg_offset = self.bg_rect.topleft + self.internal_offset
        self.internal_surf.blit(self.bg_surf, bg_offset)

        # Dibuja primero las capas del mapa de Tiled
        for layer in list:
            
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite in layer:
                    offset_pos = sprite.rect.topleft + self.internal_offset
                    self.internal_surf.blit(sprite.image, offset_pos)
        
        # A continuacion dibuja grupos como enemigos, balas, monedas, corazones y armas
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

        # Hace el blit de la pantalla
        self.display_surface.blit(scaled_surf, scaled_rect)
