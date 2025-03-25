import pygame
from constants.gameConstants import *
from constants.colours import *
from constants.gameVariables import *
class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self,window):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:#whole screen fade
			pygame.draw.rect(window, self.colour, (0 - self.fade_counter, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT))
			pygame.draw.rect(window, self.colour, (WINDOW_WIDTH // 2 + self.fade_counter, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
			pygame.draw.rect(window, self.colour, (0, 0 - self.fade_counter, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
			pygame.draw.rect(window, self.colour, (0, WINDOW_WIDTH // 2 +self.fade_counter, WINDOW_WIDTH, WINDOW_HEIGHT))
		if self.direction == 2:#vertical screen fade down
			pygame.draw.rect(window, self.colour, (0, 0, WINDOW_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= WINDOW_WIDTH:
			fade_complete = True

		return fade_complete