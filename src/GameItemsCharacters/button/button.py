import pygame 

#button class
class Button():
	"""
    A class to represent a button in a Pygame application.
    Attributes
    ----------
    image : pygame.Surface
        The scaled image of the button.
    rect : pygame.Rect
        The rectangle area of the button.
    clicked : bool
        A flag to check if the button has been clicked.
    Methods
    -------
    __init__(x, y, image, scale):
        Initializes the button with position, image, and scale.
    draw(window):
        Draws the button on the given window and checks for click events.
    """
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, window):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		window.blit(self.image, (self.rect.x, self.rect.y))

		return action