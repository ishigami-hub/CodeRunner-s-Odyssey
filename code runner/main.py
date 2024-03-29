import pygame, sys
from settings import *
from level import Level

#pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)

#title
pygame.display.set_caption("CodeRunner's Odyssey")


while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('purple')
    level.run()         
    pygame.display.update()
    clock.tick(60)   