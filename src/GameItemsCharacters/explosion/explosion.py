import pygame


class Explosion(pygame.sprite.Sprite):
	"""
	A class to represent an explosion animation in a game.
	Attributes
	----------
	images : list
		A list of images representing the frames of the explosion animation.
	frame_index : int
		The current frame index of the explosion animation.
	image : pygame.Surface
		The current image/frame of the explosion animation.
	rect : pygame.Rect
		The rectangular area of the current image.
	count : int
		A counter to control the speed of the animation.
	Methods
	-------
	__init__(x, y, scale)
		Initializes the explosion animation with the given position and scale.
	update(screen_scroll)
		Updates the explosion animation and position based on the screen scroll.
	"""
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(0, 8):
			img = pygame.image.load(f'images/Explosion/{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.frame_index = int(0)
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.count = int(0)


	def update(self,screen_scroll):
		self.rect.x += screen_scroll
		SPEED = 4
		#update explosion amimation
		self.count += 1

		if self.count >= SPEED:
			self.count = 0
			self.frame_index += 1
			#if the animation is complete then delete the explosion
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]

