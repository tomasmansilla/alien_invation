import pygame.mixer


class Sound:
    """A class to manege the sounds of the game."""

    def __init__(self):
        """Initialize the background music."""
        pygame.mixer.music.load('music/alien_2.mp3')
        pygame.mixer.music.play(-1)

    def shot_sound(self):
        self.sound_shot = pygame.mixer.Sound('music/shot.mp3')
        self.sound_shot.play()

    def game_over_sound(self):
        self.sound_gameover = pygame.mixer.Sound('music/gameover.mp3')
        self.sound_gameover.play()

    def button_sound(self):
        self.sound_button = pygame.mixer.Sound('music/button.mp3')
        self.sound_button.play()

    def destroy_sound(self):
        self.sound_destroy = pygame.mixer.Sound('music/destroy.mp3')
        self.sound_destroy.play()
