class GameStats:
    # Track game stats for Alien Invasion

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        # High score deosnt reset
        f = open("highscore.txt", "r")
        self.high_score = int(f.read())
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        