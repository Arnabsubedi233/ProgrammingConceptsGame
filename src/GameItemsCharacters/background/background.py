import pygame
from constants.gameConstants import *
from constants.colours import *
from constants.gameVariables import *

def draw_bg(window, background_scroll, sky_img, buildingOverlay_img, city1_img):
    window.fill(BGCOLOUR)
    width = sky_img.get_width()
    buildingOverlay_new_img = pygame.transform.scale(buildingOverlay_img, (buildingOverlay_img.get_width() * 2, buildingOverlay_img.get_height()*2))
    city1_new_img = pygame.transform.scale(city1_img, (city1_img.get_width() * 2.5, city1_img.get_height()*2.5))

    for x in range(6):
        window.blit(sky_img, ((x * width) - background_scroll * 0.5, 0))
        window.blit(buildingOverlay_img, ((x * width) - background_scroll * 0.6, WINDOW_HEIGHT - buildingOverlay_img.get_height() - 350))
        window.blit(buildingOverlay_new_img, ((x * width) - background_scroll * 0.7, WINDOW_HEIGHT - city1_img.get_height() - 300))
        window.blit(buildingOverlay_new_img, ((x * width) - background_scroll * 0.8, WINDOW_HEIGHT - city1_img.get_height()-200))
        window.blit(city1_new_img, ((x * width) - background_scroll * 0.9, WINDOW_HEIGHT - city1_img.get_height()-100))
