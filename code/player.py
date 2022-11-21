from tkinter import CENTER
from turtle import Turtle, speed
import pygame
from support import import_folder
from setting import *
from level import *
from particles import ParticleEffect
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles,change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 0
        self.gravity = 0.8
        self.jump_speed = -12
        self.last = -1500
        self.cooldown = 900
        self.jumpcount = 0
        self.lastjump = -300
        self.jumpcooldown = 200
        self.collision_rect = pygame.Rect(self.rect.topleft,(30,40))

        #health management
        self.change_health = change_health
        self.invisible = False
        self.invisible_duration = 1000
        self.hurt_time = 0

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_celling = False
        self.on_left = False
        self.on_right = False
        self.on_wall =False

        #audio
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.jump_sound.set_volume(0.25)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')
        self.hit_sound.set_volume(0.5)
    def import_character_assets(self):
        character_path =  '../graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'crouch':[],'crouchwalk':[],'attack':[],'dash':[],'hit':[],'attack2':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right :
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else : 
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright
        if self.invisible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
    def run_dust_animation(self):
        if self.status =='dash' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(8,11)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(8,11)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)

    def get_input(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not self.status == 'hit':
            self.direction.x = 1
            self.facing_right = True
            if keys[pygame.K_a] :
                self.direction.x =0
        elif keys[pygame.K_a] and not self.status == 'hit':
            self.direction.x = -1
            self.facing_right = False
            if keys[pygame.K_d]:
                self.direction.x =0
                self.facing_right = False
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            self.direction.x = 0
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.jumpcount < 1 and now - self.lastjump >= self.jumpcooldown and now - self.last >=self.cooldown and not self.status == 'hit':
            self.lastjump = now
            self.jump()
            self.create_jump_particles(self.rect.midbottom - pygame.math.Vector2(0,2))
            self.jumpcount += 1
        
        if self.on_ground == True:
            self.jumpcount = 0

    def get_status(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if self.direction.y < 0 and self.on_ground ==False and now - self.last >=self.cooldown :
            self.status = 'jump'
        elif self.direction.y > 1 and self.on_ground == False and now - self.last >=self.cooldown :
            self.status = 'fall'
        
        elif keys[pygame.K_LSHIFT] and now - self.last >=self.cooldown and (keys[pygame.K_d] or keys[pygame.K_a])and self.on_ground :
                self.status = 'dash'
                self.speed = 6
                self.animation_speed = 0.2
                if keys[pygame.K_d] and keys[pygame.K_a]:
                    self.status = 'idle'
        elif keys[pygame.K_e] and self.on_ground :
                self.status = 'attack2'
                self.speed = 0

        elif self.invisible and now - self.hurt_time < self.invisible_duration - 700 and self.on_ground:
            self.status = 'hit'         
                                
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
        self.collision_rect.y += self.direction.y
        self.rect.y += self.direction.y
   
    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()
    
    def get_damage(self,damage):
        if not self.invisible:
            self.hit_sound.play()
            self.change_health(damage)
            self.invisible = True
            self.hurt_time = pygame.time.get_ticks()
    
    def invisibility_timer(self):
        if self.invisible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invisible_duration:
                self.invisible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0

    def update(self):
        # self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invisibility_timer()
        self.wave_value()


            