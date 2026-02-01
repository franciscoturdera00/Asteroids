import math
from typing import Callable, List
import pygame
from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import Asteroid, SizeType
from Interactables_Objects.Items.Item import Item
from game_logic.Score import Score

class BlackHoleItem(Item):

    NUKE_RADIUS = 500
    PACE = 5

    def __init__(self, screen, fps, players, initial_location, size, pick_up_sound_path="Sounds/blackhole.wav"):
        self.retreat_tick = 0
        super().__init__(screen, fps, players, initial_location, size, pick_up_sound_path)
    
    def _current_radius(self):
        return self.ticks_since_grabbed * self.PACE

    def _is_expanding(self):
        return self._current_radius() <= self.NUKE_RADIUS

    def _consume_entities(self, entities, play_sounds_function, get_sound_arg):
        if not self._is_expanding():
            return False
        radius = self._current_radius()
        consumed = [e for e in entities if e.position.distance_to(self.position) <= radius]
        for entity in consumed:
            entities.remove(entity)
            if play_sounds_function:
                play_sounds_function(get_sound_arg(entity))
        return True

    def perform_action_on_asteroids(self, asteroids: List[Asteroid], play_sounds_function: Callable[[int], None] | None = None):
        return self._consume_entities(asteroids, play_sounds_function, lambda a: int(a.size))

    def perform_action_on_score(self, score: Score):
        score.score += 15
        return super().perform_action_on_score(score)

    def perform_action_on_aliens(self, aliens: List[Alien], play_sounds_function: Callable[[int], None] | None = None):
        return self._consume_entities(aliens, play_sounds_function, lambda _: SizeType.MEDIUM)
    
    def render(self):
        self.draw_nuke(1 if self.show else 0.5)

    def render_item_effect(self):
        if self._is_expanding():
            radius = self._current_radius()
            self.retreat_tick = self.ticks_since_grabbed
        elif self.retreat_tick * self.PACE >= 0:
            radius = self.retreat_tick * self.PACE
            self.retreat_tick -= 3
        else:
            return False
        pygame.draw.circle(self.screen, "black", self.position, radius)
        pygame.draw.circle(self.screen, "white", self.position, radius, 1)
        return True

    # Function to draw the Nuke
    def draw_nuke(self, scale):
        # Draw the bomb body (circle)
        pygame.draw.circle(self.screen, "white", self.position, 5 * scale)
        
        # Draw the fuse (line)
        fuse_start = (self.position.x, self.position.y - 5 * scale)
        fuse_end = (self.position.x, self.position.y  - 10 * scale)
        pygame.draw.line(self.screen, "white", fuse_start, fuse_end, math.ceil(2 * scale))
        
        # Draw the spark (small circle)
        pygame.draw.circle(self.screen, "red", fuse_end, 1 * scale)