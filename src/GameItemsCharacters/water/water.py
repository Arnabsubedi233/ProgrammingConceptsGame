import pygame
from constants.gameConstants import *

class Water(pygame.sprite.Sprite):
	"""
	A class to represent a water sprite in the game.
	Attributes
	----------
	image : Surface
		The image of the water sprite.
	rect : Rect
		The rectangular area of the sprite.
	Methods
	-------
	__init__(img, x, y)
		Initializes the water sprite with an image and position.
	update(screen_scroll)
		Updates the position of the water sprite based on screen scroll.
	"""
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
	
	def update(self,screen_scroll):
		self.rect.x += screen_scroll