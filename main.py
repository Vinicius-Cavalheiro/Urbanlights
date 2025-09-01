import pygame
print('Setup start')
pygame.init()


screen = pygame.display.set_mode(size = (600, 480))
print('SETUP END')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()