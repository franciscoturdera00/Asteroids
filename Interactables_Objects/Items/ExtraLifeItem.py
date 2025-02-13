
import pygame
from Interactables_Objects.Items.Item import Item


class ExtraLifeItem(Item):

    def __init__(self, screen, fps, players, initial_location, size, pick_up_sound_path="Sounds/life_item.mp3"):
        A = 0.5
        self.color = [255 * A, 255 * A, 255 * A]
        super().__init__(screen, fps, players, initial_location, size, pick_up_sound_path)

    def render(self):
        if self.show:
            self._render_by_scale(0.4)
        else:
            self._render_by_scale(0.2)

    def perform_action_on_player(self, player):
        for p in self.players:
            if p != player and p.lives.number == 0:
                p.revive()
                return super().perform_action_on_player(player)
        player.lives.number += 1
        return super().perform_action_on_player(player)
    
    def _render_by_scale(self, scale):
        self.life_shape = [(0, -24 * scale), (18 * scale, 24 * scale), (0, 18 * scale), (-18 * scale, 24 * scale)]
        pygame.draw.polygon(self.screen, self.color, [(self.position.x + x, self.position.y + y) for x, y in self.life_shape], 2)