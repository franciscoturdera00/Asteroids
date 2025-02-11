
import pygame
from Interactables_Objects.Items.Item import Item


class ExtraLifeItem(Item):

    def render(self):
        if self.show:
            self._render_by_scale(0.4)
        else:
            self._render_by_scale(0.2)

    def perform_action_on_player(self, player):
        player.lives.number += 1
        return super().perform_action_on_player(player)
    
    def _render_by_scale(self, scale):
        self.life_shape = [(0, -24 * scale), (18 * scale, 24 * scale), (0, 18 * scale), (-18 * scale, 24 * scale)]
        pygame.draw.polygon(self.screen, "white", [(self.position.x + x, self.position.y + y) for x, y in self.life_shape], 2)