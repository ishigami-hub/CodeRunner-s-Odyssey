import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):

        #game attributes
        self.max_level = 0
        self.max_health = 58
        self.cur_health = 58
        self.coins = 0

        #audio
        self.level_bg_music = pygame.mixer.Sound('../audio/effects/theme.mp3')
        self.level_bg_music.set_volume(0.2)
        self.overworld_bg_music = pygame.mixer.Sound('../audio/effects/overworld.mp3')
        self.overworld_bg_music.set_volume(0.2)
        self.deth_sound = pygame.mixer.Sound('../audio/effects/Death.mp3')
      
        #overworld creation
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)

        #use interfence
        self.ui = UI(screen)

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)

    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)
        self.level_bg_music.stop()

    def change_coins(self,amount):
        self.coins += amount

    def change_health(self,amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.deth_sound.play()
            self.cur_health = 58
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0,self.max_level,screen,self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops = -1)
    
    def run(self):
        if self.status == 'overworld':
           self.overworld.run()
        else:
            self.level.run()
            self.ui.sho_health(self.cur_health,100)
            self.ui.sho_coins(self.coins)
            self.check_game_over()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
pygame.display.set_caption("CodeRunner's Odyssey")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('sky blue')
    game.run()

    pygame.display.update()
    clock.tick(60)           