# code/Player.py
import pygame
from code.Const import HEIGHT, GRAVITY


# IMPORT Bullet dinamicamente na hora do tiro para evitar circular imports

def load_spritesheet(path, frames):
    sheet = pygame.image.load(path).convert_alpha()
    w, h = sheet.get_size()
    frame_w = w // frames
    frames_list = []
    for i in range(frames):
        rect = pygame.Rect(i * frame_w, 0, frame_w, h)
        frames_list.append(sheet.subsurface(rect))
    return frames_list


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega spritesheets (verifique nomes dos arquivos)
        try:
            self.walk = load_spritesheet("assets/player_walk_spritesheet.png", 8)
            self.jump = load_spritesheet("assets/Jump.png", 10)
            self.attack = load_spritesheet("assets/attack_player.png", 6)
        except pygame.error as e:
            raise SystemExit(f"Erro ao carregar sprites do player: {e}")

        self.image = self.walk[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # movement
        self.speed = 5
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        # animation
        self.action = "idle"  # idle/walk/jump/attack
        self.frame = 0.0
        self.anim_speed = {"idle": 0.08, "walk": 0.25, "jump": 0.18, "attack": 0.45}
        self.facing_right = True

        # combat
        self.hp = 100
        self.shoot_cooldown = 0
        self.shoot_delay = 18  # frames
        self.attacking = False
        self.attack_timer = 0
        self.attack_hit_done = False
        self.attack_damage = 25

    def handle_input(self, keys, bullets_group):
        # horizontal
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
            if not self.attacking and not (self.action == "jump"):
                self.action = "walk"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
            if not self.attacking and not (self.action == "jump"):
                self.action = "walk"
        else:
            if not self.attacking and not (self.action == "jump"):
                self.action = "idle"

        # jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -15
            self.on_ground = False
            self.action = "jump"
            self.frame = 0.0

        # melee attack (X)
        if keys[pygame.K_x] and not self.attacking:
            self.attacking = True
            self.attack_timer = 0
            self.attack_hit_done = False
            self.action = "attack"
            self.frame = 0.0

        # shoot (Z)
        if keys[pygame.K_z] and self.shoot_cooldown <= 0:
            # lazy import to avoid circular imports
            from code.Bullet import Bullet
            dir = 1 if self.facing_right else -1
            bx = self.rect.centerx + (30 if dir == 1 else -30)
            by = self.rect.centery
            bullets_group.add(Bullet(bx, by, dir))
            self.shoot_cooldown = self.shoot_delay

    def update(self, platforms):
        # cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # horizontal movement & collisions
        self.rect.x += self.vel_x
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.rect.right = plat.rect.left
                elif self.vel_x < 0:
                    self.rect.left = plat.rect.right

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 12:
            self.vel_y = 12
        self.rect.y += int(self.vel_y)

        # vertical collisions
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    if self.action == "jump":
                        self.action = "idle"
                elif self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0

        # attacking logic (melee)
        if self.attacking:
            self.attack_timer += 1
            # decide in which frame/time the attack connects:
            # here: make it connect around middle frame:
            frames = len(self.attack)
            # convert animation progress to frame index:
            self.frame += self.anim_speed["attack"]
            if self.frame >= frames:
                # end attack
                self.attacking = False
                self.attack_timer = 0
                self.attack_hit_done = False
                self.action = "idle"
                self.frame = 0.0
        else:
            # animate normally
            if self.action == "walk":
                self.frame += self.anim_speed["walk"]
            elif self.action == "jump":
                self.frame += self.anim_speed["jump"]
            else:
                self.frame += self.anim_speed["idle"]

        # clamp frame indexes
        self.apply_animation_frame()

    def apply_animation_frame(self):
        if self.action == "walk":
            frames = self.walk
        elif self.action == "jump":
            frames = self.jump
        elif self.action == "attack":
            frames = self.attack
        else:
            frames = [self.walk[0]]

        idx = int(self.frame) % len(frames)
        self.image = frames[idx]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def get_attack_rect(self):
        w, h = 40, 40
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.centery - h // 2, w, h)
        else:
            return pygame.Rect(self.rect.left - w, self.rect.centery - h // 2, w, h)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
