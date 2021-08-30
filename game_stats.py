class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize the game."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize the statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
