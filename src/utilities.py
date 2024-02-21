import pygame


def get_image(sheet, frameW, frameH, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frameW * width),(frameH * height), width, height))
    image = pygame.transform.scale(image, ((width * scale), (height * scale)))
    image.set_colorkey(colour)

    return image