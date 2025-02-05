
import pygame


class Score:

    MULTIPLIER = 1

    def __init__(self, intial_score=500):
        self.score = intial_score
        self.tick_counter = 0


    def tick(self, screen: pygame.Surface, x_loc, y_loc, style='Smooch Sans', size=50, count=True):
        font = pygame.font.SysFont(style, size)
        # Update time
        self.tick_counter += 1
        # Lower the score every n ticks
        n = 75
        if self.tick_counter % n == 0 and count:
            self.score -= n
        # NNN
        self.score = max(self.score, 0)

        # Draw Score
        A = 0.7
        text_surface = font.render(str(self.score), False, (0 * A, 255 * A, 0 * A))
        screen.blit(text_surface, (x_loc, y_loc))
    
    def bullet_fired(self):
        self.score -= 50
    
    def asteroid_hit(self, size):
        self.score += size * 50 * self.MULTIPLIER
    
    def player_hit(self):
        self.score -= 700

    def win(self):
        self.score += 100000 * self.MULTIPLIER
