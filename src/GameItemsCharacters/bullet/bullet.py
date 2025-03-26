import pygame


bulletImg = pygame.image.load('images/gameItems/Bullet.png')

class Bullet(pygame.sprite.Sprite):
	"""
	A class to represent a bullet in the game.
	Attributes
	----------
	speed : float
		The speed at which the bullet travels.
	image : pygame.Surface
		The image of the bullet.
	rect : pygame.Rect
		The rectangular area of the bullet image.
	direction : int
		The direction in which the bullet travels.
	Methods
	-------
	update(SCREEN_WIDTH, cops, gangster, bullet_group, world, screen_scroll):
		Updates the position of the bullet and handles collisions.
	"""
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = float(10)
		self.image = pygame.transform.scale(bulletImg, (10, 10))  # Resize the bullet image
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self, SCREEN_WIDTH, cops,gangster,bullet_group,world,screen_scroll):
		self.rect.x += (self.direction * self.speed) + screen_scroll

		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()

		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):
				self.kill()

		if pygame.sprite.spritecollide(gangster, bullet_group, False):
			if gangster.alive:
				gangster.health -= 9
				self.kill()
		for cop in cops:
			if pygame.sprite.spritecollide(cop, bullet_group, False):
				if cop.alive:
					cop.health -= 20
					self.kill()