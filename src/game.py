import pygame
from GameItemsCharacters.shooter.shooter import *
from GameItemsCharacters.bullet.bullet import *
from GameItemsCharacters.grenade.grenade import *
from GameItemsCharacters.itemBoxes.itemBoxes import *
from GameItemsCharacters.healthBar.healthBar import *
from GameItemsCharacters.decorations.decorations import *
from GameItemsCharacters.water.water import *
from GameItemsCharacters.world.world import *
from GameItemsCharacters.exit.exit import *
from GameItemsCharacters.button.button import *
from constants.gameConstants import *
from constants.colours import *
from constants.gameVariables import *

#pygame initialisation
pygame.init()

#screen configurations
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Cops and Robbers Game')
 
#Clock Settings
clock = pygame.time.Clock()

#Game Variables
game_start = bool(False)
level = int(1)
window_scroll = int(0)
background_scroll = int(0)
game_running = True

#background configurations
start = pygame.image.load('images/ui/Start.png').convert_alpha()
restart = pygame.image.load('images/ui/Restart.png').convert_alpha()
exit = pygame.image.load('images/ui/Exit.png').convert_alpha()

city1_img = pygame.image.load('images/background/city1.png').convert_alpha()
buildingOverlay_img = pygame.image.load('images/background/buildingOverlay.png').convert_alpha()
sky_img = pygame.image.load('images/background/sky.png').convert_alpha()

def draw_bg():
    window.fill(BGCOLOUR)
    width = sky_img.get_width()
    buildingOverlay_new_img = pygame.transform.scale(buildingOverlay_img, (buildingOverlay_img.get_width() * 2, buildingOverlay_img.get_height()*2))
    city1_new_img = pygame.transform.scale(city1_img, (city1_img.get_width() * 2.5, city1_img.get_height()*2.5))

    for x in range(5):
        window.blit(sky_img, ((x * width) - background_scroll * 0.5, 0))
        window.blit(buildingOverlay_img, ((x * width) - background_scroll * 0.6, WINDOW_HEIGHT - buildingOverlay_img.get_height() - 350))
        window.blit(buildingOverlay_new_img, ((x * width) - background_scroll * 0.7, WINDOW_HEIGHT - city1_img.get_height() - 300))
        window.blit(buildingOverlay_new_img, ((x * width) - background_scroll * 0.8, WINDOW_HEIGHT - city1_img.get_height()-200))
        window.blit(city1_new_img, ((x * width) - background_scroll * 0.9, WINDOW_HEIGHT - city1_img.get_height()-100))

#resetting level

#function to reset level
def level_reset():
	cops.empty()
	bullets.empty()
	grenades.empty()
	explosions.empty()
	itemBoxes.empty()
	decorations.empty()
	waters.empty()
	exits.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLUMNS
		data.append(r)

	return data

#drawing text on screen
font = pygame.font.SysFont('Calibri', 25)

def text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	window.blit(img, (x, y))
     
#Player actions
left = bool(False)
right = bool(False)
shooting = bool(False)
grenade = bool(False)
throw_grenade = bool(False)

#create buttons
start_button = Button(WINDOW_WIDTH // 2- 200 , WINDOW_HEIGHT // 2 - 125 , start, 2)
exit_button = Button(WINDOW_WIDTH // 2-200 , WINDOW_HEIGHT // 2 + 75, exit, 2)
restart_button = Button(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50, restart, 2)


#Groups
bullets = pygame.sprite.Group()
grenades = pygame.sprite.Group()
cops = pygame.sprite.Group()
explosions = pygame.sprite.Group()
itemBoxes = pygame.sprite.Group()
decorations = pygame.sprite.Group()
waters = pygame.sprite.Group()
exits = pygame.sprite.Group()


#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLUMNS
	world_data.append(r)
#load in level data and create world
with open(f'levels/level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
    
world = World()
gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)


 
while game_running:
    clock.tick(FPS)

    if game_start == False:
         window.fill(BLACK)
         if start_button.draw(window):
                game_start = True
         if exit_button.draw(window):
                game_running = False
    else:
        draw_bg()
        world.draw(window,window_scroll)
        health_bar.draw(window, gangster.health)

        text('AMMO: ', font, WHITE, 10, 35)
        text(f'{gangster.ammo}',font,WHITE,(90), 35)
        transformedBullet = pygame.transform.scale(bulletImg, (10, 10))
        window.blit(transformedBullet, (140, 40))

        text('GRENADES: ', font, WHITE, 10, 60)
        text(f'{gangster.grenades}',font,WHITE,(135), 60)
        window.blit(grenadeImg, (155, 55))

        
        #update character attributes and then draw them
        gangster.update_character()
        gangster.draw(window)

        #update bullets and draw them
        bullets.update(WINDOW_WIDTH,cops,gangster,bullets,world,window_scroll)
        bullets.draw(window)

        #update grenades and draw them
        grenades.update(world,GRAVITY,explosions,gangster,cops,TILE_SIZE,window_scroll)
        grenades.draw(window)

        #update explosions and draw them
        explosions.update(window_scroll)
        explosions.draw(window)

        itemBoxes.update(gangster,window_scroll)
        itemBoxes.draw(window)

        decorations.update(window_scroll)
        decorations.draw(window)

        waters.update(window_scroll)
        waters.draw(window)

        exits.update(window_scroll)
        exits.draw(window)


        #for each cop in the group, update their attributes and then draw them
        for cop in cops:
            cop.enemy_auto(gangster,bullets,world,window_scroll,background_scroll,waters,exits)
            cop.update_character()
            cop.draw(window)
    

        
        #check if the gangster is alive then carry out functionalities 
        if gangster.alive:
            if shooting:
                gangster.shoot(bullets)
            elif grenade and throw_grenade == False and gangster.grenades > 0:
                grenade = Grenade(gangster.rect.centerx + (0.5 * gangster.rect.size[0] * gangster.direction),\
                                gangster.rect.top, gangster.direction)
                grenades.add(grenade)
                #reduce grenades
                gangster.grenades -= 1
                throw_grenade = True
            if gangster.in_air:
                gangster.update_action(2)  # 2: jump
            elif left or right:
                gangster.update_action(1)  # 1: run
            else:
                gangster.update_action(0)  # 0: idle
            window_scroll,level_end = gangster.move(left, right,world,background_scroll,waters,exits)
            background_scroll -= window_scroll
            if level_end:
                 level += 1
                 print(level)
                 background_scroll = 0
                 world_data = level_reset()
                 if level <= MAXIMUM_LEVELS:
                    with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)
        else:
             window_scroll = 0
             if restart_button.draw(window):
                background_scroll = 0
                world_data = level_reset()
                with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_w and gangster.alive:
                gangster.jump = True
            if event.key == pygame.K_SPACE:
                shooting = True
            if event.key == pygame.K_ESCAPE:
                game_running = False
            if event.key == pygame.K_q:
                grenade = True
 
 
        #Reset Events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_SPACE:
                shooting = False
            if event.key == pygame.K_q:
                grenade = False
                throw_grenade = False
     
 
    pygame.display.update()
 
pygame.quit()