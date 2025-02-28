import pygame
from characters.Gangster import *

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

#colours
def draw_background():
    window.fill((100,200,130))


GameRunning = True

Gangster = ShooterCharacter('player',200, 200, 0.1,5)
Police = ShooterCharacter('enemy',400, 200, 0.1,5)

while GameRunning:
    game_clock.tick(FPS)
    draw_background()

    Gangster.draw(window)
    Police.draw(window)

    Gangster.move(left,right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_ESCAPE:
                GameRunning = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
     

    pygame.display.update()

pygame.quit()