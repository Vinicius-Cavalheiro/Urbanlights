# code/Enemy.py
import pygame
from code.Const import HEIGHT

def load_spritesheet(path, frames):
    sheet = pygame.image.load(path).convert_alpha()
    w, h = sheet.get_size()
    frame_w = w // frames
    frames_list = []
    for i in range(frames):
        rect = pygame.Rect(i*frame_w, 0, frame_w, h)
        frames_list.append(sheet.subsurface(rect))
    return frames_list

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance=140, speed=2):
        super().__init__()
        try:
            self.walk = load_spritesheet("assets/enemy_walk_spritesheet.png", 11)
            self.attack = load_spritesheet("assets/attack_enemy.png", 6)
        except pygame.error as e:
            raise SystemExit(f"Erro ao carregar sprites do inimigo: {e}")

        self.image = self.walk[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.direction = -1
        self.patrol_distance = patrol_distance
        self.speed = speed

        # animation state
        self.action = "walk"
        self.frame = 0.0
        self.anim_speed = {"walk": 0.18, "attack": 0.35}
        self.facing_right = False

        # combat
        self.hp = 80
        self.attacking = False
        self.attack_timer = 0
        self.attack_hit_done = False
        self.attack_damage = 12

    def update(self, player=None, platforms=None):
        # simple AI: patrol when far, attack when close
        if not self.attacking:
            if player and abs(player.rect.centerx - self.rect.centerx) < 110 and abs(player.rect.centery - self.rect.centery) < 40:
                self.attacking = True
                self.attack_timer = 0
                self.action = "attack"
                self.frame = 0.0
            else:
                # patrol
                self.action = "walk"
                self.rect.x += self.speed * self.direction
                if self.rect.x > self.start_x + self.patrol_distance:
                    self.direction = -1
                    self.facing_right = False
                if self.rect.x < self.start_x - self.patrol_distance:
                    self.direction = 1
                    self.facing_right = True

        else:
            # attack progression
            self.attack_timer += 1
            self.frame += self.anim_speed["attack"]
            if self.attack_timer > 40:  # end attack after some ticks
                self.attacking = False
                self.attack_timer = 0
                self.attack_hit_done = False
                self.action = "walk"
                self.frame = 0.0

        # animate
        if self.action == "walk":
            self.frame += self.anim_speed["walk"]
            frames = self.walk
        else:
            frames = self.attack

        idx = int(self.frame) % len(frames)
        self.image = frames[idx]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def get_attack_rect(self):
        w, h = 48, 40
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.centery - h//2, w, h)
        else:
            return pygame.Rect(self.rect.left - w, self.rect.centery - h//2, w, h)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            self.kill()
