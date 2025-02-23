import pygame

class ShooterCharacter(pygame.sprite.Sprite):
	def __init__(self,x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		sprite = pygame.image.load('images/sprites/shooter.png')
		self.image = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self, window):
		window.blit(self.image, self.rect)