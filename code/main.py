import pygame, sys
from setting import *
from level import Level
from game_data import level_0
from overworld import Overworld 
from ui import UI
from menu import menu
from score_board import *
from startpage import *
import json

score_data = {
     "name" : "",
     "score" : 0
    }       


class Game:
    def __init__(self):
        
        #audio
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')
        self.start_bg_music = pygame.mixer.Sound('../audio/start.wav')

        #game attributes
        self.max_level = 0  
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        self.score_data = score_data
        self.start_menu = 0

        #score board creation
        self.score_board = Leaderboard(screen,self.create_overworld)   
  
        #overworld creation
        self.overworld = Overworld(0,self.max_level,screen,self.create_level,self.create_startpage)
        self.start_overworld =0
        
        #menu creation
        self.menu = menu(screen,self.create_overworld,self.start_menu,self.create_startpage)
        self.status = 'start_page'

        #startpage
        self.start_page = start_page(screen,self.create_menu)  
        self.seescoreboard = seeLeaderboard(screen,self.create_startpage)

        #button
        self.buttonstart = Buttonstart(screen,"START GAME",200,60,(screen_width/2 - 90,200),6,self.create_menu)
        self.buttonscoreboard = Buttonstart(screen,"SCORE BOARD",200,60,(screen_width/2 - 90,300),6,self.create_seescoreboard)
        self.buttonexit = Buttonstart(screen,"EXIT",200,60,(screen_width/2 - 90,400),6,self.quitgame)
        

        #user interface
        self.ui = UI(screen) 
        
        #timer
        self.start_time = 0
        self.time_count = 00.00

        self.level = Level(0,screen,self.create_overworld,self.start_time,self.change_coins,self.change_health)
        

    def create_level(self,current_level):
        now = pygame.time.get_ticks()
        if now - self.start_overworld > 100 :   
            self.start_time = now
            self.level = Level(current_level,screen,self.create_overworld,self.start_time,self.change_coins,self.change_health)
            self.status = 'level'
            self.overworld_bg_music.stop()
            self.level_bg_music.play(loops= -1)
            self.level_bg_music.set_volume(0.25)

    def create_overworld(self,current_level,new_max_level):
        if new_max_level >= self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level,self.create_startpage)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.start_bg_music.stop()
        self.overworld_bg_music.play(loops= -1)
        self.overworld_bg_music.set_volume(0.25)

    def create_menu(self):
        self.menu = menu(screen,self.create_overworld,self.start_menu,self.create_startpage)
        self.status = 'menu'

    def create_scoreboard(self):
        self.score_board = Leaderboard(screen,self.create_overworld)
        self.status = 'scoreboard'
        self.level_bg_music.stop()

    def create_seescoreboard(self):
        self.seescore_board = seeLeaderboard(screen,self.create_startpage)
        self.status = 'seescoreboard'

    def create_startpage(self):
        self.start_page = start_page(screen,self.create_menu)
        self.status = 'start_page'
        score_data['name'] = ''
        self.overworld_bg_music.stop()

    def change_coins(self,amount):
        self.coins += amount
        score_data['score'] += amount

    def change_health(self,amount):
        self.cur_health += amount
        if self.cur_health > self.max_health:
            self.cur_health = self.max_health

    def check_game_over(self):
        if self.cur_health <= 0 :
            with open('score_file.json','r+') as score_file:
                file_data = json.load(score_file)
                file_data["scorefile"].append(score_data)
                score_file.seek(0)
                json.dump(file_data,score_file,indent=4)
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0,self.max_level,screen,self.create_level,self.create_startpage)
            self.status = 'scoreboard'
    
    def quitgame(self):
        pygame.quit()
        sys.exit()


    def run(self):
        now = pygame.time.get_ticks()
        if self.status == 'menu':
            self.menu.run()
            self.ui.show_name()
            self.start_overworld = now
        elif self.status == 'overworld':
            self.overworld.run()
            self.ui.show_name()
            self.ui.show_health(self.cur_health,self.max_health )
            self.ui.show_coins(self.coins)
        elif self.status == 'scoreboard':
            self.score_board.run()
            self.ui.show_name()
            self.start_overworld = now
        elif self.status == 'seescoreboard':
            self.seescoreboard.run()
            self.ui.show_name()
        elif self.status == 'start_page':
            self.start_bg_music.play(loops= -1)
            self.start_bg_music.set_volume(0.25)
            self.start_page.run()
            self.ui.show_name()
            self.ui.show_logo()
            self.buttonstart.draw()
            self.buttonscoreboard.draw()
            self.buttonexit.draw()
            self.start_menu = now
        else:
            self.level.run()
            self.ui.show_health(self.cur_health,self.max_health )
            self.ui.show_coins(self.coins)
            self.ui.show_name()
            self.start_overworld = now
            self.check_game_over()
 
#pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
font = pygame.font.Font('../graphics/iu/ARCADEPI.TTF',20)
user_text = ''
count = 0
text_x = screen_width/2
text_y = screen_height/2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game.status == 'menu' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                score_data['name'] += user_text

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
                count -=1
                text_x += 6
            elif count<=10 and not event.key == pygame.K_ESCAPE:
                user_text += event.unicode
                count +=1
                text_x -= 6
    if game.status =='level':
        screen.fill('black')
    elif game.status == 'menu':
        screen.fill('black')
        text_surface = font.render(user_text,True,'white')
        screen.blit(text_surface,(text_x,text_y))
    elif game.status == 'scoreboard':
        screen.fill('black')
    elif game.status == 'start_page':
        screen.fill('black')
    elif game.status == 'seescoreboard':
        screen.fill('black')
    else:
        screen.fill('gray')
    game.run()
    

    pygame.display.update()
    clock.tick(60)

