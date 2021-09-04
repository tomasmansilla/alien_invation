import pygame.mixer


class Sound:
    """A class to manege the sounds of the game."""

    def __init__(self):
        """Initialize the background music."""
        pygame.mixer.music.load('sounds/alien_2.mp3')
        pygame.mixer.music.play(-1)
        self.sound_shot = pygame.mixer.Sound('sounds/shot.mp3')
        self.sound_game_over = pygame.mixer.Sound('sounds/gameover.mp3')
        self.sound_button = pygame.mixer.Sound('sounds/button.mp3')
        self.sound_destroy = pygame.mixer.Sound('sounds/destroy.mp3')

    def shot_sound(self):
        self.sound_shot.play()

    def game_over_sound(self):
        self.sound_game_over.play()

    def button_sound(self):
        self.sound_button.play()

    def destroy_sound(self):
        self.sound_destroy.play()
