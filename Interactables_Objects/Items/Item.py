
from abc import ABC, abstractmethod
import math
import random
from typing import Callable, List, final, override
import pygame

from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import Asteroid
from Interactables_Objects.Player import Player
from game_logic.Score import Score


class Item(ABC):

    ITEM_LIFETIME_SECONDS = 15
    HITBOX_SCALE = 6 / 5
    ITEM_PACE = 0.7

    def __init__(self, screen: pygame.Surface, fps, players: List[Player], initial_location: pygame.Vector2, size, pick_up_sound_path="Sounds/life_item.wav"):
        self.screen = screen
        self.position = initial_location
        self.size = size
        self.players = players
        self.pick_up_sound = pygame.mixer.Sound(pick_up_sound_path)
        self.ticks_left = fps * self.ITEM_LIFETIME_SECONDS
        self.fps = fps
        self.show = True
        self.ticks_since_grabbed = 0

        self.velocity = self._change_direction()

        self.hitbox = float(size * self.HITBOX_SCALE)
    
    def update(self):   
        self.ticks_left -= 1
        self.position.x += self.velocity[0]
        self.position.x %= self.screen.get_width()
        self.position.y += self.velocity[1]
        self.position.y %= self.screen.get_height()
        if self.ticks_left % 15 == 0:
            self.show = not self.show
        if self.ticks_left % math.ceil(self.fps * self.ITEM_LIFETIME_SECONDS / 5) == 0:
            self.velocity = self._change_direction()
    
    def _change_direction(self):
        angle = random.random() * 2 * math.pi
        max_x_vel = self.ITEM_PACE * math.cos(angle)
        max_y_vel = self.ITEM_PACE * math.sin(angle)
        return random.random() * max_x_vel, random.random() * max_y_vel

        

    def play_pick_up_sound(self):
        self.pick_up_sound.play()
        # self.pick_up_sound.fadeout(4000)

    @abstractmethod
    def render(self):
        # create a surface object, image is drawn on it.
        # self.repr = pygame.image.load(self.image_file_path).convert()
        # self.screen.blit(self.repr, (pos_x, pos_y))
        raise NotImplementedError("Item must implement 'render'")
        
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
    