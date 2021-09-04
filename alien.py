import pygame
from pygame.sprite import Sprite
from random import randint


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the image and set its rect attribute.
        random_number = randint(1, 3)
        if random_number == 1:
            self.image = pygame.image.load("images/alien.bmp")
            self.rect = self.image.get_rect()
        elif random_number == 2:
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
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right or left."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
