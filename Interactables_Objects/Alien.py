

import math
import random
import pygame


class Alien:

    HITBOX_SCALE = 5 / 6


    def __init__(self, screen: pygame.Surface, fps, position: pygame.Vector2 = None, color = "white", size = 20, debugging_mode=False):
        self.screen = screen
        self.position = position
        if position is None:
            # Spawn at either side of the screen
            self.position = pygame.Vector2(random.randrange(-5, 5) % screen.get_width(), random.randrange(0, screen.get_height()))
        self.fps = fps
        self.size = size
        self.color = color
        self.move=True
        self.freeze_time_seconds = 3
        self.freeze_timer = self.fps * self.freeze_time_seconds
        self.hitbox_radius = self.size * self.HITBOX_SCALE
        self.goal = self._generate_random_point_within_square(self.position, 150)
        self.velocity = self._generate_velocity_to_goal(1)

        self.debugging_mode=debugging_mode

    def update(self, player_positions):
        player_position = random.choice(player_positions)
        if self.move:
            self._move_towards_goal()
            if self.position.distance_to(self.goal) <= 3:
                self.goal = self._generate_random_point_within_square(player_position, 50)
                self.velocity = self._generate_velocity_to_goal(self._random_time_frame())
                self.move = False
        else:
            if self.freeze_timer > 0:
                self._chill()
                self.freeze_timer -= 1
            else:
                self.move = True
                self.freeze_timer = self.fps * self.freeze_time_seconds
                self.goal = self._generate_random_point_within_square(player_position, 50)
                self.velocity = self._generate_velocity_to_goal(self._random_time_frame())

        # print(self.goal.x, self.goal.y, self.position.x, self.position.y)

    def render(self):
        self._render_shape()

        if self.debugging_mode:
            self._render_hit_box()

    

    def _render_shape(self):
        pygame.draw.ellipse(self.screen, "black", pygame.Rect(self.position.x - self.size, self.position.y - self.size / 2, self.size * 2, self.size), 0)
        pygame.draw.line(self.screen, "green", pygame.Vector2(self.position.x, self.position.y - self.size / 2), pygame.Vector2(self.position.x, self.position.y - self.size + 5), 5)
        pygame.draw.ellipse(self.screen, self.color, pygame.Rect(self.position.x - self.size, self.position.y - self.size / 2, self.size * 2, self.size), 1)
        pygame.draw.ellipse(self.screen, self.color, pygame.Rect(self.position.x - self.size, self.position.y - self.size / 8, self.size * 2, self.size / 4), 0)
        pygame.draw.arc(self.screen, self.color, pygame.Rect(self.position.x - self.size / 2, self.position.y - self.size, self.size, self.size), 0, math.pi, 1)
        # pygame.draw.circle(self.screen, self.color, self.position, self.size, 1)
    
    def _render_hit_box(self):
        pygame.draw.circle(self.screen, "white", self.position, self.hitbox_radius, 1)
    
    def _generate_random_point_within_square(self, square_middle: pygame.Vector2, square_length):
        x = random.randint(max(0, int(square_middle.x) - math.floor(square_length / 2)), min(int(square_middle.x) + math.ceil(square_length / 2), self.screen.get_width()))
        y = random.randint(max(0, int(square_middle.y) - math.floor(square_length / 2)), min(int(square_middle.y) + math.ceil(square_length / 2), self.screen.get_height()))
        return pygame.Vector2(x, y)
    
    def _generate_velocity_to_goal(self, time_in_seconds): # Velocity = Pixels moved per frame
        total_frames = self.fps * time_in_seconds
        velocity_x = (self.goal.x - self.position.x) / total_frames
        velocity_y = (self.goal.y - self.position.y) / total_frames
        return pygame.Vector2(velocity_x, velocity_y)

    
    def _move_towards_goal(self):
        # LOOK INTO self.position.movetowards(Vector2)
        self.position.x = (self.position.x + self.velocity.x) % (self.screen.get_width() + 10)
        self.position.y = (self.position.y + self.velocity.y) % (self.screen.get_height() + 10)

    def _chill(self):
        sign = lambda : random.choice([-1, 1])
        self.position.x += 0.1 * sign()
        self.position.y += 0.1 * sign()
        

    def _random_time_frame(self, min=2, max=4):
        return random.randint(min, max)