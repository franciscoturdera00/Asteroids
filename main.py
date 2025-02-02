
import random
from typing import List
import pygame
from Player import Player
from Asteroid import Asteroid
import tkinter as tk


def tick_game(screen, clock, player: Player, asteroids: List[Asteroid]):
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
    # for asteroid in asteroids:
    #     asteroid.draw(screen)

    keys = pygame.key.get_pressed()

    player.receive_commands(keys)
    # # if keys[pygame.K_w]:
    # #     player.move()
    # # if keys[pygame.K_a]:
    # #     player_pos.x -= 300 * dt
    # #     player.rotate(-1)
    # # if keys[pygame.K_d]:
    # #     player.rotate(1)
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    return running
    

def main():
    # pygame setup
    pygame.init()
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    screen = pygame.display.set_mode((width - 50, height - 100))
    clock = pygame.time.Clock()
    running = True
    dt = 0 
    initial_asteroid_number = 10

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    player = Player(player_pos, scale=0.5)
    asteroids = list()
    sign = [-1, 1]
    for _ in range(initial_asteroid_number):
        x_start = random.randrange(0, screen.get_width())
        y_start = random.randrange(0, screen.get_height())
        x_vel = random.randint(1, 5) * random.choice(sign)
        y_vel = random.randint(1, 5) * random.choice(sign)
        size = random.randrange(10, 40)
        asteroid = Asteroid(pygame.Vector2(x_start, y_start), size, x_vel, y_vel)
        asteroids.append(asteroid)

    while running:
        running = tick_game(screen, clock, player, asteroids)

    pygame.quit()


main()