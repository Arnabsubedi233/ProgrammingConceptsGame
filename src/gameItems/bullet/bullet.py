import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = float(10)
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self, SCREEN_WIDTH, cops,gangster,bullet_group):
		#move bullet
		self.rect.x += (self.direction * self.speed)
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()

	
		if pygame.sprite.spritecollide(gangster, bullet_group, False):
			if gangster.alive:
				gangster.health -= 6
				self.kill()
		if pygame.sprite.spritecollide(cops, bullet_group, False):
			if cops.alive:
				cops.health -= 20
				self.kill()