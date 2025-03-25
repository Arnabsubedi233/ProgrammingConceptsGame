import pygame


class Explosion(pygame.sprite.Sprite):
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
		"""
        Update the explosion animation.
        This method increments the counter and updates the frame index of the explosion animation.
        If the counter reaches the defined EXPLOSION_SPEED, it resets the counter and advances the frame index.
        If the frame index exceeds the number of available images, the explosion object is deleted.
        Otherwise, the current image of the explosion is updated to the next frame.
        Attributes:
            EXPLOSION_SPEED (int): The speed at which the explosion animation progresses.
            counter (int): The current counter value for the explosion animation.
            frame_index (int): The current frame index of the explosion animation.
            images (list): A list of images representing the explosion animation frames.
        """
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

