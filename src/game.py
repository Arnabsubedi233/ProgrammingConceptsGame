import pygame
from characters.Gangster.Gangster import *
 
pygame.init()
 
WINDOW_WIDTH = int(800)
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.8)
 
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game*')
 
#Frames per second
game_clock = pygame.time.Clock()
FPS = float(60)
 
#Player actions
left = bool(False)
right = bool(False)
 
#Game Variables
GRAVITY = float(0.75)
 
#colours
bgColour = tuple((100,200,130))
RedColour = tuple((255,0,0))
 
def draw_background():
    window.fill(bgColour)
 
 
GameRunning = True
 
Gangster = ShooterCharacter('gangster',200, 200, 1,2,50)
Police = ShooterCharacter('cop',400, 200, 1,2,50)
 
while GameRunning:
    game_clock.tick(FPS)
    draw_background()
 
    Gangster.animation()
    Gangster.draw(window)
    Police.draw(window)
 
    Gangster.move(left,right)
 
    if Gangster.alive:
        if Gangster.in_air:
            Gangster.update_action(2)  # 2: jump
        elif left or right:
            Gangster.update_action(1)  # 1: run
        else:
            Gangster.update_action(0)  # 0: idle
        Gangster.move(left, right)
 
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_w and Gangster.alive:
                Gangster.jump = True
            if event.key == pygame.K_ESCAPE:
                GameRunning = False
 
 
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
     
 
    pygame.display.update()
 
pygame.quit()