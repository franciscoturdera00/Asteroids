
import pygame
from Interactables_Objects.Alien import Alien
from Interactables_Objects.Player import Player


class SmartAlien(Alien):

    SPEED = 1

    def __init__(self, player_target, screen: pygame.Surface, fps, position: pygame.Vector2 = None, color = "white", size = 20, debugging_mode=False):
        self.player_target = player_target

    def update(self, player_positions):
        direction = lambda player, alien : -self.SPEED if player < alien else self.SPEED
        self.position.x += direction(self.player_target.x, self.position.x)
        self.position.y += direction(self.player_target.y, self.position.y)