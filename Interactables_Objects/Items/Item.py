
from abc import ABC, abstractmethod
from typing import Callable, List, final, override
import pygame

from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import Asteroid
from Interactables_Objects.Player import Player
from game_logic.Score import Score


class Item(ABC):

    ITEM_LIFETIME_SECONDS = 15
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
        self.ticks_since_grabbed = 0

        self.hitbox = float(size * self.HITBOX_SCALE)
    
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
        
    # Action performed when player picks up item
    @final
    def perform_action(self, score: Score = None, player: Player = None, asteroids: List[Asteroid] = None, aliens: List[Alien] = None, play_sounds_function: Callable[[int], None] = None):
        # DO NOT MODIFY IN SUBCLASS
        self.ticks_since_grabbed += 1
        self.perform_action_on_score(score)
        self.perform_action_on_player(player)
        self.perform_action_on_asteroids(asteroids, play_sounds_function)
        self.perform_action_on_aliens(aliens, play_sounds_function)

    # Return True if ongoing, False otherwise
    @override
    def render_item_effect(self):
        # Modify this function in your Item subclass to draw something on the screen as a result of picking up the item
        return False
    
    # Return True if ongoing, False otherwise
    @override
    def perform_action_on_player(self, player: Player):
        # Modify this function in your Item subclass to perform an action on the player that picked up this item
        return False

    # Return True if ongoing, False otherwise
    @override
    def perform_action_on_asteroids(self, asteroids: List[Asteroid], play_sounds_function: Callable[[int], None] = None):#, play_sounds_function: Callable[[int], None] = None):
        # Modify this function in your Item subclass to perform an action on any/all interactable asteroids
        return False

    # Return True if ongoing, False otherwise
    @override
    def perform_action_on_aliens(self, aliens: List[Alien], play_sounds_function: Callable[[int], None] = None):
        # Modify this function in your Item subclass to perform an action on any/all interactable aliens
        return False

    # Return True if ongoing, False otherwise
    @override
    def perform_action_on_score(self, score: Score):
        # Modify this function in your Item subclass to perform an action on the game score
        return False
    