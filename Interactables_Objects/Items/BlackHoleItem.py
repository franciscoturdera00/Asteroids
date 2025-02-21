import math
import pygame
from Interactables_Objects.Asteroid import SizeType
from Interactables_Objects.Items.Item import Item

class BlackHoleItem(Item):

    NUKE_RADIUS = 500
    PACE = 5

    def __init__(self, screen, fps, players, initial_location, size, pick_up_sound_path="Sounds/blackhole.wav"):
        self.retreat_tick = 0
        super().__init__(screen, fps, players, initial_location, size, pick_up_sound_path)
    
    def perform_action_on_asteroids(self, asteroids, play_sounds_function = None):
        if self.ticks_since_grabbed * self.PACE <= self.NUKE_RADIUS:
            def eat_everything():
                for asteroid in asteroids:
                    if asteroid.position.distance_to(self.position) <= self.ticks_since_grabbed * self.PACE:
                        asteroids.remove(asteroid)
                        play_sounds_function(asteroid.size)
                        eat_everything()
                        break
            eat_everything()
            return True
        return False
    
    def perform_action_on_score(self, score):
        score.score += 15
        return super().perform_action_on_score(score)

    def perform_action_on_aliens(self, aliens, play_sounds_function = None):
        if self.ticks_since_grabbed * self.PACE <= self.NUKE_RADIUS:
            def eat_everything():
                for asteroid in aliens:
                    if asteroid.position.distance_to(self.position) <= self.ticks_since_grabbed * self.PACE:
                        aliens.remove(asteroid)
                        play_sounds_function(SizeType.MEDIUM)
                        eat_everything()
                        break
            eat_everything()
            return True
        return False
    
    def render(self):
        if self.show:
            self.draw_nuke(1)
        else:
            self.draw_nuke(0.5)
        
    def render_item_effect(self):
        if self.ticks_since_grabbed * self.PACE <= self.NUKE_RADIUS:
            pygame.draw.circle(self.screen, "black", self.position, self.ticks_since_grabbed * self.PACE)
            pygame.draw.circle(self.screen, "white", self.position, self.ticks_since_grabbed * self.PACE, 1)
            self.retreat_tick = self.ticks_since_grabbed
            return True
        elif self.retreat_tick * self.PACE >= 0:
            pygame.draw.circle(self.screen, "black", self.position, self.retreat_tick * self.PACE)
            pygame.draw.circle(self.screen, "white", self.position, self.retreat_tick * self.PACE, 1)
            self.retreat_tick -= 3
            return True
        return False

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