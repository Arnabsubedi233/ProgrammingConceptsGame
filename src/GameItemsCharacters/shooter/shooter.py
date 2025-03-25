import pygame
import os
import random
from constants.gameConstants import *
from constants.gameVariables import SCROLLING_THRESHOLD, GRAVITY
from GameItemsCharacters.bullet.bullet import Bullet

class ShooterCharacter(pygame.sprite.Sprite): #This class is a subcla
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
  
    
    def enemy_auto(self,gangster,bullets,world,screen_scroll,background_scroll,waters,exits):
        """
        Controls the automatic behavior of an enemy character.
        Parameters:
        gangster (object): The enemy character that this character interacts with.
        bullets (list): A list to store bullets fired by the enemy.
        Behavior:
        - If both the enemy and the gangster are alive:
            - If the enemy is not still and a random condition is met, the enemy stops moving for a short period.
            - If the gangster is within the enemy's sight, the enemy stops moving and shoots.
            - If the gangster is not within sight and the enemy is not still:
                - The enemy moves in the current direction and updates its action.
                - The enemy's sight is adjusted based on its direction.
                - If the enemy has moved a certain distance, it changes direction.
            - If the enemy is still, it counts down the still counter and resumes movement when the counter reaches zero.
        """
        if self.alive and gangster.alive:
            if self.still == False and random.randint(1, 200) == 1:
                self.update_action(0)  
                self.still = True
                self.still_counter = 50
            if self.sight.colliderect(gangster.rect):
                self.update_action(0) 
                self.shoot(bullets)
                
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
        """
        Updates the character's state by performing the following actions:
        - Calls the animation method to update the character's animation.
        - Checks if the character is alive by calling the check_alive method.
        - Decreases the shooting cooldown timer if it is greater than zero.
        """
        self.animation()
        self.check_alive()
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1

 
    def move (self,left,right,world,bg_scroll,waters,exits):
        """
        Moves the character based on input directions and applies gravity.
        Args:
            left (bool): If True, move the character to the left.
            right (bool): If True, move the character to the right.
        Attributes:
            GRAVITY (float): The gravity constant affecting the character's vertical velocity.
            dx (int): The change in the character's horizontal position.
            dy (int): The change in the character's vertical position.
        Behavior:
            - Moves the character left or right based on input.
            - Flips the character's direction based on movement.
            - Initiates a jump if the character is not already in the air.
            - Applies gravity to the character's vertical velocity.
            - Limits the character's vertical velocity to a maximum value.
            - Prevents the character from falling below a certain point (ground level).
        """
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
        """
        Updates the current animation frame of the character.

        This method updates the character's image to the next frame in the animation
        sequence based on the current action and frame index. It also handles the
        timing of the frame updates using a cooldown period.

        Attributes:
            COOLDOWN (int): The time in milliseconds between frame updates.
            self.image (Surface): The current image of the character based on the animation list.
            self.animation_list (list): A list of lists containing animation frames for different actions.
            self.action (int): The current action being performed by the character.
            self.frame_index (int): The current frame index in the animation list.
            self.update_time (int): The time when the last frame update occurred.

        Behavior:
            - Updates the character's image to the next frame in the animation list.
            - Resets the frame index to 0 if the end of the animation list is reached,
              except for action 3, where the frame index is set to the last frame.
        """
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
        """
        Check if the character is alive based on its health.

        If the character's health is less than or equal to 0, set the health to 0,
        speed to 0, and alive status to False. Also, update the character's action
        to a specific state (e.g., death animation).

        Returns:
            None
        """
        if self.health <= 0:
            self.health = float(0)
            self.speed = float(0)
            self.alive = bool(False)
            self.update_action(3)
    
    def shoot(self,bullet_group):
        """
        Handles the shooting action for the character.

        Args:
            bullet_group (pygame.sprite.Group): The group to which the new bullet will be added.

        Behavior:
            - Checks if the shooting cooldown is zero and there is ammo available.
            - Resets the shooting cooldown to 20.
            - Creates a new bullet at the character's position, adjusted by direction.
            - Prints the character's current health.
            - Adds the new bullet to the bullet group.
            - Decreases the ammo count by 1.
        """
        if self.shooting_cooldown == 0 and self.ammo > 0:
            self.shooting_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.7 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
 
    def update_action(self, new_action):
        """
        Update the current action of the shooter.

        Args:
            new_action (int): The new action to be set. If it is different from the current action,
                              the action will be updated, the frame index will be reset to 0, and
                              the update time will be set to the current time in milliseconds.
        """
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
 
 
 
    def draw(self,window):
        """
        Draws the shooter character on the given window.

        Args:
            window (pygame.Surface): The surface on which to draw the shooter character.
        """
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)