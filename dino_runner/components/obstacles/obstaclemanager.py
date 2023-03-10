import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus, CactusLarge
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS


class ObstacleManager:
    def __init__(self):
        self.obstacles = []


    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_type = random.randint(0,2)
            if obstacle_type ==  0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif obstacle_type == 1:
                self.obstacles.append(CactusLarge(LARGE_CACTUS))
            else:
                self.obstacles.append(Bird(LARGE_CACTUS))
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    pygame.mixer.music.stop()
                    pygame.time.delay(1000)
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
