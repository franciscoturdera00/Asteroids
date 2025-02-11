
from typing import List
import pygame
from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import Asteroid
from Interactables_Objects.Items.Item import Item
from Interactables_Objects.Player import Player
from game_logic.Score import Score


class PlusBulletItem(Item):

    def render(self):
        if self.show:
            pygame.draw.circle(self.screen, "red", self.position, self.size)
        else:
            pygame.draw.circle(self.screen, "red", self.position, self.size * 0.75)
    
    def perform_action(self, score: Score = None, player: Player = None, asteroids: List[Asteroid] = None, aliens: List[Alien] = None):
        player.max_bullets += 1
        

    