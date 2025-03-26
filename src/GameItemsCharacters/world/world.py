import pygame
import csv
from constants.gameConstants import *
from GameItemsCharacters.water.water import Water
from GameItemsCharacters.decorations.decorations import Decoration
from GameItemsCharacters.itemBoxes.itemBoxes import ItemBox
from GameItemsCharacters.exit.exit import Exit
from GameItemsCharacters.shooter.shooter import ShooterCharacter
from GameItemsCharacters.healthBar.healthBar import HealthBar

img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'images/tiles/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

class World():
	"""
	A class to represent the game world.
	Attributes
	----------
	obstacle_list : list
		A list to store obstacle tiles in the game world.
	level_length : int
		The length of the level data.
	Methods
	-------
	__init__():
		Initializes the World object with an empty obstacle list.
	process_data(data, water_group, decoration_group, item_box_group, exit_group, enemy_group):
		Processes the level data to create game objects and add them to their respective groups.
	draw(window, screen_scroll):
		Draws the obstacles on the game window and updates their positions based on screen scroll.
	"""
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data, water_group, decoration_group, item_box_group, exit_group, enemy_group):
		#iterate through each value in level data file
		self.level_length = len(data[0])
		for image in img_list:
			image.convert_alpha()

		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 0 and tile <= 8:
						self.obstacle_list.append(tile_data)
					elif tile >= 9 and tile <= 10:
						water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)
					elif tile >= 11 and tile <= 14:
						if tile == 14:
							img = pygame.transform.scale(img, (TILE_SIZE // 3, TILE_SIZE // 3))
						elif tile == 11:
							img = pygame.transform.scale(img, (TILE_SIZE , TILE_SIZE * 2 ))
	
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)
					elif tile == 15:#create player
						gangster = ShooterCharacter('gangster', x * TILE_SIZE, y * TILE_SIZE, 0.8, 5 ,40, 5)
						health_bar = HealthBar(10, 10, gangster.health, gangster.health)
					elif tile == 16:#create enemies
						cop = ShooterCharacter('cop', x * TILE_SIZE, y * TILE_SIZE, 0.9, 3, 20, 0)
						enemy_group.add(cop)
					elif tile == 17:#create ammo box
						item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 18:#create grenade box
						item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 19:#create health box
						item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 20:#create exit
						img = pygame.transform.scale(img, (TILE_SIZE *3 , TILE_SIZE * 3 ))
						exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)

		return gangster, health_bar


	def draw(self,window,screen_scroll):
		for tile in self.obstacle_list:
			tile[1][0] += screen_scroll
			window.blit(tile[0], tile[1])