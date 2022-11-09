from re import T
import pygame
from player import Player
from tiles import Tile, StaticTile,AnimateTile       
from setting import tile_size, screen_height
from support import *
from enemy import Enemy
from player import *
from game_data import levels


class Level:
    def __init__(self,current_level,surface,create_overworld,start_time):
        #level setup
        self.display_surface = surface 
        level_data = levels[current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.start_time = start_time
        # overworld connection  
        self.create_overworld = create_overworld
        self.current_level = current_level
        
        #coins setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        #player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)
        #enemies setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')
        #constraints setup
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints_layout,'constraint')
        #scoll
        self.world_shift = -10
        self.current_x = 0
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level,self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level,0)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row  in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size 

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('C:/Users/pongsapadnet/Desktop/code/game/graphics/map/Starter Tiles Platformer/BasicGreen.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        sprite_group.add(sprite)
                    
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'constraint':
                      sprite = Tile(tile_size,x,y)

                    if type == 'coins':
                        sprite = AnimateTile(tile_size,x,y,'C:/Users/pongsapadnet/Desktop/code/game/graphics/coin/gold')

                    sprite_group.add(sprite)

        return sprite_group

    def setup_player(self,layout):
        for row_index, row  in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size 
                if val == '7':
                    sprite = Player((x,y))
                    self.player.add(sprite)
                if val == '8':
                    hat_surface = pygame.image.load('C:/Users/pongsapadnet/Desktop/code/game/graphics/enemy/slime/blueslime/idle/slimeidle1.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
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

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.direction.x = 0
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    player.direction.x = 0
                    self.current_x = player.rect.right

                elif player.on_ground == False and (player.rect.left==sprite.rect.right or player.rect.right == sprite.rect.left):
                    player.on_wall = True
                else:
                    player.on_wall = False
                    
        
        if player.on_left and (player.rect.left<self.current_x or player.direction.x >=0):
            player.on_left = False
        if player.on_right and (player.rect.right<self.current_x or player.direction.x <=0):
            player.on_right = False
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
       
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_celling = True
                    player.direction.y = 0

        if player.on_ground and player.direction.y < 0 or player.direction.y >1:
            player.on_ground = False
        if player.on_celling and player.direction.y> 0:  
            player.on_celling = False
        if self.world_shift>0:
            player.rect.y += self.world_shift
    
    def check_death(self):
        now = pygame.time.get_ticks()
        if  self.player.sprite.rect.top >screen_height and  now > 1000 :
            self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level)

    def run(self):
        now = pygame.time.get_ticks()
        self.input()
        #scoll
        self.scroll_y()
        # self.display_surface.blit(self.text_surf,self.text_rect)
        #level tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        # self.terrain_sprites.update(self.world_shift)
        #coins 
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)
        
        if now - self.start_time > 10000:
            self.check_death()
            self.check_win()
       