

# Choose-Mode Screen.
# TODO: Alter configurations
import math
import random
from typing import List
import pygame

from Interactables_Objects.Asteroid import Asteroid, SizeType

class PreGame:

    def __init__(self, screen: pygame.Surface, font_path):
        self.background_music = pygame.mixer.Sound("Sounds/background_game_music.wav")
        self.screen = screen
        self.multiplayer = False
        self.font_path = font_path

        self.num_background_asteroids = 300
        self.clock = pygame.time.Clock()

        # NON-INTERACTABLE OBJECTS
        # Initiate Background Aesthetics
        self.background_asteroids: List[Asteroid] = [Asteroid(self.screen, random.choice([s for s in SizeType]), background=True) for _ in range(self.num_background_asteroids)]

    def run(self):
        #Background music
        pygame.mixer.Channel(0).set_volume(0.7)
        pygame.mixer.Channel(0).play(self.background_music, loops=10000)

        font_size = 200
        font_title = pygame.font.Font(self.font_path, font_size)
        font_play_type = pygame.font.Font(self.font_path, math.ceil(font_size / 3))
        running = True
        while running:
            running = self.update()
            self.render(font_title, font_play_type, font_size)

        
        

    def update(self):
        # limits FPS to 60
        self.clock.tick(45)
        # Game events (user-input and more)
        # pygame.QUIT - user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.multiplayer = False
            return False
        elif keys[pygame.K_2]:
            self.multiplayer = True
            return False

        # Aesthetics only
        [background_asteroid.update() for background_asteroid in self.background_asteroids]

        return True

    def render(self, font_title: pygame.font.Font, font_play_type: pygame.font.Font, size):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")
        # Aesthetics only
        [background_asteroid.render() for background_asteroid in self.background_asteroids]

        spacing = 150
        color = (70, 200, 70)
        
        # Title
        status_surface = font_title.render("Asteroids", True, color)
        self.screen.blit(status_surface, (self.screen.get_width() / 2 - size * 2, self.screen.get_height() / 2 - 2 * size + spacing))

        # 1 Player
        status_surface = font_play_type.render("[1] 1-Player [W,A,D,SPACE]", True, color)
        self.screen.blit(status_surface, (self.screen.get_width() / 5 - size / 3 * 2.5, self.screen.get_height() / 2 - 2 * size / 3 + spacing * 2))

        # 2 Player
        status_surface = font_play_type.render("[2] 2-Player [UP,LEFT,RIGHT,R_SHIFT]", True, color)
        self.screen.blit(status_surface, (self.screen.get_width() / 5 - size / 3 * 2.5, self.screen.get_height() / 2 - 2 * size / 3 + spacing * 2.5))

        # flip() the display
        pygame.display.flip()