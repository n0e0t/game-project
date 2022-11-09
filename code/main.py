import pygame, sys
from setting import *
from level import Level
from game_data import level_0
from overworld import Overworld 

class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.start_time = 0

    def create_level(self,current_level):
        now = pygame.time.get_ticks()
        self.start_time = now
        print(self.start_time)
        self.level = Level(current_level,screen,self.create_overworld,self.start_time)
        self.status = 'level'

    
    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'

    def run(self):
        now = pygame.time.get_ticks()
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
        


#pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if game.status =='level':
        screen.fill('black')
    else:
        screen.fill('gray')
    game.run()
    

    pygame.display.update()
    clock.tick(60)
