import pygame.font


class Button:

    def __init__(self, ai_game, image_address):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image_address = image_address

        # Set the dimensions and properties of the button
        self.image = pygame.image.load(self.image_address)
        self.image_rect = self.image.get_rect()

        # Build the button's rect object and center it.
        self.image_rect.center = self.screen_rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.blit(self.image, self.image_rect)


class LevelButton(Button):
    """Initialize the buttom attributes."""

    def __init__(self, game, image_address, position):
        super().__init__(game, image_address)

        if position == 1:
            self.image_rect.y = self.screen_rect.centery + (self.image_rect.height * 1.5)
            self.image_rect.x = self.screen_rect.centerx - self.image_rect.width * 2
        elif position == 2:
            self.image_rect.y = self.screen_rect.centery + (self.image_rect.height * 1.5)
            self.image_rect.x = self.screen_rect.centerx - (self.image_rect.width // 2)
        else:
            self.image_rect.y = self.screen_rect.centery + (self.image_rect.height * 1.5)
            self.image_rect.x = self.screen_rect.centerx + self.image_rect.width


class SelectLevelImage:
    """Display un select level button."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Font settings for the button.
        self.text_color = (13, 45, 64)
        self.font = pygame.font.SysFont(None, 72)

        self._prep_image()

    def _prep_image(self):
        """Turn the text into a rendered image."""
        text = "Please, select a level!"
        self.text_image = self.font.render(text, True, self.text_color, self.settings.bg_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.screen_rect.center

    def draw_image(self):
        """Draw the button on the screen."""
        self.screen.blit(self.text_image, self.text_image_rect)
