import imp
import pygame

from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,y_shift):
        self.rect.y += y_shift

class StaticTile(Tile):
    def __init__(self, size, x, y,surface):
        super().__init__(size, x, y)
        self.image = surface    
    
class AnimateTile(Tile):

    def __init__(self, size, x, y,path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self,shift):
        self.animate()
        self.rect.y +=shift

class Coin(AnimateTile):
    def __init__(self, size, x, y, path,value):
        super().__init__(size, x, y, path)
        center_x = x 
        center_y = y 
        self.rect = self.image.get_rect(topleft = (center_x,center_y))
        self.value = value

class heal(AnimateTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x 
        center_y = y 
        self.rect = self.image.get_rect(topleft = (center_x,center_y))
        

