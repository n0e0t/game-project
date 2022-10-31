from tkinter import CENTER
from turtle import Turtle, speed
import pygame
from support import import_folder
from setting import *
from level import *
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        
        self.rect = self.image.get_rect(topleft = pos)
        
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 2
        self.gravity = 0.8
        self.jump_speed = -12
        self.last = -1500
        self.cooldown = 900
        self.jumpcount = 0
        self.lastjump = -300
        self.jumpcooldown = 300

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_celling = False
        self.on_left = False
        self.on_right = False
        self.on_wall =False
   
    def import_character_assets(self):
        character_path =  'C:/Users/pongsapadnet/Desktop/code/game/graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'crouch':[],'crouchwalk':[],'roll':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right :
            self.image = image
        else : 
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_celling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_celling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_celling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
        


    def get_input(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.x < screen_width  :
            self.direction.x = 1
            self.facing_right = True
            if keys[pygame.K_a]:
                self.direction.x =0
        elif keys[pygame.K_a]and self.rect.x > 0 :
            self.direction.x = -1
            self.facing_right = False
            if keys[pygame.K_d]:
                self.direction.x =0
                self.facing_right = False
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            self.direction.x = 0
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.jumpcount < 1 and now - self.lastjump >= self.jumpcooldown and now - self.last >=self.cooldown:
            self.lastjump = now
            self.jump()
            self.jumpcount += 1
        
        if self.on_ground == True:
            self.jumpcount = 0

    def get_status(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if self.direction.y < 0 and self.on_ground ==False and now - self.last >=self.cooldown :
            self.status = 'jump'
        elif self.direction.y > 1 and self.on_ground == False and now - self.last >=self.cooldown and not (self.on_left or self.on_right):
            self.status = 'fall'
        elif keys[pygame.K_s] and self.on_ground == True and now - self.last >=self.cooldown :
            self.status =  'crouch'
            if keys[pygame.K_d] or keys[pygame.K_a]:
                self.status = 'crouchwalk'
                self.speed = 1
        
        #elif keys[pygame.K_LSHIFT] and now - self.last >=self.cooldown and (keys[pygame.K_d] or keys[pygame.K_a])and self.on_ground :
         #   if self.facing_right == False:
          #      self.frame_index = 0
           #     self.status = 'roll'
            #    self.speed = 6
             #   self.animation_speed = 0.2
              #  self.last = now
            #elif self.facing_right == True:
             #   self.frame_index = 0
              #  self.status = 'roll'
               # self.speed = 6
                #self.animation_speed = 0.2
               # self.last = now
                                
        elif  now - self.last >=self.cooldown:
            if self.direction.x != 0 :
                self.status = 'run'
                self.speed = 3
                self.animation_speed = 0.15
            else:
                self.status = 'idle'
                self.speed = 3
                self.animation_speed = 0.15
        else:
                self.gravity=0.8
        
            
            

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
   
    def jump(self):
        self.direction.y = self.jump_speed
    
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()


            