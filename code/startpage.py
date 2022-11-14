import pygame

class start_page:
    def __init__(self,surface,creat_menu):
        self.display_surface = surface 
        self.create_menu = creat_menu
        self.font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',18)

    def draw_text(self,text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        self.display_surface.blit(img,(x,y))
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                print(1)
                self.create_menu

    def run(self):
        self.draw_text("darkkkk",self.font,'white',100,100)
        self.input()
        