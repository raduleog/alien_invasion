import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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

        #Create an instance of the Game Stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start the Alien Invasion game in an active state
        self.game_active = False

        #Make Play button
        self.play_button = Button(self, "Play")
    
    def run_game(self):
        # starts the main loop of the game
        while True:
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._check_events()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.settings.initialize_dynamic_settings()
            # Remove remaining ships and bullets.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

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
        self.aliens.draw(self.screen)
        self.sb.show_score()
        
        #Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()
    
    # Function that updates the bullets position on screen
    def _update_bullets(self):    
        self.bullets.update()

        # Get rid of bullets outside the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        # Check if the bullets hit aliens
        self._check_bullet_alien_collision()
         

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Clean bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()
            
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Check if alien hits rocket
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Check if aliens reached the bottom
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        # Respond to the ship being hit
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        
    
    def _check_aliens_bottom(self):
        # Check if the aliens have reached the bottom of the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat it like the ship has been hit
                self._ship_hit()
                break

    def _create_fleet(self):
        # Create a fleet of aliens
        # Make an alien then add more until there s no room left
        # Spacing will be half of an alien
        alien = Alien(self)
        self.aliens.add(alien)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        # Create an alien and place it in the row
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self):
        # check if the aliens reach the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        # Change the fleet direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()