class Settings:
    """A class to store all settings for alien invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = None
        self.screen_height = None
        self.bg_color = (224, 224, 224)

        # Ship settings.
        self.ship_limit = 3

        # Bullets settings.
        self.bullet_width = 1000
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10
        self.number_aliens_x = None
        self.number_aliens_y = None
        self.alien_fit_total = None

        # How quickly the game speeds up.
        self.speedup_scale = 1.1

        # How quickly the alien point values increase.
        self.score_scale = 1.5

        # Levels
        self.level = 0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""

        self.ship_speed = 1.3 * self.level
        self.bullet_speed = 3.0 * self.level
        self.alien_speed = 1.3 * self.level

        self.aliens_screen = self.number_aliens_x
        self.alien_random_limit = 10

        # fleet_direction of 1 represent right; -1 represent left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
