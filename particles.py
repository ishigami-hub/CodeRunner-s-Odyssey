import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        super().__init__()
        self.animation_speed =0.5
        self.frame_index = 0
        if type =='jump':
            self.frames = import_folder('../code runner/graphics/character/dust_particles/jump')
        if type == 'explosion':
            self.frames = import_folder('../code runner/graphics/enemy/explosion')
        if type =='land':
            self.frames = import_folder('../code runner/graphics/character/dust_particles/land')
        self.image = self.frames[self.frame_index] 
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): #to kill the dust particles after the frame ends
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)] #to make the dust particles go away  

    def update(self,x_shift):
        self.animate()
        self.rect.x += x_shift              