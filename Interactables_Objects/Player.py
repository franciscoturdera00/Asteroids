
from copy import deepcopy
import math
import random
from typing import List
import pygame

from Interactables_Objects.Bullet import Bullet
from Interactables_Objects.Utils import calculate_new_rotated_position

class Player:

    ACCELERATION = 0.1
    ROTATIONAL_SPEED = 7
    MAX_SPEED = 5
    BOUNDS_RADIUS = 18
    BOOST_SHOW_PERCENTAGE = 0.8
    MAX_BULLETS = 10
    INVINSIBLES_SECONDS = 3
    STARTING_LIVES = 3

    def __init__(self, position: pygame.Vector2, fps=60, scale=0.5, starting_angle=0, color="white"):
        self.position = position
        self.velocity = [0,0]
        self.scale = scale
        self.scaled_bound_radius = self.BOUNDS_RADIUS * scale
        self.color = color
        self.angle = starting_angle
        self.lives: List[Player] = list()

        self.player_shape = [(24 * scale, 0), (-24 * scale, -18 * scale), (-18 * scale, 0), (-24 * scale,  18 * scale)]
        self.boost_shape = [(-18 * scale, 0), (-21 * scale, 9 * scale), (-32 * scale, 0 * scale), (-21 * scale, -9 * scale)]

        self.boosting = False
        self.bullets: List[Bullet] = list()
        self.invincible = True
        self.invincible_frames = fps * self.INVINSIBLES_SECONDS
        self.fps = fps
        
        self.thrust_frame = 0
        self.bullet_sound = pygame.mixer.Sound("Sounds/fire.wav")
        self.move_sound = pygame.mixer.Sound("Sounds/thrust.wav")



    def tick(self, screen: pygame.Surface, show_bounds=False):
        # Update Bullets
        for bullet in self.bullets:
            if bullet.frames_left <= 0:
                self.bullets.remove(bullet)
            bullet.tick(screen)
        
        # Draw life
        for life in self.lives:
            life.tick()
        
        # Update the orientation of Player
        updated_player_shape = list()
        for point in self.player_shape:
            rotated_x, rotated_y = calculate_new_rotated_position(point, self._angle_in_radians())
            updated_player_shape.append((rotated_x, rotated_y))
        
        # Move the player with its momentum
        self.position.x = (self.position.x + self.velocity[0]) % screen.get_width()
        self.position.y = (self.position.y + self.velocity[1]) % screen.get_height()

        if self.invincible:
            pygame.draw.polygon(screen, "gold", [(self.position.x + x, self.position.y + y) for x, y in updated_player_shape], 2)
            self.invincible_frames -= 1
            if self.invincible_frames <= 0:
                self.invincible = False
        else:
            pygame.draw.polygon(screen, self.color, [(self.position.x + x, self.position.y + y) for x, y in updated_player_shape], 2)
        
        if self.boosting and random.random() < self.BOOST_SHOW_PERCENTAGE:
            updated_boost_shape = list()
            for point in self.boost_shape:
                rotated_boost_x, rotated_boost_y = calculate_new_rotated_position(point, self._angle_in_radians())
                updated_boost_shape.append((rotated_boost_x, rotated_boost_y))
        
            pygame.draw.polygon(screen, self.color, [(self.position.x + x, self.position.y + y) for x, y in updated_boost_shape], 2)

        if show_bounds:
            pygame.draw.circle(screen, "white", self.position, self.scaled_bound_radius, width=1)


    def receive_commands(self, shooting):
        if shooting and len(self.bullets) < self.MAX_BULLETS:
            bullet = Bullet(deepcopy(self.position), self._angle_in_radians(), fps=self.fps)
            self.bullets.append(bullet)
            self.bullet_sound.play()
            # pygame.mixer.Channel(1).play(self.bullet_sound)
        keys = pygame.key.get_pressed()
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

        # Sounds workaround for thrust and shooting happening together
        # thrust every 5 frames
        self.thrust_frame += 1
        self.thrust_frame %= 100000
        if self.thrust_frame % 5 == 0:
            self.move_sound.play()

    
    def _rotate_angle(self, direction): # direction in [-1, 1]
        self.angle = (self.angle + direction * self.ROTATIONAL_SPEED) % 360

    
    def restart_position(self, screen, invincible=False):
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.velocity = [0,0]
        if invincible:
            self.invincible = True
            self.invincible_frames = self.fps * self.INVINSIBLES_SECONDS


