import pygame
from GameItemsCharacters.shooter.shooter import *
from GameItemsCharacters.bullet.bullet import *
from GameItemsCharacters.grenade.grenade import *
from GameItemsCharacters.itemBoxes.itemBoxes import *
from GameItemsCharacters.healthBar.healthBar import *
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
 
#Characters
gangster = ShooterCharacter('gangster',200, 200, 1.2,2,100,5)
health_bar = HealthBar(10, 10, gangster.health, gangster.health)

cop1 = ShooterCharacter('cop',400, 200, 1.2,2,50,5)
cop2 = ShooterCharacter('cop',500, 200, 1.2,2,50,5)

#Groups
bullets = pygame.sprite.Group()
grenades = pygame.sprite.Group()
cops = pygame.sprite.Group()
explosions = pygame.sprite.Group()
itemBoxes = pygame.sprite.Group()

#temp - create item boxes
item_box = ItemBox('Health', 100, 260)
itemBoxes.add(item_box)
item_box = ItemBox('Ammo', 400, 260)
itemBoxes.add(item_box)
item_box = ItemBox('Grenade', 500, 260)
itemBoxes.add(item_box)


#adding characters to group
cops.add(cop1)
cops.add(cop2)
 
while GAME_RUNNING:
    clock.tick(FPS)
    draw_background()
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
    bullets.update(WINDOW_WIDTH,cops,gangster,bullets)
    bullets.draw(window)

    #update grenades and draw them
    grenades.update(WINDOW_WIDTH,GRAVITY,explosions,gangster,cops,TILE_SIZE)
    grenades.draw(window)

    #update explosions and draw them
    explosions.update()
    explosions.draw(window)

    itemBoxes.update(gangster)
    itemBoxes.draw(window)

       #for each cop in the group, update their attributes and then draw them
    for cop in cops:
        cop.enemy_auto(gangster,bullets)
        cop.update_character()
        cop.draw(window)
 
    #initialise movement variables
    gangster.move(left,right)
    
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
        gangster.move(left, right)
 
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