from enum import IntEnum
import math
import random
import pygame


class SizeType(IntEnum):
    SMALL=10
    MEDIUM=30
    LARGE=50

class Asteroid:

    SPEED = 1

    def __init__(self, starting_position: pygame.Vector2, sizeType: SizeType, x_vel, y_vel):
        self.size = sizeType.value
        self.position = starting_position
        self.x_vel = x_vel
        self.y_vel = y_vel

        self._create_vertices()

    
    def tick(self, screen: pygame.Surface):
        self.position.x = (self.position.x + self.x_vel * self.SPEED) % screen.get_width()
        self.position.y = (self.position.y + self.y_vel * self.SPEED) % screen.get_height()

        # pygame.draw.rect(screen, "white", pygame.Rect(self.position.x, self.position.y, self.size, self.size), width=1)
        
        # Draw asteroid
        for v in range(len(self.vertices)):
            if v == len(self.vertices) - 1:
                next_v = self.vertices[0]
            else:
                next_v = self.vertices[v + 1]
            this_v = self.vertices[v]
            pygame.draw.line(screen, "white", 
                             (self.position.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                            self.position.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                             (self.position.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                              self.position.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))
            
    def _create_vertices(self):
        # Make random asteroid sprites
        full_circle = random.uniform(32, 36)
        dist = random.uniform(self.size * 3 / 4, self.size)
        self.vertices = []
        while full_circle < 360:
            self.vertices.append([dist, full_circle])
            dist = random.uniform(self.size * 3 / 4, self.size)
            full_circle += random.uniform(32, 36)