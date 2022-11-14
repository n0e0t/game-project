import pygame
from setting import screen_height,screen_width
import json

f = open('score_file.json')
data_score = json.load(f)
data = sorted(data_score["scorefile"],key=lambda k:k["score"],reverse=True)[:5]



class Leaderboard:
    def __init__(self,surface,create_overworld):
        self.display_surface = surface
        self.font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',20)
        self.create_overworld = create_overworld
        self.data = data

    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                self.create_overworld(0,1)
    
    def run(self):
        for index, data in enumerate(self.data):
            name_text = self.font.render(f"{data['name']}",True,'white')
            name_text_rect = name_text.get_rect(
                midleft=(screen_width / 2 - 130, 230 + (index * 50)))
            self.display_surface.blit(name_text, name_text_rect)

            score_text = self.font.render(f"{data['score']}",True,'white')
            score_text_rect = score_text.get_rect(
                midleft=(screen_width / 2 + 100, 230 + (index * 50)))
            self.display_surface.blit(score_text, score_text_rect)
        name_ui = self.font.render("NAME",True,'white')
        name_ui_rect = name_ui.get_rect(midleft = (screen_width/2 - 145,180))
        self.display_surface.blit(name_ui,name_ui_rect)
        score_ui = self.font.render("SCORE",True,'white')
        score_ui_rect = score_ui.get_rect(midleft = (screen_width/2 + 75,180))
        self.display_surface.blit(score_ui,score_ui_rect)
        scoreboard_ui = self.font.render("SCORE BOARD",True,'white')
        scoreboard_ui_rect = scoreboard_ui.get_rect(center = (screen_width/2,130))
        self.display_surface.blit(scoreboard_ui,scoreboard_ui_rect)
        press_ui = self.font.render("Press SPACE to RESTART",True,'white')
        press_ui_rect = press_ui.get_rect(center = (screen_width/2,500))
        self.display_surface.blit(press_ui,press_ui_rect)
        
        self.input()