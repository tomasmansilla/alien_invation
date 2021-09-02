import pygame.font


class Button:

    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.image = pygame.image.load('images/play.bmp')
        self.image_rect = self.image.get_rect()

        # Build the button's rect object and center it.
        self.image_rect.center = self.screen_rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.blit(self.image, self.image_rect)


class LevelButton:
    """Initialize the buttom attributes."""

    def __init__(self, game, image, position):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(image)
        self.image_rect = self.image.get_rect()

        if position == 1:
            self.image_rect.y = self.screen_rect.centery + (self.image_rect.height * 1.5)
            self.image_rect.x = self.screen_rect.centerx - self.image_rect.width * 2
        elif position == 2:
            self.image_rect.y = self.screen_rect.centery + (self.image_rect.height * 1.5)
            self.image_rect.x = self.screen_rect.centerx - (self.image_rect.width // 2)
        else:
            self.image_rect.y = self.screen_rect.centery + (self.image_rect.height * 1.5)
            self.image_rect.x = self.screen_rect.centerx + self.image_rect.width

    def draw_button(self):
        """Draw the button"""
        self.screen.blit(self.image, self.image_rect)
