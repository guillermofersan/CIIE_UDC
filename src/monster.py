from pygame.math import Vector2 as vector

from entity import Entity
from healthBar import HealthBar
from settings import *
from settings import PATHS
from sprite import *


class Melee:
    """
    
    Define el ataque a mele de los monstruos

    """

    def attack(self):
        # Comprueba si puede atacar (distancia o ya estar atacando), y si ataca, cambia su estatus
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'


class Distance:
    """
    
    Define el ataque de rango  de los monstruos

    """

    def attack(self):
        # Comprueba si puede atacar (distancia, velocidad de ataque, o ya estar atacando) , y si ataca, cambia su estatus
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.is_attacking and (
                pygame.time.get_ticks() - self.shoot_time > self.shot_speed):
            self.is_attacking = True
            self.frame_index = 0
            self.is_shooting = False

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'


class Monster(Entity):
    """
    
    Metodos de los monstruos del juego
    
    """

    def __init__(self, pos, groups, path, collision_sprites, health, player, shot_speed, animations):
        super().__init__(pos, groups, path, collision_sprites, health, animations)

        self.player = player
        self.shot_speed = shot_speed
        self.shoot_time = 0

        self.healthBar = None

        self.is_shooting = False

    def get_player_distance_direction(self):

        """
        
        Coge la distancia y direccion del monstruo al jugador

        """

        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()

        return (distance, direction)

    def face_player(self):

        """
        
        Cambia el status del enemigo en relacion a la direccion del jugador para caminar hasta el.
        
        """

        _, direction = self.get_player_distance_direction()

        if -0.5 < direction.y < 0.5:
            if direction.x < 0:  # Izquierda
                self.status = 'left_idle'
            elif direction.x > 0:  # Derecha
                self.status = 'right_idle'
        else:
            if direction.y < 0:  # Arriba
                self.status = 'up_idle'
            elif direction.y > 0:  # Abajo
                self.status = 'down_idle'

    def walk_to_player(self):

        """
        
        Coge la direccion del jugador y camina hacia el
        
        """

        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance:
            self.dir = direction
            self.status = self.status.split('_')[0]
        else:
            self.dir = vector()

    def check_death(self):
        # Comprueba la muerte, y mata la barra de vida en caso verdadero
        super().check_death()
        if self.health <= 0:
            self.healthBar.kill()

    def collision(self, dir):
        """
        
        Comprueba su colision con las hitbox de otros objetos. Es la misma que la del player
        
        """
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
        # Tiempo en el que es invulnerable
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 40:
                self.is_vulnerable = True

    def giveHealthBar(self, healthBar: HealthBar):
        # Le da una healthbar al monstruo
        self.healthBar = healthBar

    def update(self, dt):
        # Si el jugador no esta muerto, hacer que el monstruo ejecute las funciones correspondientes: atacar, ir hacia el, actualizar su barra de vida, comprobar si muere...
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
    """
    
    Clase especifica para los monstruos con ballesta. Se seleccionan sus animaciones, su rango de ataque, velocidad y balas
    
    """

    def __init__(self, pos, groups, name, collision_sprites, player, bullet_groups):
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

        """
        
        Realiza la animacion del disparo con ballesta. Similar a la animacion hecha con las armas de rango en el player
        
        """

        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and not self.is_shooting and int(self.frame_index) == 5:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction * 40
            match self.status.split("_")[0]:
                case "left":
                    bullet_offset[1] = bullet_offset[1] + 10
                case "right":
                    bullet_offset[1] = bullet_offset[1] + 10
                case "up":
                    bullet_offset[0] = bullet_offset[0] + 5
                case "down":
                    bullet_offset[0] = bullet_offset[0] - 5
                    bullet_offset[1] = bullet_offset[1] + 5
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
    """
    
    Clase especifica para los monstruos con arco. Se seleccionan sus animaciones, su rango de ataque, velocidad y balas
    
    """

    def __init__(self, pos, groups, name, collision_sprites, player, bullet_groups):
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
        """
        
        Realiza la animacion del disparo con arco. Similar a la animacion hecha con las armas de rango en el player
        
        """
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and not self.is_shooting and int(self.frame_index) == 9:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction * 35
            match self.status.split("_")[0]:
                case "left":
                    bullet_offset[1] = bullet_offset[1] + 10
                case "right":
                    bullet_offset[1] = bullet_offset[1] + 10
                case "up":
                    bullet_offset[0] = bullet_offset[0] + 5
                case "down":
                    bullet_offset[0] = bullet_offset[0] - 5
                    bullet_offset[1] = bullet_offset[1] + 5
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
    """
    
    Clase especifica para los monstruos con baston. Se seleccionan sus animaciones, su rango de ataque, velocidad y balas
    
    """

    def __init__(self, pos, groups, name, collision_sprites, player, bullet_groups):
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
        """
        
        Realiza la animacion del disparo con baston. Similar a la animacion hecha con las armas de rango en el player
        
        """
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and not self.is_shooting and int(self.frame_index) == 6:
            direction = self.get_player_distance_direction()[1]
            bullet_offset = self.rect.center + direction * 35
            match self.status.split("_")[0]:
                case "left":
                    bullet_offset[1] = bullet_offset[1] + 10
                    bullet_offset[0] = bullet_offset[0] - 10
                case "right":
                    bullet_offset[1] = bullet_offset[1] + 10
                    bullet_offset[0] = bullet_offset[0] + 10
                case "up":
                    bullet_offset[0] = bullet_offset[0] + 5
                case "down":
                    bullet_offset[0] = bullet_offset[0] - 5
                    bullet_offset[1] = bullet_offset[1] + 5
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
    """
    
    Clase especifica para los monstruos con espada. Se seleccionan sus animaciones, su rango de ataque, velocidad y balas
    
    """

    def __init__(self, pos, groups, name, collision_sprites, player):
        path = PATHS[name] + "sword.png"
        health = 10
        shot_speed = 500
        animations = SWORD_ANIMATIONS
        super().__init__(pos, groups, path, collision_sprites, health, player, shot_speed, animations)

        self.attack_radius = 50
        self.speed = 10

    def animate(self, dt):
        """
        
        Realiza la animacion del ataque con la espada. Similar a la animacion hecha con las armas meles en el player
        
        """
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and int(self.frame_index) == 4:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage(2)

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


class MonsterBoss(Monster, Melee):
    """
    
    Clase especifica para el boss final. Se seleccionan sus animaciones, su rango de ataque, velocidad y balas
    Tambien se especifica su transformacion
    
    """

    def __init__(self, pos, groups, path, collision_sprites, health, player, shot_speed, animations):

        super().__init__(pos, groups, path, collision_sprites, health, player, shot_speed, animations)

        self.attack_radius = 100
        self.speed = 20
        self.transformation = False
        self.maxHealth = health

    def animate(self, dt):
        """
        
        Realiza la animacion del ataque del boss. Similar a la animacion hecha con las armas meles en el player
        
        """
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.is_attacking and int(self.frame_index) == 4:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage(2)

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def check_death(self):
        # Comprueba si no se ha transformado, y si no lo ha hecho, se transforma.
        if not self.transformation and self.health < (self.maxHealth / 2):
            self.transformation = True
            self.changeSprite(PATHS["bossH"], AXE_ANIMATIONS)

        # Comprueba su muerte
        super().check_death()
