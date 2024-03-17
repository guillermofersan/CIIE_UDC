import pygame


def get_image(sheet, frameW, frameH, width, height, scale, colour, w, h):
    # Coge una imagen y la transforma a la escala necesaria

    image = pygame.Surface((width + w, height + h)).convert_alpha()
    image.blit(sheet, (0, 0), ((frameW * width), (frameH * height), width + w, height + h))
    image = pygame.transform.scale(image, ((width * scale), (height * scale)))
    image.set_colorkey(colour)

    return image
