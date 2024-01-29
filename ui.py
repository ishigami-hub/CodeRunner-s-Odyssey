import pygame

class UI:
    def __init__(self,surface):

        #setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (87,26)
        self.bg_width = 159
        self.bg_height = 15
        self.bar_max_width  = 275
        self.bar_height = 15

        # coins   
        self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (10,61))
        self.font = pygame.font.Font('../graphics/ui/font/Minecrafter.ttf',30)

    def sho_health(self,current,full):
        self.display_surface.blit(self.health_bar,(5,-25))
        current_helth_ratio = current / full
        current_bar_width = self.bar_max_width * current_helth_ratio
        bg_rect = pygame.Rect((self.health_bar_topleft),(self.bg_width,self.bg_height))
        health_bar_rect = pygame.Rect((self.health_bar_topleft),(current_bar_width,self.bar_height))
        pygame.draw.rect(self.display_surface,'#FFFFFF',bg_rect)
        pygame.draw.rect(self.display_surface,'#FF0000',health_bar_rect)

    def sho_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)    