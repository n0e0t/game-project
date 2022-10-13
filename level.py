import pygame
from player import Player
from tiles import Tile
from setting import tile_size, screen_width
class Level:
    def __init__(self,level_data,surface):
        #level setup
        self.display_surface = surface 
        self.setup_level(level_data)
        self.world_shift = 0
    
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'x':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if cell == 'p':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y
        
        if player_y < screen_width/2 and direction_y <0:
            self.world_shift = 3
            player.speed = 0
        elif player_y > screen_width/2:
            self.world_shift = 0
            player.speed = 3

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
       
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
   
    def run(self):
        #level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_y()
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)