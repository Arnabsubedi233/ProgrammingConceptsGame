import pygame
import os
import random
from constants.gameConstants import *
from constants.gameVariables import SCROLLING_THRESHOLD, GRAVITY
from GameItemsCharacters.bullet.bullet import Bullet



class ShooterCharacter(pygame.sprite.Sprite): #This class is a subcla
    class ShooterCharacter(pygame.sprite.Sprite):
        """
        A class to represent a shooter character in the game.
        Attributes:
        ----------
        character_type : str
            The type of the character (e.g., 'gangster').
        speed : int
            The speed of the character.
        ammo : int
            The amount of ammunition the character has.
        begin_ammo : int
            The initial amount of ammunition the character has.
        shooting_cooldown : int
            The cooldown time between shots.
        health : float
            The health of the character.
        grenades : int
            The number of grenades the character has.
        max_health : float
            The maximum health of the character.
        direction : int
            The direction the character is facing (1 for right, -1 for left).
        flip : bool
            Whether the character's image should be flipped.
        alive : bool
            Whether the character is alive.
        vel_y : float
            The vertical velocity of the character.
        jump : bool
            Whether the character is jumping.
        in_air : bool
            Whether the character is in the air.
        animation_list : list
            A list of animations for the character.
        frame_index : int
            The current frame index of the animation.
        action : int
            The current action of the character.
        update_time : int
            The time when the animation was last updated.
        move_counter : int
            A counter for the character's movement.
        sight : pygame.Rect
            The sight range of the character.
        still : bool
            Whether the character is still.
        still_counter : int
            A counter for how long the character remains still.
        Methods:
        -------
        enemy_auto(gangster, bullets, world, screen_scroll, background_scroll, waters, exits, shooting_sound):
            Controls the automatic behavior of the enemy character.
        update_character():
            Updates the character's animation and checks if the character is alive.
        move(left, right, world, bg_scroll, waters, exits):
            Moves the character based on input and checks for collisions.
        animation():
            Updates the character's animation.
        check_alive():
            Checks if the character is alive and updates its state.
        shoot(bullet_group, shooting_sound):
            Shoots a bullet if the cooldown period has passed and the character has ammo.
        update_action(new_action):
            Updates the character's action and resets the animation frame index.
        draw(window):
            Draws the character on the given window.
        """
    def __init__(self,character_type,x, y, scale,speed,ammo,grenades):
        pygame.sprite.Sprite.__init__(self)
        #Character attributes
        self.character_type = character_type
        self.speed = speed
        self.ammo = ammo
        self.begin_ammo = ammo
        self.shooting_cooldown = int(0)
        self.health = float(100)
        self.grenades = grenades
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
        #Enemy variables
        self.move_counter = int(0)
        self.sight = pygame.Rect(0, 0, 150, 20)
        self.still = bool(False)
        self.still_counter = int(0)

       
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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
  
    
    def enemy_auto(self,gangster,bullets,world,screen_scroll,background_scroll,waters,exits,shooting_sound):
        if self.alive and gangster.alive:
            if self.still == False and random.randint(1, 200) == 1:
                self.update_action(0)  
                self.still = True
                self.still_counter = 50
            if self.sight.colliderect(gangster.rect):
                self.update_action(0) 
                self.shoot(bullets,shooting_sound)
                
            else:
                if self.still == False:
                    if self.direction == 1:
                        enemy_moving_right = True
                    else:
                        enemy_moving_right = False
                    enemy_moving_left = not enemy_moving_right
                    self.move(enemy_moving_left, enemy_moving_right,world,background_scroll,waters,exits)
                    self.update_action(1) 
                    self.move_counter += 1
                    self.sight.center = (
                        self.rect.centerx + 75 * self.direction,
                        self.rect.centery
                    )

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.still_counter -= 1
                    if self.still_counter <= 0:
                        self.still = False
       
        self.rect.x += screen_scroll

    def update_character(self):
        self.animation()
        self.check_alive()
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1

 
    def move (self,left,right,world,bg_scroll,waters,exits):
        level_end = False
        screen_scroll = int(0)
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
            self.vel_y = -14
            self.jump = False
            self.in_air = True
 
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y


        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        
        if pygame.sprite.spritecollide(self, waters, False):
            self.health = 0
        
        if pygame.sprite.spritecollide(self, exits, False):
            level_end = True
        
        if self.rect.bottom > WINDOW_HEIGHT:
            self.health = 0
            
        if self.character_type == 'gangster':
            if self.rect.left + dx < 0 or self.rect.right + dx > WINDOW_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.character_type == 'gangster':
            if (self.rect.right > WINDOW_WIDTH - SCROLLING_THRESHOLD and bg_scroll < (world.level_length * TILE_SIZE) - WINDOW_WIDTH) or (self.rect.left < SCROLLING_THRESHOLD and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx  

        return screen_scroll, level_end


 
   
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
    
    def shoot(self,bullet_group,shooting_sound):
        if self.shooting_cooldown == 0 and self.ammo > 0:
            self.shooting_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.7 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
            shooting_sound.play()
 
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
 
 
 
    def draw(self,window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)