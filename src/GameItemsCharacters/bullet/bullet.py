import pygame


bulletImg = pygame.image.load('images/gameItems/Bullet.png')

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = float(10)
		self.image = pygame.transform.scale(bulletImg, (10, 10))  # Resize the bullet image
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self, SCREEN_WIDTH, cops,gangster,bullet_group,world):
		"""
		Update the bullet's position and handle collisions.
		Args:
			SCREEN_WIDTH (int): The width of the screen.
			cops (pygame.sprite.Sprite): The cops sprite to check for collisions.
			gangster (pygame.sprite.Sprite): The gangster sprite to check for collisions.
			bullet_group (pygame.sprite.Group): The group of bullet sprites.
		Moves the bullet in its direction at its speed. If the bullet goes off-screen,
		it is removed. If the bullet collides with the gangster or cops, it reduces
		their health and is removed.
		"""
		#move bullet
		self.rect.x += (self.direction * self.speed)
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
					cop.health -= 15
					self.kill()