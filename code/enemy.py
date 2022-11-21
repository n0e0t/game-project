import pygame
from tiles import AnimateTile
from random import randint

class Enemy(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,'../graphics/enemy/slime/blueslime/run')
        self.rect.y += size*1.1 - self.image.get_size()[1]
        self.speed = randint(1,2)
    
    def move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.animate()
        self.move()
        self.reverse_image()
        self.rect.y += shift

class Enemy2(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,'../graphics/enemy/slime/redslime/run')
        self.rect.y += size*1.1 - self.image.get_size()[1]
        self.speed = randint(1,3)
    
    def move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.animate()
        self.move()
        self.reverse_image()
        self.rect.y += shift

class Enemy3(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,'../graphics/enemy/slime/greenslime/run')
        self.rect.y += size*1.1 - self.image.get_size()[1]
        self.speed = randint(1,3)
    
    def move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.animate()
        self.move()
        self.reverse_image()
        self.rect.y += shift

class Enemy4(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,'../graphics/enemy/slime/whiteslime/run')
        self.rect.y += size*1.1 - self.image.get_size()[1]
        self.speed = randint(1,4)
    
    def move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
    
    def reverse(self):
        self.speed *= -1
    
    def update(self, shift):
        self.animate()
        self.move()
        self.reverse_image()
        self.rect.y += shift