import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
     def __init__(self,image):
        self.image = BIRD[0]
        self.dino_rect = self.image.get_rect() #informacion de la imagen
        self.type = 0
        super().__init__(image,self.type)
        self.rect.y = random.choice([240, 300, 325])
        self.fly_index = 0
        

     def draw(self,screen):
        if self.fly_index >= 10: 
            self.fly_index = 0 
        if self.fly_index <= 5:
            self.image = BIRD[0]
        else:
             self.image = BIRD[1]

        screen.blit(self.image,(self.rect.x,self.rect.y))
        self.fly_index += 1
