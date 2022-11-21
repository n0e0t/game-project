import pygame

class menu:
    def __init__(self,surface,creat_overworld,start_time,create_startpage):
        self.display_surface = surface
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',18)
        self.creat_overworld = creat_overworld
        self.start_time = start_time
        self.creat_startpage = create_startpage

    def draw_text(self,text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        self.display_surface.blit(img,(x,y))
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                self.creat_overworld(0,0)
        elif keys[pygame.K_ESCAPE]:
            self.creat_startpage()
                

    def run(self):
        now = pygame.time.get_ticks()
        self.draw_text("INPUT YOUR NAME",self.font,'white',225,200)
        self.draw_text("Press SPACE to START",self.font,'white',195,420)
        self.draw_text("Press ESC to RETURN",self.font,'white',200,470)
        if now - self.start_time >=500:
            self.input()