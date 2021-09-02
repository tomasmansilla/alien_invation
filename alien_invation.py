import sys
import pygame
from time import sleep
import pygame.mixer

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button, LevelButton
from sound import Sound
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manege game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Make the Play button.
        self.play_button = Button(self)
        # Make the Level Button.
        self.basic_button = LevelButton(self, 'images/easy.bmp', 1)
        self.medium_button = LevelButton(self, 'images/normal.bmp', 2)
        self.hard_button = LevelButton(self, 'images/hard.bmp', 3)

        # Music
        self.sound = Sound()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mousebuttomdown_events()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_mousebuttomdown_events(self):
        mouse_pos = pygame.mouse.get_pos()
        if not self.stats.game_active:
            self._check_level_selected(mouse_pos)
            self._check_play_button(mouse_pos)

    def _check_level_selected(self, mouse_pos):
        basic_button_clicked = self.basic_button.image_rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.image_rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.image_rect.collidepoint(mouse_pos)

        if basic_button_clicked:
            self.sound.button_sound()
            self.settings.level = 1
        elif medium_button_clicked:
            self.sound.button_sound()
            self.settings.level = 2
        elif hard_button_clicked:
            self.sound.button_sound()
            self.settings.level = 3

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        play_button_clicked = self.play_button.image_rect.collidepoint(mouse_pos)

        if play_button_clicked and self.settings.level:
            self.sound.button_sound()
            self._start_game()

    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.stats.game_active = True

        self.sb.prep_score()
        self.sb.prep_level()

        self._set_started_position()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _set_started_position(self):
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullet.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.sound.shot_sound()
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.sound.destroy_sound()
            self._new_level()

    def _new_level(self):
        """Destroy existing bullets and create new fleet."""
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Loop for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ship_left > 0:
            # Decrement ship_left, and update scoreboard.
            self.stats.ship_left -= 1

            self._set_started_position()

            self.sound.game_over_sound()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.settings.level = 0
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien.rect.height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Updates images to the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self._draw_buttons()

        pygame.display.flip()

    def _draw_buttons(self):
        """Draw the play and level buttons."""
        self.play_button.draw_button()
        if not self.settings.level:
            self.basic_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

    def _exit(self):
        """Manege the exit of the game."""
        if self.stats.high_score != self.stats.initial_high_score:
            self.stats.get_new_high_score(self.stats.high_score)
        sys.exit()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
