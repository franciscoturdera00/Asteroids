

import pygame


class Lives:

    def __init__(self, num=3, scale=.4):
        self.number = num
        A = 0.5
        self.color = [255 * A, 255 * A, 255 * A]
        self.life_shape = [(0, -24 * scale), (18 * scale, 24 * scale), (0, 18 * scale), (-18 * scale, 24 * scale)]
    
    # Returns False if player fully dies
    # TODO: Implement this in main
    def die(self):
        self.number -= 1
        if self.number <= 0:
            return True
        return False
    
    def tick(self, screen: pygame.Surface):
        # Draw lives
        for i in range(self.number):
            pygame.draw.polygon(screen, self.color, [(screen.get_width() / 20 + x + (i * 25), screen.get_height() / 10 + y) for x, y in self.life_shape], 2)