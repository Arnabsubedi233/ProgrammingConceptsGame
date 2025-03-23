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

level = int(1)

#Player actions
left = bool(False)
right = bool(False)
shooting = bool(False)
grenade = bool(False)
throw_grenade = bool(False)


#drawing text on screen
font = pygame.font.SysFont('Calibri', 25)

def text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	window.blit(img, (x, y))

def draw_background():
    """
    Fills the game window with the background color.

    This function uses the global variables 'window' and 'bgColour' to fill the entire
    game window with the specified background color.
    """
    window.fill(BGCOLOUR)
 

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


 
while GAME_RUNNING:
    clock.tick(FPS)
    draw_background()
    world.draw(window)
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
    bullets.update(WINDOW_WIDTH,cops,gangster,bullets,world)
    bullets.draw(window)

    #update grenades and draw them
    grenades.update(world,GRAVITY,explosions,gangster,cops,TILE_SIZE)
    grenades.draw(window)

    #update explosions and draw them
    explosions.update()
    explosions.draw(window)

    itemBoxes.update(gangster)
    itemBoxes.draw(window)

    decorations.update()
    decorations.draw(window)

    waters.update()
    waters.draw(window)

    exits.update()
    exits.draw(window)


       #for each cop in the group, update their attributes and then draw them
    for cop in cops:
        cop.enemy_auto(gangster,bullets,world)
        cop.update_character()
        cop.draw(window)
 
    #initialise movement variables
    gangster.move(left,right,world)
    
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
        gangster.move(left, right,world)
 
    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNING = False
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
                GAME_RUNNING = False
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