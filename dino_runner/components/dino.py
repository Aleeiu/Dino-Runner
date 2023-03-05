import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import JUMPING, RUNNING

class Dino(Sprite):
    POS_X = 80
    POS_Y = 310
    JUMP_VEL = 8
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect() #informacion de la imagen
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y
        self.step_index = 0 #Contador de los ciclos para cambiar de imagen
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()  

        #Estados del dinosaurio segun la tecla que presionemos

        if user_input[pygame.K_UP] or user_input[pygame.K_SPACE] and not self.dino_jump:  #Agregue la tecla space por comodidad con un or
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_duck:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_duck = False
            self.dino_jump = False
            self.dino_run = True

        if self.step_index >= 10:  #resetea el contador para cambio de imagen
            self.step_index = 0 

    def draw(self,screen):
        screen.blit(self.image,(self.dino_rect.x,self.dino_rect.y))

    def run(self):
        if self.step_index < 5:
            self.image = RUNNING[0]
        else:
            self.image = RUNNING[1]

        self.dino_rect.x = self.POS_X   #La posicion del dino siempre va estar en la posicion correcta
        self.dino_rect.y = self.POS_Y
        self.step_index += 1     
    
    def duck(self):
        pass

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4  #salta
            self.jump_vel -= 0.8    #cuando es negativo baja
        if self.jump_vel < -self.JUMP_VEL:  #cuando llega a JUMP_VEL en negativo se termina el salto
            self.dino_rect.y = self.POS_Y
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL