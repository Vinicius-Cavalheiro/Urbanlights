# code/Menu.py
import pygame
from code.Const import WIDTH, HEIGHT

class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 56)
        self.options = ["Play", "Quit"]
        self.selected = 0

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected].lower()

            self.screen.fill((10, 10, 30))
            title = self.font.render("Urban Lights", True, (255, 255, 255))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

            for i, option in enumerate(self.options):
                color = (255, 220, 60) if i == self.selected else (220, 220, 220)
                txt = self.font.render(option, True, color)
                self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250 + i*70))

            pygame.display.flip()
