
from copy import deepcopy
import math
import random
from typing import List
import pygame
from features.Lives import Lives
from Interactables_Objects.Bullet import Bullet
from Interactables_Objects.Player import Player
from Interactables_Objects.Asteroid import ASTEROID_ORDERED_SIZES, Asteroid, SizeType
import tkinter as tk

from features.Score import Score

play_again = True

def main():
    # System info
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # Initilalize game dev lib
    pygame.init()
    pygame.font.init()

    # Asteroid game sounds
    BIG_EXPLODE = pygame.mixer.Sound("Sounds/bangLarge.wav")
    MEDIUM_EXPLODE = pygame.mixer.Sound("Sounds/bangMedium.wav")
    SMALL_EXPLODE = pygame.mixer.Sound("Sounds/bangSmall.wav")
    explosion_sounds = [BIG_EXPLODE, MEDIUM_EXPLODE, SMALL_EXPLODE]

    BACKGROUND_MUSIC = pygame.mixer.Sound("Sounds/background_game_music.wav")

    NUMBER_BACKGROUND_AESTHETIC_ASTEROIDS = 150

    NUMBER_INITIAL_ASTEROIDS = 1

    # Set to True to see object bounds and other tools (maybe someday)
    debugging_mode = False

    while play_again:
        play_game(width, height, initial_asteroid_number=NUMBER_INITIAL_ASTEROIDS, fps=60, explosion_sounds=explosion_sounds, 
                num_background_asts=NUMBER_BACKGROUND_AESTHETIC_ASTEROIDS, background_music=BACKGROUND_MUSIC,
                debugging_mode=debugging_mode)


def play_game(screen_width, screen_height, initial_asteroid_number, fps, explosion_sounds, num_background_asts, background_music: pygame.mixer.Sound, debugging_mode=False):
    # pygame setup
    screen = pygame.display.set_mode((screen_width - 150, screen_height - 100))
    pygame.display.set_caption("ASTEROIDS")
    clock = pygame.time.Clock()
    running = True
    score = Score(screen)
    lives = Lives()

    # Initiate Background Aesthetics
    background_asteroids = list()
    for _ in range(num_background_asts):
        background_asteroid = Asteroid(screen, random.choice([s for s in SizeType]), background=True)
        background_asteroids.append(background_asteroid)

    # Initiate Asteroids
    asteroids = list()
    for _ in range(initial_asteroid_number):
        asteroid = Asteroid(screen, SizeType.LARGE)
        asteroids.append(asteroid)
    
    # Initiate Player
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player = Player(player_pos, scale=0.5, fps=fps)
    pygame.mixer.Channel(0).play(background_music, loops=1000)
    while running:
        running = tick_game(screen, player, asteroids, score, lives, clock, fps, explosion_sounds, background_aesthetics=background_asteroids, show_bounds=debugging_mode)
    
    if len(asteroids) == 0:
        print("You Win")
        player.color = "green"
        win_screen(screen, background_asteroids, player, asteroids, clock)
        return
    else:
        # Lose Conditions
        print("You Lose!")
        player.color = "red"
        lose_screen(screen, background_asteroids, player, asteroids, clock)
    

# Returns True if the game is still going. False otherwise
def tick_game(screen: pygame.Surface, player: Player, asteroids: List[Asteroid], score: Score, lives: Lives, clock, fps, explosion_sounds, background_aesthetics: List[Asteroid], show_bounds=False):
    shooting = False
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # pygame.K_SPACE - Checking if SPACE has been pressed (once)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global play_again
            play_again = False
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            score.bullet_fired()
            shooting = True
    
    # interactions
    if player_collision_detected(player, asteroids):
        score.player_hit()
        player_hit_sound = pygame.mixer.Sound("Sounds/player_hit_sound.wav")
        player_hit_sound.play()
        dead = lives.die()
        if dead:
            return False
        else:
            player.restart_position(screen, invincible=True)
    
    if len(asteroids) == 0: # no asteroids left in the game
        print("You Won!")
        return False
    
    handle_bullet_collisions(screen, player.bullets, asteroids, score, explosion_sounds)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # Aesthetics only
    for background_asteroid in background_aesthetics:
        background_asteroid.tick(screen)

    # RENDER GAME

    # Player and bullets
    player.tick(screen, show_bounds=show_bounds)
    player.receive_commands(shooting=shooting)

    # Lives
    lives.tick(screen)

    # Asteroids
    for asteroid in asteroids:
        asteroid.tick(screen, player.position, show_bounds=show_bounds)

    # Score
    score.tick(screen)

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

def handle_bullet_collisions(screen, bullets: List[Bullet], asteroids: List[Asteroid], score: Score, explosions:List[pygame.mixer.Sound]):
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
                
                # Play asteroid explosion sound
                if asteroid.size == SizeType.LARGE.value:
                    explosions[0].play()
                elif asteroid.size == SizeType.MEDIUM.value:
                    explosions[1].play()
                elif asteroid.size == SizeType.SMALL.value:
                    explosions[2].play()

            if a >= len(asteroids):
                break
        if i >= len(bullets):
            break

def lose_screen(screen: pygame.Surface, background_asteroids: List[Asteroid], player: Player, asteroids: List[Asteroid], clock):
    _post_screen(False, screen, background_asteroids, player, asteroids, clock)

def win_screen(screen: pygame.Surface, background_asteroids: List[Asteroid], player: Player, asteroids: List[Asteroid], clock):
    _post_screen(True, screen, background_asteroids, player, asteroids, clock)

def _post_screen(win, screen: pygame.Surface, background_asteroids: List[Asteroid], player: Player, asteroids: List[Asteroid], clock):
    size = 100
    font_title = pygame.font.SysFont('Smooch Sans', size, bold=True)
    font_play_again = pygame.font.SysFont('Smooch Sans', math.ceil(size / 2))
    boo = pygame.mixer.Sound("Sounds/booing_sound.wav")
    cheer = pygame.mixer.Sound("Sounds/applause.wav")
    # Play Sounds
    if win:
        pygame.mixer.Channel(2).play(cheer)
    if not win:
        pygame.mixer.Channel(2).play(boo)
    while True:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global play_again
                play_again = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Channel(7).stop()
                return True
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        # Draw background asteroids before text
        [background_asteroid.tick(screen) for background_asteroid in background_asteroids]
        # Draw Text
        if win:
            status_surface = font_title.render("YOU WIN!", False, (0, 180, 0))
        else:
            status_surface = font_title.render("OOPS! YOU LOSE!", False, (180, 0, 0))
        screen.blit(status_surface, (screen.get_width() / 2 - size * 2, screen.get_height() / 2 - size))

        play_again_surface = font_play_again.render("Click to Play Again", False, (100, 100, 100))
        screen.blit(play_again_surface, (screen.get_width() / 2 - size, screen.get_height() * 3 / 4 - size))

        # Draw rest of (inactive) game
        player.tick(screen)
        if not win:
            player._rotate_angle(1)
        else:
            player.receive_commands(shooting=False)

        [asteroid.tick(screen) for asteroid in asteroids]

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        clock.tick(60) / 1000

main()