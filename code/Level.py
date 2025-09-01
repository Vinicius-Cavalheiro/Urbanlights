# code/Level.py
import pygame
from code.Player import Player
from code.Enemy import Enemy
from code.Const import WIDTH, HEIGHT, FPS


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("assets/chao.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class Level:
    def __init__(self, level_number, screen):
        self.level_number = level_number
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # player spawn
        self.player = Player(100, HEIGHT - 150)

        self.load_level(level_number)

    def load_level(self, level_number):
        self.platforms.empty()
        self.enemies.empty()
        # flat ground:
        self.platforms.add(Platform(0, HEIGHT - 50, WIDTH, 50))
        # add some platforms
        if level_number == 1:
            self.platforms.add(Platform(200, HEIGHT - 150, 200, 20))
            self.platforms.add(Platform(500, HEIGHT - 250, 200, 20))
            self.enemies.add(Enemy(550, HEIGHT - 290))
        elif level_number == 2:
            self.platforms.add(Platform(150, HEIGHT - 150, 150, 20))
            self.platforms.add(Platform(400, HEIGHT - 250, 200, 20))
            self.platforms.add(Platform(650, HEIGHT - 350, 100, 20))
            self.enemies.add(Enemy(180, HEIGHT - 190))
            self.enemies.add(Enemy(420, HEIGHT - 290))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            keys = pygame.key.get_pressed()

            self.player.handle_input(keys, self.bullets)

            # updates
            self.player.update(self.platforms)

            for enemy in list(self.enemies):
                enemy.update(player=self.player)

            self.bullets.update()

            # bullets -> enemies
            hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
            for bullet, hit_enemies in hits.items():
                for en in hit_enemies:
                    en.take_damage(bullet.damage)

            # player melee hit
            if self.player.attacking:
                # check approximate moment to deal damage: use frame int >= 0 (we only apply once per attack)
                # we'll base on frame index reaching middle frame
                attack_frame_index = int(self.player.frame)
                if not self.player.attack_hit_done and attack_frame_index >= 0:
                    a_rect = self.player.get_attack_rect()
                    for en in self.enemies:
                        if a_rect.colliderect(en.rect):
                            en.take_damage(self.player.attack_damage)
                            self.player.attack_hit_done = True

            # enemy melee hit
            for en in self.enemies:
                if en.attacking and not en.attack_hit_done:
                    # simple timing: when attack_timer ~ 15 do hit
                    if en.attack_timer == 15:
                        a_rect = en.get_attack_rect()
                        if a_rect.colliderect(self.player.rect):
                            self.player.hp -= en.attack_damage
                        en.attack_hit_done = True

            # remove dead enemies handled inside Enemy.take_damage via kill()

            # player death
            if self.player.hp <= 0:
                return "menu"

            # level clear?
            if len(self.enemies) == 0:
                # for now, go back to menu when cleared
                return "menu"

            # draw
            self.draw()

        return "menu"

    def draw(self):
        # simple background
        try:
            bg = pygame.image.load("assets/fundo.png").convert()
            bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
            self.screen.blit(bg, (0, 0))
        except:
            self.screen.fill((135, 206, 235))

        self.platforms.draw(self.screen)
        self.enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        # HP bars
        # player hp
        pygame.draw.rect(self.screen, (0, 0, 0), (18, 18, 204, 24))
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 20, int(self.player.hp * 2), 20))
        # enemies hp above each enemy
        for en in self.enemies:
            bar_w = max(0, int((en.hp / 80) * en.rect.width))
            pygame.draw.rect(self.screen, (0, 0, 0), (en.rect.x, en.rect.y - 10, en.rect.width, 6))
            pygame.draw.rect(self.screen, (0, 255, 0), (en.rect.x, en.rect.y - 10, bar_w, 6))

        pygame.display.flip()
