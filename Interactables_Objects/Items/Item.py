
from abc import ABC, abstractmethod
from typing import List
import pygame

from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import Asteroid
from Interactables_Objects.Player import Player
from game_logic.Score import Score


class Item(ABC):

    ITEM_LIFETIME_SECONDS = 10
    HITBOX_SCALE = 6 / 5

    def __init__(self, screen: pygame.Surface, fps, initial_location: pygame.Vector2, size, image_file_path="Images/something_wong.png"):
        self.screen = screen
        self.position = initial_location
        self.size = size
        # create a surface object, image is drawn on it.
        # self.repr = pygame.image.load(image_file_path).convert()
        self.image_file_path = image_file_path
        self.ticks_left = fps * self.ITEM_LIFETIME_SECONDS
        self.show = True

        self.hitbox = size * self.HITBOX_SCALE
        
    @abstractmethod
    def perform_action(self, score: Score = None, player: Player = None, asteroids: List[Asteroid] = None, aliens: List[Alien] = None):
        raise NotImplementedError("Item must implement 'perform_action'")
    
    def update(self):   
        self.ticks_left -= 1
        if self.ticks_left % 15 == 0:
            self.show = not self.show

    @abstractmethod
    def render(self):
        # create a surface object, image is drawn on it.
        # self.repr = pygame.image.load(self.image_file_path).convert()
        # self.screen.blit(self.repr, (pos_x, pos_y))
        raise NotImplementedError("Item must implement 'render'")
        # pygame.draw.circle(self.screen, "red", self.position, self.size)