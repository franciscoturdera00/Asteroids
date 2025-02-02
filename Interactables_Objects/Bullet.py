
import math
import pygame

from Interactables_Objects.Utils import calculate_new_rotated_position


class Bullet:

    RADIUS = 2
    SPEED = 10
    NUMBER_OF_ACTIVE_SECONDS = 5

    def __init__(self, initial_position: pygame.Vector2, angle_of_trajectory, color="white", fps=60):
        self.position = initial_position
        self.color = color
        self.x_vel = math.cos(angle_of_trajectory) * self.SPEED
        self.y_vel = math.sin(angle_of_trajectory) * self.SPEED
        self.frames_left = fps * self.NUMBER_OF_ACTIVE_SECONDS
    
    def tick(self, screen: pygame.Surface):
        self.position.x = (self.position.x + self.x_vel) % screen.get_width()
        self.position.y = (self.position.y + self.y_vel) % screen.get_height()

        self.frames_left -= 1

        pygame.draw.circle(screen, self.color, self.position, self.RADIUS)