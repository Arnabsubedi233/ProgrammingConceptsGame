import pygame
from constants.gameConstants import *

class Decoration(pygame.sprite.Sprite):
	"""
	A class to represent a decoration in the game.

	Attributes
	----------
	image : pygame.Surface
		The image of the decoration.
	rect : pygame.Rect
		The rectangle representing the position and dimensions of the decoration.

	Methods
	-------
	__init__(img, x, y)
		Initializes the decoration with an image and position.
	update(screen_scroll)
		Updates the position of the decoration based on screen scroll.
	"""
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 4, y + (TILE_SIZE - self.image.get_height()))
	def update(self,screen_scroll):
		self.rect.x += screen_scroll

