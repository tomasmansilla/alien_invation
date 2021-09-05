import pygame
from pygame.sprite import Sprite
from random import choice

from bullet import Bullet


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # load the image and set its rect attribute.
        alien_variations = ['red', 'green', 'purple']
        alien_random = choice(alien_variations)
        if alien_random == 'green':
            self.image = pygame.image.load("images/alien.bmp")
            self.rect = self.image.get_rect()
        elif alien_random == 'red':
            self.image = pygame.image.load("images/alien_red.bmp")
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.image.load("images/alien_purple.bmp")
            self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if an alien is at the edge of the screen."""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right or left."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
