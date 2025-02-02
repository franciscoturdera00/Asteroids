from enum import IntEnum
import math
import random
import pygame


class SizeType(IntEnum):
    LARGE=50
    MEDIUM=30
    SMALL=10

ASTEROID_ORDERED_SIZES = [SizeType.LARGE, SizeType.MEDIUM, SizeType.SMALL, None]
    
class Asteroid:

    SPEED_SCALAR = 2
    BOUNDARY_SCALAR = 5 / 6
    MAX_SPEED = 1.5
    MIN_SPEED = 0.3

    def __init__(self, screen: pygame.Surface, sizeType: SizeType, initial_position: pygame.Vector2 = None, color="white"):
        self.size = sizeType.value
        self.position = initial_position
        if not initial_position:
            self.position = pygame.Vector2(random.randrange(0, screen.get_width()), random.randrange(0, screen.get_height()))
        sign = [-1, 1]
        self.x_vel = ((random.random() * (self.MAX_SPEED - self.MIN_SPEED)) + self.MIN_SPEED) * random.choice(sign)
        self.y_vel = ((random.random() * (self.MAX_SPEED - self.MIN_SPEED)) + self.MIN_SPEED) * random.choice(sign)
        self.color = color
        self.boundary_radius = self.size * self.BOUNDARY_SCALAR

        self.explode_sound = pygame.mixer.Sound("Sounds/bangLarge.wav")

        self._create_vertices()
    

    
    def tick(self, screen: pygame.Surface, show_bounds=False):
        self.position.x = (self.position.x + self.x_vel * self.SPEED_SCALAR) % screen.get_width()
        self.position.y = (self.position.y + self.y_vel * self.SPEED_SCALAR) % screen.get_height()
        
        # Draw asteroid
        for v in range(len(self.vertices)):
            next_v = self.vertices[(v + 1) % len(self.vertices)]
            this_v = self.vertices[v]
            pygame.draw.line(screen, "white", 
                             (self.position.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                            self.position.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                             (self.position.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                              self.position.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))
        
        if show_bounds:
            pygame.draw.circle(screen, self.color, self.position, self.size * self.BOUNDARY_SCALAR, 1)
            
    def _create_vertices(self):
        # Make random asteroid sprite
        uniform_walk_min = 18
        angle_rotated_so_far = random.uniform(uniform_walk_min, uniform_walk_min * 2)
        dist = random.uniform(self.size / 2, self.size)
        self.vertices = []
        while angle_rotated_so_far < 360:
            self.vertices.append([dist, angle_rotated_so_far])
            dist = random.uniform(self.size / 2, self.size)
            angle_rotated_so_far += random.uniform(uniform_walk_min, uniform_walk_min * 2)