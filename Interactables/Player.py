
import math
import random
import pygame


class Player:

    ACCELERATION = 0.1
    ROTATIONAL_SPEED = 10
    MAX_SPEED = 5
    BOUNDS_RADIUS = 18
    BOOST_SHOW_PERCENTAGE = 0.8

    def __init__(self, position: pygame.Vector2, scale=0.5, starting_angle=0, color="white", show_bounds=False):
        self.position = position
        self.velocity = [0,0]
        self.scale = scale
        self.bounds = self.BOUNDS_RADIUS * scale
        self.color = color
        self.angle = starting_angle
        self.player_shape = [(24 * scale, 0), (-24 * scale, -18 * scale), (-18 * scale, 0), (-24 * scale,  18 * scale)]
        # self.boost_shape = [(-18 * self.scale, -5 * self.scale), (-18 * self.scale, 5 * self.scale), (-24 * self.scale, 0)]
        self.boost_shape = [(-18 * scale, 0), (-21 * scale, 9 * scale), (-32 * scale, 0 * scale), (-21 * scale, -9 * scale)]
        self.boosting = False

        # For debugging
        self.show_bounds = show_bounds
    

    def tick(self, screen: pygame.Surface):
        # Update the orientation of Player
        updated_player_shape = list()
        for point in self.player_shape:
            rotated_x, rotated_y = self._calculate_new_rotated_position(point, self._angle_in_radians())
            updated_player_shape.append((rotated_x, rotated_y))
        

        # Move the player given its momentum
        self.position.x = (self.position.x + self.velocity[0]) % screen.get_width()
        self.position.y = (self.position.y + self.velocity[1]) % screen.get_height()

        pygame.draw.polygon(screen, self.color, [(self.position.x + x, self.position.y + y) for x, y in updated_player_shape], 2)
        
        if self.boosting and random.random() < self.BOOST_SHOW_PERCENTAGE:
            updated_boost_shape = list()
            for point in self.boost_shape:
                rotated_boost_x, rotated_boost_y = self._calculate_new_rotated_position(point, self._angle_in_radians())
                updated_boost_shape.append((rotated_boost_x, rotated_boost_y))
        
            pygame.draw.polygon(screen, self.color, [(self.position.x + x, self.position.y + y) for x, y in updated_boost_shape], 2)

        if self.show_bounds:
            pygame.draw.circle(screen, "white", self.position, self.bounds, width=1)

    def receive_commands(self, keys):
        if keys[pygame.K_a]:
            self._rotate_angle(-1)
        if keys[pygame.K_d]:
            self._rotate_angle(1)
        if keys[pygame.K_w]:
            self._accelerate()
            self.boosting = True
        if not keys[pygame.K_w]:
            self.boosting = False

    def _angle_in_radians(self):
        return math.pi * self.angle / 180
    
    def _accelerate(self, acceleration=ACCELERATION):
        dir_x = -1 if self.velocity[0] < 0 else 1
        dir_y = -1 if self.velocity[1] < 0 else 1
        # Updates the velocity of the Player object when a player thrusts
        self.velocity[0] = self.velocity[0] + math.cos(self._angle_in_radians()) * acceleration if abs(self.velocity[0]) <= self.MAX_SPEED else self.MAX_SPEED * dir_x
        self.velocity[1] = self.velocity[1] + math.sin(self._angle_in_radians()) * acceleration if abs(self.velocity[1]) <= self.MAX_SPEED else self.MAX_SPEED * dir_y

    
    def _rotate_angle(self, direction): # direction in [-1, 1]
        self.angle = (self.angle + direction * self.ROTATIONAL_SPEED) % 360


    def _calculate_new_rotated_position(self, point, angle):
        x, y = point
        new_x = (x * math.cos(angle)) - (y * math.sin(angle))
        new_y = (x * math.sin(angle)) + (y * math.cos(angle))
        return new_x, new_y

