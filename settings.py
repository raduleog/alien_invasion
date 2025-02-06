class Settings:
    # A class to store the settings of the game

    def __init__(self):
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # Alien settings
        self.fleet_drop_speed = 10

        # Score Settings
        self.alien_points = 50

        # Increasing speed in game scale
        self.speedup_scale = 1.1

        # Increase number of points as game progresses
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        self.alien_speed = 1.0
        self.ship_speed = 3
        self.bullet_speed = 5.0

        self.fleet_direction = 1
    
    def increase_speed(self):
        # Increase speed settings
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale) 