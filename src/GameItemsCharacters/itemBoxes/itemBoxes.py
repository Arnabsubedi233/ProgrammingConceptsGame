import pygame
from constants.gameConstants import *

healthBox = pygame.image.load('images/gameItems/HealthBox.png')
ammoBox = pygame.image.load('images/gameItems/AmmoBox.png')
grenadeBox = pygame.image.load('images/gameItems/GrenadeBox.png')
itemBoxes = {
	'Health'	: healthBox,
	'Ammo'		: ammoBox,
	'Grenade'	: grenadeBox
}

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.original_image = itemBoxes[self.item_type]
		self.image = pygame.transform.scale(self.original_image, (self.original_image.get_width() // 7, self.original_image.get_height() // 7))
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self,gangster):
		"""
            Update the state of the item box when it collides with a gangster.
            If the item box collides with the gangster, it will apply its effect based on the item type:
            - 'Health': Increases the gangster's health by 25, up to the maximum health.
            - 'Ammo': Increases the gangster's ammo by 15.
            - 'Grenade': Increases the gangster's grenades by 3.
            After applying the effect, the item box is removed from the game.
            Args:
                gangster (Gangster): The gangster object that the item box collides with.
        """
		if pygame.sprite.collide_rect(self, gangster):
	
			if self.item_type == 'Health':
				gangster.health += 30
				if gangster.health > gangster.max_health:
					gangster.health = gangster.max_health
			elif self.item_type == 'Ammo':
				gangster.ammo += 20
			elif self.item_type == 'Grenade':
				gangster.grenades += 4
		
			self.kill()