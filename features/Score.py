
import pygame


class Score:

    MULTIPLIER = 1

    def __init__(self, screen: pygame.Surface, intial_score=500):
        self.score = intial_score
        self.tick_counter = 0

        self.font = pygame.font.SysFont('Smooch Sans', 50)
        self.x_loc = screen.get_width() / 25
        self.y_loc = screen.get_height() / 20

    def tick(self, screen: pygame.Surface):
        # Update time
        self.tick_counter += 1
        # Lower the score every n ticks
        n = 50
        if self.tick_counter % n == 0:
            self.score -= n * self.MULTIPLIER
        # NNN
        self.score = max(self.score, 0)

        # Draw Score
        A = 0.7
        text_surface = self.font.render(str(self.score), False, (0 * A, 255 * A, 0 * A))
        screen.blit(text_surface, (self.x_loc, self.y_loc))
    
    def bullet_fired(self):
        self.score -= 50 * self.MULTIPLIER
    
    def asteroid_hit(self, size):
        self.score += size * 125 * self.MULTIPLIER
    
    def player_hit(self):
        self.score -= 700 * self.MULTIPLIER
