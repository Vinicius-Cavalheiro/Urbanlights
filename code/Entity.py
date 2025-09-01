import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, animations, health=100):
        super().__init__()
        self.animations = animations  # dicionário com listas de sprites
        self.action = "idle"  # estado inicial
        self.frame = 0
        self.image = self.animations[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.flip = False
        self.health = health
        self.alive = True
        self.speed = 5
        self.jump_force = -15
        self.vel_y = 0
        self.on_ground = False

    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.frame = 0

    def update_animation(self):
        animation = self.animations[self.action]
        self.frame += 0.2
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def is_alive(self):
        return self.alive
