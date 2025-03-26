import pygame
from constants.gameConstants import *

class Exit(pygame.sprite.Sprite):
	"""
	A class to represent an exit in the game.
	Attributes
	----------
	image : pygame.Surface
		The image representing the exit.
	rect : pygame.Rect
		The rectangular area of the image.
	Methods
	-------
	__init__(img, x, y):
		Initializes the Exit object with an image and position.
	update(screen_scroll):
		Updates the position of the exit based on the screen scroll.
	"""
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
	
	def update(self,screen_scroll):
		self.rect.x += screen_scroll

