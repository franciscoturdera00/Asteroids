
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

    # NUMBER_INITIAL_ASTEROIDS = random.randint(3,7)
    NUMBER_INITIAL_ASTEROIDS = 5

    INITIAL_ASTEROID_SPAWN_RATE_SECONDS = 7

    # Set to True to see object bounds and other tools (maybe someday)
    debugging_mode = False

    while play_again:
        play_game(width, height, initial_asteroid_number=NUMBER_INITIAL_ASTEROIDS, fps=60, explosion_sounds=explosion_sounds, 
                num_background_asts=NUMBER_BACKGROUND_AESTHETIC_ASTEROIDS, background_music=BACKGROUND_MUSIC,
                initial_asteroid_spawn_rate_seconds=INITIAL_ASTEROID_SPAWN_RATE_SECONDS, debugging_mode=debugging_mode)


def play_game(screen_width, screen_height, initial_asteroid_number, fps, explosion_sounds, 
              num_background_asts, background_music: pygame.mixer.Sound, 
              initial_asteroid_spawn_rate_seconds, debugging_mode=False):
    # pygame setup
    screen = pygame.display.set_mode((screen_width - 150, screen_height - 100))
    pygame.display.set_caption("ASTEROIDS")
    clock = pygame.time.Clock()
    running = True
    score = Score()
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

    #Background music
    pygame.mixer.Channel(0).play(background_music, loops=1000)

    tick = 0

    while running:
        running = tick_game(screen, player, asteroids, score, lives, clock, fps, explosion_sounds, 
                            background_aesthetics=background_asteroids, asteroid_spawn_rate_seconds=initial_asteroid_spawn_rate_seconds,
                            game_tick=tick, show_bounds=debugging_mode)
        tick += 1
    
    if len(asteroids) == 0:
        print("You Win")
        player.color = "green"
        score.win()
        win_screen(screen, background_asteroids, player, asteroids, clock, score)
        return
    else:
        # Lose Conditions
        print("You Lose!")
        player.color = "red"
        lose_screen(screen, background_asteroids, player, asteroids, clock, score)
    

# Returns True if the game is still going. False otherwise
def tick_game(screen: pygame.Surface, player: Player, asteroids: List[Asteroid], 
              score: Score, lives: Lives, clock: pygame.time.Clock, fps, explosion_sounds, 
              background_aesthetics: List[Asteroid], asteroid_spawn_rate_seconds, game_tick, show_bounds=False):
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
        return False
    
    handle_bullet_collisions(screen, player.bullets, asteroids, score, explosion_sounds)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # Aesthetics only
    for background_asteroid in background_aesthetics:
        background_asteroid.tick(screen)
    
    # Score
    score_x_loc = screen.get_width() / 25
    score_y_loc = screen.get_height() / 20
    score.tick(screen, score_x_loc, score_y_loc)

    # RENDER GAME

    # Player and bullets
    player.tick(screen, show_bounds=show_bounds)
    player.receive_commands(shooting=shooting)

    # Lives
    lives.tick(screen)

    # Asteroids
    for asteroid in asteroids:
        asteroid.tick(screen, player.position, show_bounds=show_bounds)

    # limits FPS to 60
    clock.tick(fps)

    game_tick += 1

    # Spawn new asteroid
    if (game_tick / fps) % asteroid_spawn_rate_seconds == 0.0:
        # Find spawn point not near player
        new_asteroid = Asteroid(screen, random.choice(ASTEROID_ORDERED_SIZES[:-1]), is_in_game_spawn=True)
        asteroids.append(new_asteroid)

    # flip() the display
    pygame.display.flip()

    return True


def player_collision_detected(player: Player, asteroids: List[Asteroid]):
    if not player.invincible:
        for asteroid in asteroids:
            actual_distance = player.position.distance_to(asteroid.position)
            min_distance = player.scaled_bound_radius + asteroid.boundary_radius

            if actual_distance <= min_distance:
                return True
    return False 

def handle_bullet_collisions(screen, bullets: List[Bullet], asteroids: List[Asteroid], score: Score, explosions:List[pygame.mixer.Sound]):
    for i, bullet in enumerate(bullets):
        for a, asteroid in enumerate(asteroids):
            actual_distance = bullet.position.distance_to(asteroid.position)
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

def lose_screen(screen: pygame.Surface, background_asteroids: List[Asteroid], player: Player, asteroids: List[Asteroid], clock, score: Score):
    _post_screen(False, screen, background_asteroids, player, asteroids, clock, score)

def win_screen(screen: pygame.Surface, background_asteroids: List[Asteroid], player: Player, asteroids: List[Asteroid], clock, score: Score):
    _post_screen(True, screen, background_asteroids, player, asteroids, clock, score)

def _post_screen(win, screen: pygame.Surface, background_asteroids: List[Asteroid], player: Player, asteroids: List[Asteroid], clock, score: Score):
    size = 100
    font_title = pygame.font.SysFont('Smooch Sans', size, bold=True)
    font_play_again = pygame.font.SysFont('Smooch Sans', math.ceil(size / 2))
    boo = pygame.mixer.Sound("Sounds/booing_sound.wav")
    cheer = pygame.mixer.Sound("Sounds/applause.wav")
    channel = 2
    # Play Sounds
    if win:
        pygame.mixer.Channel(channel).play(cheer)
    if not win:
        pygame.mixer.Channel(channel).play(boo)
    while True:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global play_again
                play_again = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Channel(channel).stop()
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

        score_x_loc = screen.get_width() / 2 - 50
        score_y_loc = screen.get_height() / 2
        score.tick(screen, score_x_loc, score_y_loc, size=150, count=False)

        play_again_surface = font_play_again.render("Click to Play Again", False, (100, 100, 100))
        screen.blit(play_again_surface, (screen.get_width() / 2 - size, screen.get_height() * 4 / 5 - size))

        # Draw rest of (inactive) game
        player.tick(screen, active_game=False)
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