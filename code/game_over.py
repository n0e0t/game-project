import pygame
from setting import screen_height,screen_width

class game_over:
    def __init__(self,surface,create_score_board) -> None:
        self.display_surface = surface
        self.font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',20)
        self.create_score_board = create_score_board

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                self.create_score_board(0,1)