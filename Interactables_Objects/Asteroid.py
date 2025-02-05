from enum import IntEnum
import math
import random
import pygame


class SizeType(IntEnum):
    LARGE=50
    MEDIUM=30
    SMALL=10

ASTEROID_ORDERED_SIZES = [SizeType.LARGE, SizeType.MEDIUM, SizeType.SMALL, None]
SCALE_BACKGROUND_AESTHETIC_ASTEROIDS = 0.3
GRAVITATIONAL_CONSTANT = 0.0000001
    
class Asteroid:

    SPEED_SCALAR = 2
    BOUNDARY_SCALAR = 5 / 6
    MAX_SPEED = 1
    MIN_SPEED = 0.3
    

    def __init__(self, screen: pygame.Surface, sizeType: SizeType, position = None, is_in_game_spawn=False, background=False, debugging_mode=False):
        self.screen = screen
        self.size = sizeType.value
        sign = [-1, 1]

        if position:
            self.position = position
            self.x_vel = ((random.random() * (self.MAX_SPEED - self.MIN_SPEED)) + self.MIN_SPEED) * random.choice(sign)
        
        if not position:
            if not is_in_game_spawn:
                self.position = pygame.Vector2(random.randrange(0, screen.get_width()), random.randrange(0, screen.get_height()))
                self.x_vel = self._generate_random_speed() * random.choice(sign)
            else:
                comes_from_left = random.choice([True,False])
                if comes_from_left:
                    self.position = pygame.Vector2(0, random.randrange(0, screen.get_height()))
                    self.x_vel = self._generate_random_speed()
                else:
                    self.position = pygame.Vector2(screen.get_width(), random.randrange(0, screen.get_height()))
                    self.x_vel = 0 - self._generate_random_speed()
            
        self.y_vel = self._generate_random_speed() * random.choice(sign)

        rgb = [255, 255, 255]
        R,G,B = rgb
        if background:
            A = random.random() * .2  + .1
            R,G,B = [A * v for v in rgb]
            self.size *= SCALE_BACKGROUND_AESTHETIC_ASTEROIDS
            self.x_vel *= 0.1
            self.y_vel *= 0.1

        self.boundary_radius = self.size * self.BOUNDARY_SCALAR
        self.color = (R, G, B)

        self._create_vertices()

        self.debugging_mode = debugging_mode
    
    def _generate_random_speed(self):
        return ((random.random() * (self.MAX_SPEED - self.MIN_SPEED)) + self.MIN_SPEED)
    
    def tick(self, player_pos: pygame.Vector2 = None):

        # Gravitational pull of player on asteroid
        if player_pos:
            distance = player_pos.distance_to(self.position)
            # The gravitational effect gets stronger the closer the asteroid is to the player
            gravitational_effect = GRAVITATIONAL_CONSTANT * (1500 - distance) * self.size / 10
            x_direction = -1 if player_pos.x < self.position.x else 1
            self.x_vel += gravitational_effect * x_direction
            y_direction = -1 if player_pos.y < self.position.y else 1
            self.y_vel += gravitational_effect * y_direction
        
        # Update position of asteroid
        self.position.x = (self.position.x + self.x_vel * self.SPEED_SCALAR) % self.screen.get_width()
        self.position.y = (self.position.y + self.y_vel * self.SPEED_SCALAR) % self.screen.get_height()
        
        # Draw asteroid
        pygame.draw.circle(self.screen, "black", self.position, self.size * self.BOUNDARY_SCALAR)
        for v in range(len(self.vertices)):
            next_v = self.vertices[(v + 1) % len(self.vertices)]
            this_v = self.vertices[v]
            pygame.draw.line(self.screen, self.color, 
                             (self.position.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                            self.position.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                             (self.position.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                              self.position.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))
            
        if self.debugging_mode:
            pygame.draw.circle(self.screen, self.color, self.position, self.size * self.BOUNDARY_SCALAR, 1)
            
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