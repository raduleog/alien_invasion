import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    # Overall class to manage game assets and behavior.

    def __init__(self):
        #Initializes the game and creates the game resources
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    
    def run_game(self):
        # starts the main loop of the game
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
    
    # Function to handle key presses events
    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Move ship to the right
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            # Move ship to the right
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            # Fire a bullet
            self._fire_bullet()
        if event.key == pygame.K_ESCAPE:
            # Move ship to the right
            sys.exit()
    
    # Function to check key releases events
    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Move ship to the right
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # Move ship to the right
            self.ship.moving_left = False

    # Function that handles behavior when the bullet is fired
    def _fire_bullet(self):
        # Create a new bullet and add it to the bullets group
        if self.settings.bullets_allowed >= len(self.bullets):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Update the images on the screen and flip to the new screen
    def _update_screen(self):
        # Redraw the screed during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()
    
    # Function that updates the bullets position on screen
    def _update_bullets(self):    
        self.bullets.update()

        # Get rid of bullets outside the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
 
if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()