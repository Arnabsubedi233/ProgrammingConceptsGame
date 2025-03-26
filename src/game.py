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
from GameItemsCharacters.screenFade.screenfade import *
from GameItemsCharacters.background.background import *
from constants.gameConstants import *
from constants.colours import *
from constants.gameVariables import *

#pygame initialisation
pygame.init()

#screen configurations
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Law And Disorder')
 
#Clock Settings
clock = pygame.time.Clock()

#Game Variables with strict type casting
game_start = bool(False)
level = int(1)
window_scroll = int(0)
background_scroll = int(0)
game_running = bool(True)
intro = bool(False)

#sounds
jump_sound = pygame.mixer.Sound('sounds/jump.mp3')
shooting_sound = pygame.mixer.Sound('sounds/shot.wav')
grenade_sound = pygame.mixer.Sound('sounds/grenade.wav')
death_sound = pygame.mixer.Sound('sounds/death.mp3')

#background configurations
start = pygame.image.load('images/ui/Start.png').convert_alpha()
restart = pygame.image.load('images/ui/Restart.png').convert_alpha()
exit = pygame.image.load('images/ui/Exit.png').convert_alpha()
gameover = pygame.image.load('images/ui/gameover.png').convert_alpha()

city1_img = pygame.image.load('images/background/city1.png').convert_alpha()
buildingOverlay_img = pygame.image.load('images/background/buildingOverlay.png').convert_alpha()
sky_img = pygame.image.load('images/background/sky.png').convert_alpha()


#function to reset level
def level_reset():
    """
        Resets the game level by clearing all game objects and creating an empty tile list.
        This function performs the following actions:
        - Empties the lists of cops, bullets, grenades, explosions, item boxes, decorations, waters, and exits.
        - Creates and returns a new empty tile list with dimensions ROWS x COLUMNS, where each tile is initialized to -1.
        Returns:
            list: A 2D list representing the empty tile map with dimensions ROWS x COLUMNS.
    """
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

#function to read csv file / level data
def csv_reader():
    """
    Reads a CSV file containing level data and populates the world_data array.

    The CSV file is expected to be located in the 'levels' directory and named
    in the format 'level{level}_data.csv', where {level} is a variable representing
    the current level number.

    The function reads the CSV file line by line, and for each cell in the CSV,
    it converts the value to an integer and assigns it to the corresponding position
    in the world_data array.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        ValueError: If the CSV file contains non-integer values.

    Note:
        The variables 'level' and 'world_data' should be defined in the global scope
        or passed to the function for it to work correctly.
    """
    with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

#drawing text on screen
font = pygame.font.SysFont('Calibri', 25)
font2 = pygame.font.Font('fonts/font2.otf', 280)
font3 = pygame.font.Font('fonts/font2.otf', 120)


def text(text, font, text_col, x, y):
    """
    Renders and displays text on the game window.

    Args:
        text (str): The text to be rendered.
        font (pygame.font.Font): The font object used to render the text.
        text_col (tuple): The color of the text in RGB format.
        x (int): The x-coordinate where the text will be displayed.
        y (int): The y-coordinate where the text will be displayed.
    """
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))
     
#Player actions
left = bool(False)
right = bool(False)
shooting = bool(False)
grenade = bool(False)
throw_grenade = bool(False)

