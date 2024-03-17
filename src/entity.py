from math import sin

from pygame.math import Vector2 as vector

from observer import Observer, Subject
from resources import *
from sprite import Bullet
from utilities import *


class Entity(pygame.sprite.Sprite, Subject):

    """
    
    Clase padre de todas las entidades -> monstruos y personaje principal
    
    """

    def __init__(self, pos, groups, path, collision_sprites, health, animations):

        """
        
        Inicializa la clase con sus parametros correspondientes
        
        """

        super().__init__(groups)

        # Observer necesario para hacer el update de las barras de vida
        self.observers = []

        # Carga las animaciones
        self.animations = {}
        self.import_assets(path, animations)
        self.frame_index = 0
        self.status = "down_idle"

        # Coge la imagen correspondiente (La activa en cada momento)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Movimiento
        self.pos = vector(self.rect.center)
        self.dir = vector()
        self.speed = 100

        # Colisiones
        self.hitbox = self.rect.inflate(-self.rect.width * 0.6, -self.rect.height / 4)
        self.collision_sprites = collision_sprites
        self.mask = pygame.mask.from_surface(self.image)

        # Ataque
        self.is_attacking = False

        # Otros parametros
        self.health = health
        self.maxHealth = health
        self.is_vulnerable = True
        self.hit_time = None

        # Carga la flecha en sus direcciones
        arrow_surf = ResourceManager.load('arrow')
        self.arrow = []
        for i in range(4):
            self.arrow.append(get_image(arrow_surf, i, 0, 32, 32, 1, (0, 0, 0), 0, 0))
        self.bullet_surf = ResourceManager.load('fireball')

    def changeSprite(self, path, animations):
        # Cambia el sprite correspondiente (Por ejemplo, cambiar de arma, o cambiar la fase del boss)

        self.animations = {}
        self.import_assets(path, animations)

    def import_assets(self, path, animations):

        """
        
        Funcion creada para importar los assets correspondientes. Se basa en los settings del archivo settings.py

        """

        surf = ResourceManager.load(path, is_path=True)

        # Para todas las animaciones
        for i in animations:
            extraW = 0
            extraH = 0
            if ":" in animations[i]:
                extraW = int(animations[i].split(':')[1])
                extraH = int(animations[i].split(':')[2])

            # Coge la animacion correspondiente usando splits para ir cogiendo las partes que necesitas (valores del settings: status, frame...)
            animations[i] = animations[i].split(':')[0]
            status = animations[i].split('.')[0]
            frames = int(animations[i].split('.')[1])
            space = 0

            # Para comprobar si existe un segundo numero (separacion anormal), y modifica el space al numero correspondiente
            if len(animations[i].split('.')) > 2:
                space = int(animations[i].split('.')[2])
            if status not in self.animations:
                self.animations[status] = []

            # Itera por toda la fila y cambia el salto de frame a frame dependiendo del tipo de animacion: Ejemplo, el boss se escala, el arco tiene distinta separacion que otras animaciones...
            for j in range(frames):
                j2 = j
                if "/bow" in path:
                    j3 = 0.5
                else:
                    j3 = 1
                if space != 0:
                    j2 = j3 + (space * j)
                    if j == 0:
                        j2 = j3
                    i2 = float(i)
                else:
                    i2 = round(float(i))
                scale = 1
                if "boss" in path:
                    scale = 2

                # Carga la imagen
                image = get_image(surf, j2, i2, PLAYER_ANIMATIONSW, PLAYER_ANIMATIONSH, scale, (0, 0, 0), extraW,
                                  extraH)
                self.animations[status].append(image)

    # Funciones del observer
    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for ob in self.observers:
            ob.update(self)

    # Parpadeo en el periodo de invulnerabilidad del personaje tras ser golpeado
    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    # Cambia el color en blink
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    # Aplica el cambio de vida tras recibir daño
    def damage(self, ammount):
        if self.is_vulnerable:
            self.health -= ammount
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            self.notify()

    # Comprueba la muerte
    def check_death(self):
        if self.health <= 0:
            self.kill()

    # Comprueba el estado actual del personaje
    def get_status(self):
        # idle
        if self.dir.x == 0 and self.dir.y == 0 and self.status != "death":
            self.status = self.status.split("_")[0] + "_idle"

        # ataque
        if self.is_attacking and self.status != "death":
            self.status = self.status.split("_")[0] + "_attack"

    # Funcion que se encarga del movimiento del personaje, comprobando colisiones
    def move(self, dt):
        # normalizar
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()

        # Colision horizontal
        self.pos.x += self.dir.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # Colision vertical
        self.pos.y += self.dir.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    # Crea la flecha
    def create_arrow(self, pos, dir, status, bullet_groups):
        match status.split("_")[0]:
            case "up":
                arrow = self.arrow[0]
            case "left":
                arrow = self.arrow[1]
            case "down":
                arrow = self.arrow[2]
            case "right":
                arrow = self.arrow[3]
        Bullet(pos, dir, arrow, bullet_groups)

    # Crea la bola de fuego
    def create_fireball(self, pos, dir, status, bullet_groups):
        Bullet(pos, dir, self.bullet_surf, bullet_groups)
