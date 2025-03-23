import pygame
from constants.colours import *

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self,window, health):
		"""
            Draws the health bar on the given window.

            Parameters:
            window (pygame.Surface): The surface on which to draw the health bar.
            health (int): The current health value to be displayed on the health bar.

            The health bar is drawn with three rectangles:
            - A black border rectangle.
            - A red background rectangle representing the empty health.
            - A green foreground rectangle representing the current health based on the health ratio.
        """
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(window, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(window, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(window, GREEN, (self.x, self.y, 150 * ratio, 20))