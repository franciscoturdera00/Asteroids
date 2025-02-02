
import math
import pygame


class Player:

    SPEED = 5
    ROTATIONAL_SPEED = 10

    def __init__(self, position: pygame.Vector2, scale=1, starting_angle=0, color="white"):
        self.position = position
        self.velocity = [0,0]
        self.scale = scale
        self.color = color
        self.angle = starting_angle
        self.player_shape = [(24 * scale, 0), (-24 * scale, -18 * scale), (-18 * scale, 0), (-24 * scale,  18 * scale)]
    
    
    def move(self, speed=SPEED):
        print(1, self.position.x, self.position.y)
        self.position.x = self.position.x + math.cos(self._angle_in_radians()) * speed
        self.position.y = self.position.y + math.sin(self._angle_in_radians()) * speed

        # self.position.x += self.velocity[0]
        # self.position.y += self.velocity[1]
        print(2, self.position.x, self.position.y)
    
    def rotate(self, direction): # direction in [-1, 1]
        self.angle = (self.angle + direction * self.ROTATIONAL_SPEED) % 360
        print("angle", self.angle, self._angle_in_radians())

    def draw(self, screen):
        shape = list()
        for point in self.player_shape:
            x = (point[0] * math.cos(self._angle_in_radians())) - (point[1] * math.sin(self._angle_in_radians()))
            y = (point[0] * math.sin(self._angle_in_radians())) + (point[1] * math.cos(self._angle_in_radians()))
            shape.append((x, y))


        pygame.draw.polygon(screen, self.color, [(self.position.x + x, self.position.y + y) for x, y in shape], 2)

    def receive_commands(self, keys):
        if keys[pygame.K_a]:
            self.rotate(-1)
        if keys[pygame.K_d]:
            self.rotate(1)
        if keys[pygame.K_w]:
            self.move()

    def _angle_in_radians(self):
        return math.pi * self.angle / 180

