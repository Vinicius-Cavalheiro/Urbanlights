# code/Game.py
import pygame
from code.Menu import Menu
from code.Level import Level
from code.Const import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Urban Lights")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            menu = Menu(self.screen)
            action = menu.run()
            if action == "quit":
                self.running = False
                break
            if action == "play" or action == "start":
                level = Level(1, self.screen)
                result = level.run()
                if result == "quit":
                    self.running = False
                    break
                # if result == "menu" -> simply loop to menu again

        pygame.quit()
