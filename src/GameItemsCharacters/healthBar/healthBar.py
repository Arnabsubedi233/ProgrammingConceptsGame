import pygame
from constants.colours import *

class HealthBar():
	"""
	A class to represent a health bar in a game.
	Attributes
	----------
	x : int
		The x-coordinate of the health bar.
	y : int
		The y-coordinate of the health bar.
	health : int
		The current health value.
	max_health : int
		The maximum health value.
	Methods
	-------
	draw(window, health):
		Draws the health bar on the given window with the updated health value.
	"""
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self,window, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(window, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(window, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(window, GREEN, (self.x, self.y, 150 * ratio, 20))