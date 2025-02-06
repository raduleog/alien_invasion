import pygame

class Ship:
    # Initialize the Ship and it's coordinates
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings
        # Load the ship image and it's rect.
        self.image = pygame.image.load('resources/SpaceShip.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Store the x pos as a float for finer control
        self.x = float(self.rect.x)

        # Flag to see confirm if the ship is moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Update the ship's position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update the rect object from self.x which is a float
        self.rect.x = self.x
    def center_ship(self):
        # Center the ship after death
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)    

    def blitme(self):
        # Draw the ship at its current location
        self.screen.blit(self.image, self.rect)