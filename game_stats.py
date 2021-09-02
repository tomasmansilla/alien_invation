import json


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize the game."""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = None
        self.initial_high_score = None
        self.check_high_score_file()

    def reset_stats(self):
        """Initialize the statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def check_high_score_file(self):
        """Check if there's a high score stored."""
        high_score_file = self.get_stored_high_score()
        if high_score_file:
            self.high_score = int(high_score_file)
        else:
            self.high_score = 0

        self.initial_high_score = self.high_score

    def get_stored_high_score(self):
        """Get stored high score if available."""
        filename = 'high_score.json'
        try:
            with open(filename) as f:
                high_score = json.load(f)
        except FileNotFoundError:
            return None
        else:
            return high_score

    def get_new_high_score(self, high_score):
        """Store a new high score."""
        filename = 'high_score.json'
        with open(filename, 'w') as f:
            json.dump(high_score, f)
