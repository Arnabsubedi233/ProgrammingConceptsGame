import pygame
from characters.shooter import *

pygame.init()

WINDOW_WIDTH = int(800)
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.8)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game*')

GameRunning = True

shooter1 = ShooterCharacter(200, 200, 0.1)
shooter2 = ShooterCharacter(400, 200, 0.1)

while GameRunning:
    shooter1.draw(window)
    shooter2.draw(window)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
     

    pygame.display.update()

pygame.quit()