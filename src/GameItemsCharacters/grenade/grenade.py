import pygame
from GameItemsCharacters.explosion.explosion import Explosion

grenadeImg = pygame.image.load('images/gameItems/Grenade.png')


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.clock = 300
        self.vel_y = -11
        self.speed = 7
        self.image = grenadeImg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, world, GRAVITY,explosion_group,gangster,cop_group,TILE_SIZE,screen_scroll,grenade_sound):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom	

        # update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        grenade_sound.play()
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



