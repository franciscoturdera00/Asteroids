

import pygame


class Lives:

    def __init__(self, id, screen: pygame.Surface, num=3, scale=.4):
        self.id = id
        self.number = num
        self.screen = screen
        A = 0.5
        self.color = [255 * A, 255 * A, 255 * A]
        self.life_shape = [(0, -24 * scale), (18 * scale, 24 * scale), (0, 18 * scale), (-18 * scale, 24 * scale)]
    
    # Returns False if player fully dies
    def die(self):
        self.number -= 1
        if self.number <= 0:
            return True
        return False
    
    def render(self):
        # Draw lives
        for i in range(self.number):
            pygame.draw.polygon(self.screen, self.color, [(self.screen.get_width() / 25 + x + (i * 25), (self.screen.get_height() / 8) + y + (self.id * 75)) for x, y in self.life_shape], 2)