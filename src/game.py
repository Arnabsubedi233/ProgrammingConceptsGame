import pygame
from GameItemsCharacters.shooter.shooter import *
from GameItemsCharacters.bullet.bullet import *
from GameItemsCharacters.grenade.grenade import *
 
pygame.init()

 
#constants
WINDOW_WIDTH = int(800)
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.8)
TILE_SIZE= float(50)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Cops and Robbers Game')
 
#FPS Settings
clock = pygame.time.Clock()
FPS = float(60)
 
#Player actions
left = bool(False)
right = bool(False)
shooting = bool(False)
grenade = bool(False)
throw_grenade = bool(False)
 
#Game Variables
GRAVITY = float(0.75)
GAME_RUNNING = True
 
#colours
bgColour = tuple((100,200,130))
 

def draw_background():
    """
    Fills the game window with the background color.

    This function uses the global variables 'window' and 'bgColour' to fill the entire
    game window with the specified background color.
    """
    window.fill(bgColour)
 
#Characters
gangster = ShooterCharacter('gangster',200, 200, 1.2,2,100,5)
cop1 = ShooterCharacter('cop',400, 200, 1.2,2,1,5)
cop2 = ShooterCharacter('cop',500, 200, 1.2,2,1,5)

#Groups
bullets = pygame.sprite.Group()
grenades = pygame.sprite.Group()
cops = pygame.sprite.Group()
explosions = pygame.sprite.Group()

#adding characters to group
cops.add(cop1)
cops.add(cop2)
 
while GAME_RUNNING:
    clock.tick(FPS)

    draw_background()
    
    #update character attributes and then draw them
    gangster.update_character()
    gangster.draw(window)

    #for each cop in the group, update their attributes and then draw them
    for cop in cops:
        cop.update_character()
        cop.draw(window)

    #update bullets and draw them
    bullets.update(WINDOW_WIDTH,cops,gangster,bullets)
    bullets.draw(window)

    #update grenades and draw them
    grenades.update(WINDOW_WIDTH,GRAVITY,explosions,gangster,cops,TILE_SIZE)
    grenades.draw(window)

    #update explosions and draw them
    explosions.update()
    explosions.draw(window)
 
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
            GameRunning = False
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
                GameRunning = False
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