#create buttons
start_button = Button(WINDOW_WIDTH // 2- 200 , WINDOW_HEIGHT // 2  , start, 2)
exit_button = Button(WINDOW_WIDTH // 2-200 , WINDOW_HEIGHT // 2 + 125, exit, 2)
restart_button = Button(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 , restart, 2)

#create screen fades
intro_fade = ScreenFade(1, BLACK, 9)
death_fade = ScreenFade(2, RED, 9)
outro_fade = ScreenFade(2, WHITE, 9)

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
csv_reader()
    
world = World()
gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)


#Game Loop
while game_running:
    clock.tick(FPS)

    #Game Start Screen
    if game_start == False:
         window.fill(BLACK)
         text('LAW AND DISORDER', font3, WHITE, WINDOW_WIDTH // 2 - 390, WINDOW_HEIGHT // 2 - 190)
         if start_button.draw(window):
                game_start = True
                intro = True
         if exit_button.draw(window):
                game_running = False
    else:
        #draw background
        draw_bg(window, background_scroll, sky_img, buildingOverlay_img, city1_img)
        world.draw(window,window_scroll)
        health_bar.draw(window, gangster.health)

        #draw ammo text
        text('AMMO: ', font, WHITE, 10, 35)
        text(f'{gangster.ammo}',font,WHITE,(90), 35)
        transformedBullet = pygame.transform.scale(bulletImg, (10, 10))
        window.blit(transformedBullet, (140, 40))

        #draw grenade text
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

        #update item boxes and draw them
        itemBoxes.update(gangster,window_scroll)
        itemBoxes.draw(window)

        #update decorations and draw them
        decorations.update(window_scroll)
        decorations.draw(window)

        #update waters and draw them
        waters.update(window_scroll)
        waters.draw(window)

        #update exits and draw them
        exits.update(window_scroll)
        exits.draw(window)

        #check if intro is true and then fade the screen
        if intro == True:
             if intro_fade.fade(window):
                intro = False
                intro_fade.fade_counter = 0

        #for each cop in the group, update their attributes and then draw them
        for cop in cops:
            cop.enemy_auto(gangster,bullets,world,window_scroll,background_scroll,waters,exits,shooting_sound)
            cop.update_character()
            cop.draw(window)
    

        
        #check if the gangster is alive then carry out functionalities 
        if gangster.alive:
            #shoot bullets
            if shooting:
                gangster.shoot(bullets,shooting_sound)
            #throw grenades
            elif grenade and throw_grenade == False and gangster.grenades > 0:
                grenade = Grenade(gangster.rect.centerx + (0.5 * gangster.rect.size[0] * gangster.direction),\
                                gangster.rect.top, gangster.direction)
                grenades.add(grenade)
                gangster.grenades -= 1
                throw_grenade = True
            #jump
            if gangster.in_air:
                gangster.update_action(2)  # 2: jump
            #movement left or right
            elif left or right:
                gangster.update_action(1)
            #idle  # 1: run
            else:
                gangster.update_action(0)  # 0: idle
            window_scroll,level_end = gangster.move(left, right,world,background_scroll,waters,exits)
            background_scroll -= window_scroll
            #check if level is complete then move to next level
            if level_end:
                 start_intro = True
                 level += 1
                 print(level)
                 background_scroll = 0
                 world_data = level_reset()
                 if level <= MAXIMUM_LEVELS:
                    csv_reader()
                    world = World()
                    gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)
            #if level is at final level then display win screen
            if level == 4:
                window_scroll = 0
                if outro_fade.fade(window):
                    text('YOU WIN!', font2, BLACK, WINDOW_WIDTH // 2- 380 , WINDOW_HEIGHT // 2 - 250 )
                if restart_button.draw(window):
                    outro_fade.fade_counter = 0
                    intro = True
                    background_scroll = 0
                    level = 1
                    world_data = level_reset()
                    csv_reader()
                    world = World()
                    gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)
                if exit_button.draw(window):
                     game_running = False
        #if gangster is dead then display game over screen
        else:
             window_scroll = 0
             if death_fade.fade(window):
                death_sound.play()
                window.blit(gameover, (WINDOW_WIDTH // 2- 200 , WINDOW_HEIGHT // 2 - 200 ))
                if restart_button.draw(window):
                    death_fade.fade_counter = 0
                    intro = True
                    background_scroll = 0
                    world_data = level_reset()
                    csv_reader()
                    world = World()
                    gangster, health_bar = world.process_data(world_data,waters,decorations,itemBoxes,exits,cops)
                if exit_button.draw(window):
                    game_running = False
                

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
                jump_sound.play()
            if event.key == pygame.K_SPACE:
                shooting = True
            if event.key == pygame.K_ESCAPE:
                game_running = False
            if event.key == pygame.K_q:
                grenade = True
                grenade_sound.play()
 
 
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