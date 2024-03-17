import pygame


class Sprite(pygame.sprite.Sprite):
    """
    Carga sprites del mapa
    """
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)


class Bullet(pygame.sprite.Sprite):
    """
    Carga los proyectiles
    """
    def __init__(self, pos, dir, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.dir = dir
        self.speed = 200

    def update(self, dt):
        # Hace update de su posicion en base a la velocidad y dt
        self.pos += self.dir * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))


class Weapon(pygame.sprite.Sprite):
    """
    Sprites de las armas
    """
    def __init__(self, pos, surf, groups, name, price):
        super().__init__(groups)
        self.name = name
        self.image = surf
        # Precio al comprarla
        self.price = price
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)

        self.pos = pygame.math.Vector2(self.rect.center)

    def taken(self):
        # Al cogerla, desaparece
        self.kill()


class Heart(pygame.sprite.Sprite):
    """
    Sprite del corazon
    """
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)

        self.pos = pygame.math.Vector2(self.rect.center)

    def taken(self):
        # Al cogerlo, desaparece
        self.kill()
