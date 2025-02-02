
from copy import deepcopy
import math
from typing import List
import pygame
from Interactables_Objects.Bullet import Bullet
from Interactables_Objects.Player import Player
from Interactables_Objects.Asteroid import ASTEROID_ORDERED_SIZES, Asteroid, SizeType
import tkinter as tk

from features.Score import Score

def main():
    # System info
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((width - 150, height - 100))
    pygame.display.set_caption("ASTEROIDS")
    clock = pygame.time.Clock()
    running = True
    initial_asteroid_number = 5
    fps = 60

    # For debugging
    show_bounds = False

    score = Score()

    # Initiate Player
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player = Player(player_pos, scale=0.5, fps=fps)

    # Initiate Asteroids
    asteroids = list()
    for _ in range(initial_asteroid_number):
        asteroid = Asteroid(screen, SizeType.LARGE)
        asteroids.append(asteroid)

    while running:
        running = tick_game(screen, player, asteroids, score, show_bounds, clock, fps)
        
    pygame.quit()


# Returns True if the game is still going. False otherwise
def tick_game(screen, player: Player, asteroids: List[Asteroid], score: Score, show_bounds, clock, fps):
    print(score.score)
    shooting = False
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # pygame.K_SPACE - Checking if SPACE has been pressed (once)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            score.bullet_fired()
            shooting = True
    
    # interactions
    if player_collision_detected(player, asteroids):
        score.player_hit()
        return False
    
    handle_bullet_collisions(screen, player.bullets, asteroids, score)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER GAME

    # Player and bullets
    player.tick(screen, show_bounds=show_bounds)

    # Asteroids
    for asteroid in asteroids:
        asteroid.tick(screen, show_bounds=show_bounds)

    # Score
    score.tick()
    
    player.receive_commands(shooting=shooting)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(fps) / 1000

    return True


def player_collision_detected(player: Player, asteroids: List[Asteroid]):
    if not player.invincible:
        for asteroid in asteroids:
            actual_distance = math.sqrt((player.position.x - asteroid.position.x)**2 + (player.position.y - asteroid.position.y)**2)
            min_distance = player.scaled_bound_radius + asteroid.boundary_radius

            if actual_distance <= min_distance:
                return True
    return False

def handle_bullet_collisions(screen, bullets: List[Bullet], asteroids: List[Asteroid], score: Score):
    for i, bullet in enumerate(bullets):
        for a, asteroid in enumerate(asteroids):
            actual_distance = math.sqrt((bullet.position.x - asteroid.position.x)**2 + (bullet.position.y - asteroid.position.y)**2)
            min_distance = bullet.RADIUS + asteroid.boundary_radius

            if actual_distance <= min_distance:
                # Update score
                score.asteroid_hit(asteroid.size)

                # Update bullets
                if bullet in bullets:
                    bullets.remove(bullet)

                # Update asteroids
                asteroids.remove(asteroid)
                new_type = ASTEROID_ORDERED_SIZES[ASTEROID_ORDERED_SIZES.index(SizeType(asteroid.size)) + 1]
                if new_type is not None:
                    for _ in range(2):
                        new_ast = Asteroid(screen, new_type, deepcopy(asteroid.position))
                        asteroids.append(new_ast)
            if a >= len(asteroids):
                break
        if i >= len(bullets):
            break

main()