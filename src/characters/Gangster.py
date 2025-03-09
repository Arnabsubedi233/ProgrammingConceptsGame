import pygame
import os

class ShooterCharacter(pygame.sprite.Sprite): #This class is a subcla
	def __init__(self,character_type,x, y, scale,speed):
		pygame.sprite.Sprite.__init__(self)
		#Character attributes
		self.character_type = character_type
		self.speed = speed
		self.direction = int(1)
		self.flip = bool(False)
		self.alive = bool(True)
		self.velocity_y = float(0)
		self.jump = bool(False)
		self.in_air = bool(False)
		self.animation_list = []
		self.frame_index = int(0)
		self.action = int(0)
		self.update_time = pygame.time.get_ticks()
		
		#animation configuration
		animations = ['Idle','Run','Jump']
		for animation in animations:
			list = []
			no_frames = len(os.listdir(f'images/{self.character_type}/{animation}'))
			for i in range(no_frames):
				animation_img = pygame.image.load(f'imgages/{self.character_type}/{animation}/{i}.png')
				animation_img = pygame.transform.scale(animation_img, (int(animation_img.get_width() * scale), int(animation_img.get_height() * scale)))
				list.append(animation_img)
			self.animation_list.append(list)


		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
	
	def draw(self, window):
		window.blit(pygame.transform.flip(self.image,self.flip,False), self.rect) 	
	

	def move (self,left,right):
			
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
		self.rect.x += dx
		self.rect.y += dy


		