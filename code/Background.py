import pygame
import os
from code.Const import WIDTH, HEIGHT

class Background:
    def __init__(self):
        path = os.path.join("assets", "fundo.png")
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
