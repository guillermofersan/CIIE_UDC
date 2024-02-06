import sys

import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from settings import *
from sprite import Bullet
from sprite import Sprite


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Cálculo del factor de escala basado en el tamaño de la ventana y el tamaño del fondo
        self.bg_size = 16  # Cuadrado 16x16
        self.tile_size = 16  # El tamaño original de cada tile (16x16)
        self.zoom_scale = WINDOW_HEIGHT / (self.bg_size * self.tile_size)

        # Ajustes para la cámara y el zoom
        self.offset = pygame.math.Vector2()
        self.half_w, self.half_h = self.display_surface.get_size()[0] // 2, WINDOW_HEIGHT // 2
        self.internal_surf_size = (self.bg_size * self.tile_size, self.bg_size * self.tile_size)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(topleft=(0, 0))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2(self.internal_surf_size[0] // 2 - 8 * self.tile_size,
                                                   self.internal_surf_size[1] // 2 - 8 * self.tile_size)

        self.bg_surf = pygame.image.load('../graphics/other/bg.png').convert_alpha()
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
        self.bullet_surf = pygame.image.load("../graphics/weapon/bullet.png").convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.setup()

    def create_bullet(self, pos, dir):
        Bullet(pos, dir, self.bullet_surf, [self.all_sprites, self.bullets])

    def setup(self):
        tmx_map = load_pygame("../data/map..tmx")

        for x, y, surf in tmx_map.get_layer_by_name("walls").tiles():
            Sprite((x * 16, y * 16), surf, [self.all_sprites, self.colliders])

        for obj in tmx_map.get_layer_by_name("player"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS["player"],
                    collision_sprites=self.colliders,
                    create_bullet=self.create_bullet
                )

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            # update groups
            self.all_sprites.update(dt)

            # draw groups
            self.display_surface.fill("black")
            self.all_sprites.custom_draw()

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
