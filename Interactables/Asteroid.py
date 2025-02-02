import math
import random
import pygame


class Asteroid:

    SPEED = 1

    def __init__(self, starting_position: pygame.Vector2, size, x_vel, y_vel):
        self.size = size
        self.position = starting_position
        self.x_vel = x_vel
        self.y_vel = y_vel

    
    def tick(self, screen):
        self.position.x = (self.position.x + self.x_vel * self.SPEED) % screen.get_width()
        self.position.y = (self.position.y + self.y_vel * self.SPEED) % screen.get_height()

    
    def draw(self, screen):
        self.tick(screen)
        pygame.draw.rect(screen, "white", pygame.Rect(self.position.x, self.position.y, self.size, self.size), width=1)

    
    # def _create_shape(self, num_sides, size):
    #     # Create a list of points an R distance from the center
    #     points = list()
    #     for _ in range(num_sides):
    #         angle = random.random() * math.pi * 2
    #         scale = size * random.random() * 0.4 + 0.6 * size
           
    #         continue