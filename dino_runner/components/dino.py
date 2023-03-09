import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_SHIELD, JUMPING, JUMPING_SHIELD, RUNNING, RUNNING_SHIELD, SHIELD, SHIELD_TYPE

class Dino(Sprite):
    POS_X = 80
    POS_Y = 310
    JUMP_VEL = 8
    POS_Y_DUCK = 340

    def __init__(self):
        self.image = RUNNING [0]
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]
        self.dino_rect = self.image.get_rect() #informacion de la imagen
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y
        self.step_index = 0 #Contador de los ciclos para cambiar de imagen
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.setup_state_booleans()
        self.shield = False
        self.shield_time_up = 0
        self.show_text = False

    def setup_state_booleans (self):
        self.has_powerup = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()  

        #Estados del dinosaurio segun la tecla que presionemos

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump:  #Agregue la tecla space por comodidad con un or
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_duck and not self.dino_jump:
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
        if self.step_index <= 5:
            self.image = self.run_img[self.type][0]
        else:
            self.image = self.run_img[self.type][1]
        

        self.dino_rect.x = self.POS_X   #La posicion del dino siempre va estar en la posicion correcta
        self.dino_rect.y = self.POS_Y
        self.step_index += 1     
    
    def duck(self):
        if self.step_index <= 5:
            self.image = self.duck_img[self.type][0]
        else:
            self.image = self.duck_img[self.type][1]
        self.dino_rect.x = self.POS_X 
        self.dino_rect.y = self.POS_Y_DUCK
        self.dino_duck = False
        self.step_index += 1     

    def jump(self):
        self.image = self.jump_img[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4  #salta
            self.jump_vel -= 0.8    #cuando es negativo baja
        if self.jump_vel < -self.JUMP_VEL:  #cuando llega a JUMP_VEL en negativo se termina el salto
            self.dino_rect.y = self.POS_Y
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def check_invincibility (self, screen):
        if self.shield and self == Dino:
            time_to_show = round ((self.shield_time_up - pygame.time.get_ticks())/ 1000 , 2)
            if time_to_show >=0:
                if self.show_text:
                    font = pygame.font.Font('freesansbold.ttf', 18)
                    text = font.render(f'Shield enabled for {time_to_show}',True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (500, 40)
                    screen.blit(text, textRect)
            else:
                self.shield

    def update_to_default (self, current_type):
        if self.type == current_type:
            self.type = DEFAULT_TYPE
