import pygame
from constants.gameConstants import *

healthBox = pygame.image.load('images/gameItems/HealthBox.png')
ammoBox = pygame.image.load('images/gameItems/AmmoBox.png')
grenadeBox = pygame.image.load('images/gameItems/GrenadeBox.png')
itemBoxes = {
	'Health'	: healthBox,
	'Ammo'		: ammoBox,
	'Grenade'	: grenadeBox
}

class ItemBox(pygame.sprite.Sprite):
	"""
	A class to represent an item box in the game.
	Attributes:
	-----------
	item_type : str
		The type of item contained in the box (e.g., 'Health', 'Ammo', 'Grenade').
	original_image : pygame.Surface
		The original image of the item box.
	image : pygame.Surface
		The scaled image of the item box.
	rect : pygame.Rect
		The rectangular area of the item box for collision detection.
	Methods:
	--------
	__init__(item_type, x, y):
		Initializes the item box with the specified type and position.
	update(gangster, screen_scroll):
		Updates the position of the item box and checks for collisions with the gangster.
	"""
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.original_image = itemBoxes[self.item_type]
		self.image = pygame.transform.scale(self.original_image, (self.original_image.get_width() // 7, self.original_image.get_height() // 7))
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self,gangster,screen_scroll):
		self.rect.x += screen_scroll
		if pygame.sprite.collide_rect(self, gangster):
	
			if self.item_type == 'Health':
				gangster.health += 60
				if gangster.health > gangster.max_health:
					gangster.health = gangster.max_health
			elif self.item_type == 'Ammo':
				gangster.ammo += 20
			elif self.item_type == 'Grenade':
				gangster.grenades += 4
		
			self.kill()