import pygame
from pygame.sprite import Sprite



class Projectile(Sprite):
    # Class that implements the alien projectiles
    
    def __init__(self, ai_game, alien):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pygame.image.load('resources/projectile.png')
        self.rect = self.image.get_rect()

        self.rect.midtop = alien.rect.midbottom

        self.y = float(self.rect.y)

    
    def update(self):
        # Move projectile down the screen
        self.y += self.settings.projectile_speed
        self.rect.y = self.y

    def draw_projectile(self):
        # Draw the projectile on the screen
        self.screen.blit(self.image, self.rect)
