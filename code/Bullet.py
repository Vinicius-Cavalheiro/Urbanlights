# code/Bullet.py
import pygame
from code.Const import WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=12, damage=15):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/projetile.png").convert_alpha()
        except pygame.error as e:
            raise SystemExit(f"Erro ao carregar 'assets/projetile.png': {e}")
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed * direction
        self.damage = damage

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
