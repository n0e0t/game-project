from re import T
import pygame
from player import Player
from tiles import Tile, StaticTile,AnimateTile,Coin,heal,portal      
from setting import tile_size, screen_height
from support import *
from enemy import *
from player import *
from game_data import levels
from particles import ParticleEffect


class Level:
    def __init__(self,current_level,surface,create_overworld,start_time,change_coins,change_health):
        #level setup
        self.display_surface = surface 
        level_data = levels[current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.start_time = start_time
        self.enemydamage = -10
        self.imu = 0

        # audio
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.coin_sound.set_volume(0.5)
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
        self.stomp_sound.set_volume(0.5)
        self.heal_sound = pygame.mixer.Sound('../audio/effects/Suck 1V2.wav')
        self.heal_sound.set_volume(0.5)
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        #explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # overworld connection  
        self.create_overworld = create_overworld
        self.current_level = current_level
        
        #coins setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        #heal setup
        heal_layout = import_csv_layout(level_data['heal'])
        self.heal_sprites = self.create_tile_group(heal_layout,'heal')
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        #player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout,change_health)
        self.change_health = change_health

        #user interface
        self.change_coins = change_coins

        #enemies setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')
        #constraints setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints_layout,'constraint')
        #scoll
        self.world_shift = -10
        self.current_x = 0
    
    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(0,5)
        else:
            pos += pygame.math.Vector2(0,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground =False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(0,7)
            else:
                offset = pygame.math.Vector2(0,7)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level,self.new_max_level)
        elif keys[pygame.K_r]:
            self.change_health(100)
        elif keys[pygame.K_t]:
            self.imu ^= 1

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row  in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size 

                    if type == 'terrain':
                        if self.current_level == 0:
                            terrain_tile_list = import_cut_graphic('../graphics/map/Starter Tiles Platformer/BasicGreen.png')
                        elif self.current_level == 1:
                            terrain_tile_list = import_cut_graphic('../graphics/map/Starter Tiles Platformer/DarkCastle.png')  
                        elif self.current_level == 2:
                            terrain_tile_list = import_cut_graphic('../graphics/map/Starter Tiles Platformer/FireSet.png') 
                        elif self.current_level == 3:
                            terrain_tile_list = import_cut_graphic('../graphics/map/Starter Tiles Platformer/IceSet.png') 
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        sprite_group.add(sprite)
                    
                    if type == 'enemies':
                        if self.current_level == 0:
                            sprite = Enemy(tile_size,x,y)
                            self.enemydamage = -10
                        elif self.current_level == 1:
                            sprite = Enemy2(tile_size,x,y)
                            self.enemydamage = -20
                        elif self.current_level == 2:
                            sprite = Enemy3(tile_size,x,y)
                            self.enemydamage = -30
                        elif self.current_level == 3:
                            sprite = Enemy4(tile_size,x,y)
                            self.enemydamage = -40

                    if type == 'constraint':
                      sprite = Tile(tile_size,x,y)

                    if type == 'coins':
                        if self.current_level == 0:
                            sprite = Coin(tile_size,x,y,'../graphics/coin/gold',1)
                        elif self.current_level == 1:
                            sprite = Coin(tile_size,x,y,'../graphics/coin/gold',2)
                        elif self.current_level == 2:
                            sprite = Coin(tile_size,x,y,'../graphics/coin/gold',3)
                        elif self.current_level == 3:
                            sprite = Coin(tile_size,x,y,'../graphics/coin/gold',4)
                    
                    if type == 'heal':
                        sprite = heal(tile_size,x,y,'../graphics/heal')

                    sprite_group.add(sprite)

        return sprite_group

    def setup_player(self,layout,change_health):
        for row_index, row  in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size 
                if val == '7':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
                    self.player.add(sprite)
                if val == '8':
                    sprite = portal(tile_size,x,y,'../graphics/portal')
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y
        
        if player_y < screen_height/2  and  direction_y <= 0 and player.on_ground == False:
            self.world_shift = player.speed
            #player.speed = 0
        elif player_y > screen_height/2 and player_y < screen_height-64:
            self.world_shift = 0
            player.speed = 3
        elif self.world_shift < 0 :
            player.direction.x = 0
            player.speed = 0

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    player.direction.x = 0
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    player.direction.x = 0
                    self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
       
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.on_ground = True
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.on_celling = True
                    player.direction.y = 0

        if player.on_ground and player.direction.y < 0 or player.direction.y >1:
            player.on_ground = False
        if player.on_celling and player.direction.y> 0:  
             player.on_celling = False
        if self.world_shift>0:
            player.collision_rect.y += self.world_shift
            player.rect.y += self.world_shift
    
    def check_death(self):
        now = pygame.time.get_ticks()
        if  self.player.sprite.rect.top >screen_height and  now > 1000 :
            self.change_health(-50)
            self.create_overworld(self.current_level,self.current_level)

    def check_win(self):
        keys = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False) and keys[pygame.K_SPACE]:
            if self.current_level == 3:
                self.create_overworld(self.current_level,self.current_level)
                self.change_health(50)
                self.change_coins(20)
            else :
                self.change_health(50)
                self.create_overworld(self.current_level,self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)
    def check_heal_collisions(self):
        collided_heal = pygame.sprite.spritecollide(self.player.sprite,self.heal_sprites,True)
        if collided_heal:
                self.heal_sound.play()
                self.change_health(20)

    def check_enemy_collision(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -8
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion') 
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                elif self.player.sprite.status == 'attack2':
                    self.stomp_sound.play()
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion') 
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    if self.player_on_ground and self.imu == 0:
                     self.player.sprite.get_damage(self.enemydamage)

    def run(self):
        now = pygame.time.get_ticks()
        player = self.player.sprite
        self.input()
        
        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #level tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        #coins 
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #heal
        self.heal_sprites.update(self.world_shift)
        self.heal_sprites.draw(self.display_surface)

        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        
        #scoll
        self.scroll_y()
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        # self.create_landing_dust()
        self.player.draw(self.display_surface)
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)
        
        if now - self.start_time > 5500:
            player.get_input()
            self.check_death()
            self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collision()
        self.check_heal_collisions()
            
       