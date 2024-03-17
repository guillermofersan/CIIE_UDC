import pygame
from pygame.math import Vector2 as vector

from entity import Entity
from settings import *


class Player(Entity):
    """

    Clase encargada de la creacion del player y el manejo de sus atributos relacionados

    """

    def __init__(self, pos, groups, path, collision_sprites, health, death, start_scroll, animations, weapon_sprites,
                 enemies, bullet_groups, hearts, coins, money, weapon):
        super().__init__(pos, groups, path, collision_sprites, health, animations)
        self.bullet_dir = None
        self.death = death
        self.is_shooting = False
        self.create_bullet = self.create_arrow
        self.create_magic = self.create_fireball
        self.start_scroll = start_scroll
        self.healthBar = None
        self.weapon = weapon
        self.weapon_sprites = weapon_sprites
        self.enemies = enemies
        self.bullet_groups = bullet_groups
        self.hearts = hearts
        self.coins = coins
        self.money = money
        self.base_dmg = 2

    def input(self):

        """

        Comprueba las teclas pulsadas, y modifica el status y direccion correspondientes, o hace trigger de alguna accion.

        """

        keys = pygame.key.get_pressed()

        if not self.is_attacking:

            # Cambia direcciones y derecha/izquierda
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.dir.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.dir.x = -1
                self.status = 'left'
            else:
                self.dir.x = 0

            # Cambia direcciones y arriba/abajo
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.dir.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.dir.y = 1
                self.status = 'down'
            else:
                self.dir.y = 0

            # Mecanica de disparos en base al arma
            if keys[pygame.K_SPACE]:
                match self.weapon:
                    case "bow" | "crossbow" | "staff":
                        self.is_attacking = True
                        self.dir = vector()
                        self.frame_index = 0  # empieza la animación desde el primer frame
                        self.is_shooting = False
                        match self.status.split("_")[0]:
                            case "left":
                                self.bullet_dir = vector(-1, 0)
                            case "right":
                                self.bullet_dir = vector(1, 0)
                            case "up":
                                self.bullet_dir = vector(0, -1)
                            case "down":
                                self.bullet_dir = vector(0, 1)

                    case "sword" | "hacha" | "spear":
                        self.is_attacking = True
                        self.frame_index = 0

            # Mecánica de compra
            if keys[pygame.K_e]:
                for sprite in self.weapon_sprites:
                    if sprite.hitbox.colliderect(self.hitbox) and self.money >= 3:
                        self.change_weapon(sprite.name)
                        self.money -= 3
                        sprite.kill()

    def change_weapon(self, name):
        # Cambia el arma y su sprite correspondiente
        self.weapon = name
        self.changeSprite(PATHS[(name + "P")], ANIMATIONS[name])

    def melee_attack(self, damage_multiplier):
        if self.is_attacking and int(self.frame_index) == 4 and self.status != "death":
            collisions = pygame.sprite.spritecollide(self, self.enemies, False)
            if collisions:
                collisions[0].damage(self.base_dmg * damage_multiplier)

    def ranged_attack(self, create_func):
        if self.is_attacking and not self.is_shooting and int(self.frame_index) == 6 and self.status != "death":
            bullet_offset = self.rect.center + self.bullet_dir * 35
            direction = self.status.split("_")[0]
            if direction in ["left", "right"]:
                bullet_offset[1] += 10
            if direction in ["up", "down"]:
                bullet_offset[0] += 5 if direction == "up" else -5
            if direction == "down":
                bullet_offset[1] += 5
            if direction == "left" and create_func == self.create_magic:
                bullet_offset[0] -= 10
            if direction == "right" and create_func == self.create_magic:
                bullet_offset[0] += 10
            create_func(bullet_offset, self.bullet_dir, self.status, self.bullet_groups)
            self.is_shooting = True

    def animate(self, dt):

        # Realiza la animacion

        # Aqui se coge la velocidad
        current_animation = self.animations[self.status]
        if self.status == "death":
            self.frame_index += 7 * dt
        else:
            # Cambiar la velocidad de la animación basada en el tipo de arma
            if self.weapon == "sword":
                self.frame_index += 14 * dt  # Velocidad de animación para la espada
            elif self.weapon == "hacha":
                self.frame_index += 7 * dt  # Velocidad de animación para el hacha
            elif self.weapon == "spear":
                self.frame_index += 30 * dt  # Velocidad de animación para la lanza
            elif self.weapon == "staff":
                self.frame_index += 14 * dt  # Velocidad de animación para el baston
            else:
                self.frame_index += 14 * dt

        match self.weapon:
            # Crea las animaciones

            # En las armas mele, se especifica su daño

            # En las armas rango, se crea la bala dependiendo de hacia donde esta mirando el personaje

            # Precondiciones de estar atacando, no disparando y no estar muerto
            case "sword":
                self.melee_attack(1)
            case "hacha":
                self.melee_attack(2)
            case "spear":
                self.melee_attack(0.5)
            case "bow" | "crossbow":
                self.ranged_attack(self.create_bullet)
            case "staff":
                self.ranged_attack(self.create_magic)

        # Si ya se acabo la animacion, vuelves a empezar
        # Si la animacion es la de muerte, te mueres
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.status == "death":
                self.death()
                self.frame_index = len(current_animation) - 1

            # Finaliza la animacion de ataque
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self, dir):

        """

        Define colisiones y scroll

        """

        # Define la posicion del player para la realizacion del scroll en los niveles
        if ((WINDOW_WIDTH - 80 < self.pos.x < WINDOW_WIDTH
             or WINDOW_WIDTH * 2 - 80 < self.pos.x < WINDOW_WIDTH * 2
             or WINDOW_WIDTH * 3 - 80 < self.pos.x < WINDOW_WIDTH * 3)
                and WINDOW_HEIGHT / 2 - 15 < self.pos.y < WINDOW_HEIGHT / 2 + 15):
            self.start_scroll()

        # Colision con el corazon, que hace kill al realizarse
        for heart in self.hearts.sprites():
            if heart.hitbox.colliderect(self.hitbox):
                if self.health < self.maxHealth:
                    self.health = min(self.health + 3, 10)
                self.notify()
                heart.kill()

        # Colision con la moneda, que hace kill al realizarse
        for coin in self.coins.sprites():
            if coin.hitbox.colliderect(self.hitbox):
                self.money += 1
                self.notify()
                coin.kill()

        # Colisiones generales
        for sprite in self.collision_sprites.sprites():
            # Comprueba las hitbox de los objetos entre si

            # Colisiones horizontales
            if sprite.hitbox.colliderect(self.hitbox):
                if dir == "horizontal":
                    if self.dir.x > 0:  # derecha
                        self.hitbox.right = sprite.hitbox.left
                    if self.dir.x < 0:  # izquierda
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:  # Colisiones verticales
                    if self.dir.y > 0:  # abajo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.dir.y < 0:  # arriba
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def vulnerability_timer(self):
        """
        Tiempo durante el cual eres invulnerable a daño
        """
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 200:
                self.is_vulnerable = True

    def check_death(self):
        # Comprueba tu vida y cambia tu estatus si le toca
        if self.health <= 0:
            self.status = 'death'

    def update(self, dt):

        """

        Runea las funciones del personaje que se deben ejecutar en bucle

        """

        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_death()
