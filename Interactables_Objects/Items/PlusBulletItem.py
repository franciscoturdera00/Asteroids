import pygame
from Interactables_Objects.Items.Item import Item
from Interactables_Objects.Player import Player


class PlusBulletItem(Item):

    def __init__(self, screen, fps, players, initial_location, size, pick_up_sound_path="Sounds/bullet_pick_up.wav"):
        super().__init__(screen, fps, players, initial_location, size, pick_up_sound_path)

    def render(self):
        radius = self.size if self.show else self.size * 0.75
        pygame.draw.circle(self.screen, "red", self.position, radius)
    
    def perform_action_on_player(self, player: Player):
        player.max_bullets += 1
        return super().perform_action_on_player(player)
        

    