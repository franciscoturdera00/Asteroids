
import random
from typing import List
import pygame
from Interactables.Player import Player
from Interactables.Asteroid import Asteroid
import tkinter as tk

def main():
    # System info
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((width - 50, height - 100))
    clock = pygame.time.Clock()
    running = True
    initial_asteroid_number = 30
    asteroid_max_speed = 5

    # For debugging
    show_bounds = False

    # Initiate Player
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player = Player(player_pos, scale=0.5, show_bounds=show_bounds)

    # Initiate Asteroids
    asteroids = list()
    sign = [-1, 1]
    for _ in range(initial_asteroid_number):
        x_start = random.randrange(0, screen.get_width())
        y_start = random.randrange(0, screen.get_height())
        x_vel = random.randint(1, asteroid_max_speed) * random.choice(sign)
        y_vel = random.randint(1, asteroid_max_speed) * random.choice(sign)
        size = random.randrange(10, 40)

        asteroid = Asteroid(pygame.Vector2(x_start, y_start), size, x_vel, y_vel)
        asteroids.append(asteroid)

    while running:
        running = tick_game(screen, player, asteroids)
        
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        clock.tick(60) / 1000
    pygame.quit()


def tick_game(screen, player: Player, asteroids: List[Asteroid]):
    running = True
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER GAME
    player.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)

    keys = pygame.key.get_pressed()

    player.receive_commands(keys)
    return running


main()