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
        # if keys[pygame.K_SPACE]:
        #         self.create_menu()

    def run(self):
        # self.draw_text("darkkkk",self.font,'white',100,100)
        self.input()

class Buttonstart:
    def __init__(self,surface,text,width,height,pos,elevation,creat_menu) :
        self.display_surface = surface
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'
        self.font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',18)
        self.button_sound = pygame.mixer.Sound('../audio/menu_086.wav')
        self.button_sound.set_volume(2)

        #text
        self.text_surf = self.font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        #care attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.creat_menu = creat_menu

        #bottom_rectangle
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = '#354B5E'
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.button_sound.play()
                    self.creat_menu()
                    self.pressed = False
        else:
            self.top_color = '#475F77'
    
    def draw(self):
        #eleveaion logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.display_surface,self.bottom_color,self.bottom_rect)
        pygame.draw.rect(self.display_surface,self.top_color,self.top_rect)
        self.display_surface.blit(self.text_surf,self.text_rect)
        self.check_click()
    

