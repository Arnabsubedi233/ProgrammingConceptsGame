import pygame

class ShooterCharacter(pygame.sprite.Sprite):
	def __init__(self,character_type,x, y, scale,speed):
		pygame.sprite.Sprite.__init__(self)
		self.character_type = character_type
		self.speed = speed
		self.direction = int(1)
		self.flip = bool(False)
		sprite = pygame.image.load('images/sprites/shooter.png')
		self.image = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
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


		