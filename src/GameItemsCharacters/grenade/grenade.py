import pygame
from GameItemsCharacters.explosion.explosion import Explosion

grenadeImg = pygame.image.load('images/gameItems/Grenade.png')

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.clock = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenadeImg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, SCREEN_WIDTH, GRAVITY,explosion_group,gangster,cop_group,TILE_SIZE):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        self.clock -= 1
        if self.clock <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # do damage to anyone that is nearby
            if abs(self.rect.centerx - gangster.rect.centerx) < TILE_SIZE * 2 and \
            abs(self.rect.centery - gangster.rect.centery) < TILE_SIZE * 2:
                gangster.health -= 50

            for enemy in cop_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50



