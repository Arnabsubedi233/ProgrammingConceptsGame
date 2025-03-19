import pygame
import os
 
class ShooterCharacter(pygame.sprite.Sprite): #This class is a subcla
    def __init__(self,character_type,x, y, scale,speed,ammo):
        pygame.sprite.Sprite.__init__(self)
        #Character attributes
        self.character_type = character_type
        self.speed = speed
        self.ammo = ammo
        self.begin_ammo = ammo
        self.shooting_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = int(1)
        self.flip = bool(False)
        self.alive = bool(True)
        self.vel_y = float(0)
        self.jump = bool(False)
        self.in_air = bool(False)
        self.animation_list = []
        self.frame_index = int(0)
        self.action = int(0)
        self.update_time = pygame.time.get_ticks()
       
        #animation configuration
        animations = ['Idle','Run','Jump','Dead']
        for animation in animations:
            list = []
            no_frames = len(os.listdir(f'images/{self.character_type}/{animation}'))
            for i in range(no_frames):
                animation_img = pygame.image.load(f'images/{self.character_type}/{animation}/{i}.png').convert_alpha()
                animation_img = pygame.transform.scale(animation_img, (int(animation_img.get_width() * scale), int(animation_img.get_height() * scale)))
                list.append(animation_img)
            self.animation_list.append(list)
 
 
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_character(self):
        self.animation()
        self.check_alive()

 
    def move (self,left,right):
        GRAVITY = float(0.75)
        dx = int(0)
        dy = int(0)
 
        if left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
 
        if right:
            dx = self.speed
            self.flip = False
            self.direction = 1
 
        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
 
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
 
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
 
        self.rect.x += dx
        self.rect.y += dy
 
   
    def animation(self):
        COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = float(0)
            self.speed = float(0)
            self.alive = bool(False)
            self.update_action(3)
 
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
 
 
 
    def draw(self,window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)