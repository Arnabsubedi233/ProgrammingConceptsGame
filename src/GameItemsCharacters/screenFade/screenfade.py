import pygame
from constants.gameConstants import *
from constants.colours import *
from constants.gameVariables import *
class ScreenFade():
	"""
    A class to handle screen fade effects in a game.
    Attributes:
    -----------
    direction : int
        The direction of the fade effect. 1 for horizontal and vertical fade, 2 for vertical fade only.
    colour : tuple
        The RGB colour value for the fade effect.
    speed : int
        The speed at which the fade effect progresses.
    fade_counter : int
        A counter to track the progress of the fade effect.
    Methods:
    --------
    fade(window):
        Applies the fade effect to the given window and returns whether the fade is complete.
    """
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self,window):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:
			pygame.draw.rect(window, self.colour, (0 - self.fade_counter, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT))
			pygame.draw.rect(window, self.colour, (WINDOW_WIDTH // 2 + self.fade_counter, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
			pygame.draw.rect(window, self.colour, (0, 0 - self.fade_counter, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
			pygame.draw.rect(window, self.colour, (0, WINDOW_WIDTH // 2 +self.fade_counter, WINDOW_WIDTH, WINDOW_HEIGHT))
		if self.direction == 2:
			pygame.draw.rect(window, self.colour, (0, 0, WINDOW_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= WINDOW_WIDTH:
			fade_complete = True

		return fade_complete