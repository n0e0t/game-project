import pygame

class menu:
    def __init__(self,surface,creat_overworld):
        self.display_surface = surface
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',18)
        self.creat_overworld = creat_overworld

    def draw_text(self,text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        self.display_surface.blit(img,(x,y))
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                self.creat_overworld(0,0)
                

    def run(self):
        self.draw_text("INPUT YOUR NAME",self.font,'white',225,200)
        self.draw_text("Press SPACE to START",self.font,'white',195,420)
        self.input()