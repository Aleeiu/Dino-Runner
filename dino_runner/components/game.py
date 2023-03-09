from asyncio import shield
import random
import pygame
from dino_runner.components import dino
from dino_runner.components.dino import Dino
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components import text_utils
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, CLOUD, ICON, RUNNING_HAMMER, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 230
        self.player = Dino()
        self.obstacle_manager = ObstacleManager()
        self.points = 0
        self.running = True
        self.death_count = 0
        self.power_up_manager = PowerUpManager()
        self.y_poscd  = 50
        self.x_poscd = 1000
        self.hello_index = 0
        

    def run(self):
        # Game loop: events - update - draw
        self.create_components()
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.death_count += 1
        self.reset()
        
        while self.playing:
            self.events()
            self.update()
            self.draw()
            pygame.display.update()
        self.show_menu() 
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
    


    def draw(self):
        self.score()
        self.clock.tick(FPS)
        self.screen.fill((144, 182, 197))
        self.draw_background()
        self.draw_cloud()
        self.player.draw(self.screen)  #dibujo del player
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_cloud(self):
        cdimage_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_poscd, self.y_poscd))
        self.screen.blit(CLOUD, (cdimage_width + self.x_poscd - 5, self.y_poscd + 10))
        if self.x_poscd <= -cdimage_width:
            self.screen.blit(CLOUD, (cdimage_width + self.x_poscd, self.y_poscd))
            self.x_poscd = 1000
            self.y_poscd  = random.randint(50,250)
        self.x_poscd -= self.game_speed


    def execute (self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def show_menu(self):
        self.running = True
        white_color = (255, 255, 255)
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()

    def print_menu_elements(self):
        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message('Press any Key to start')
            self.screen.blit(text, text_rect)
            pygame.mixer.music.load("lofi.MP3")
            pygame.mixer.music.play(-1)
            
            
        else:
            score_text, score_rect = text_utils.get_centered_message('Your score: '+ str(self.last_score),width = SCREEN_WIDTH // 2, height = SCREEN_HEIGHT // 2.4)
            death_text, death_rect = text_utils.get_centered_message('Your deaths: '+str(self.death_count))
        
            self.screen.blit(score_text, score_rect)
            self.screen.blit(death_text, death_rect)

        self.screen.blit(RUNNING_HAMMER[0], (500, 350))
        if self.hello_index <= 5:
            self.image = RUNNING_HAMMER[0]
        else:
            self.image = RUNNING_HAMMER[1]
            self.hello_index += 1

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element(self.points)
        self.screen.blit(text, text_rect)
        pygame.display.update
        self.last_score = self.points - 2

        self.screen.blit(text, text_rect)
        self.player.check_invincibility(self.screen)

    def create_components(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points)

    def reset(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.load("lofi.MP3")
        pygame.mixer.music.play(-1)
        self.points = 0
        self.game_speed = 20

