
import pygame


class Score:

    MULTIPLIER = 1

    def __init__(self, screen: pygame.Surface, font, intial_score=500):
        self.screen = screen
        self.score = intial_score
        self.tick_counter = 0
        self.font = font

    def tick(self, x_loc, y_loc, size=50):
        self.update()
        self.render(x_loc, y_loc, size)

    def _clamp_score(self):
        self.score = max(self.score, 0)

    def update(self):
        self.tick_counter += 1
        n = 75
        if self.tick_counter % n == 0:
            self.score -= n
        self._clamp_score()

    def render(self, x_loc, y_loc, size=50):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(str(self.score), False, (0, 178, 0))
        self.screen.blit(text_surface, (x_loc, y_loc))

    def bullet_fired(self):
        self.score -= 50
        self._clamp_score()

    def asteroid_hit(self, size):
        self.score += size * 50 * self.MULTIPLIER

    def alien_hit(self):
        self.score += 2000 * self.MULTIPLIER

    def player_hit(self):
        self.score -= 700
        self._clamp_score()

    def win(self, lives_left):
        self.score += 100000 * lives_left * self.MULTIPLIER
