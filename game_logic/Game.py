
from copy import deepcopy
import math
import random
from typing import List
import pygame

from Interactables_Objects.Asteroid import ASTEROID_ORDERED_SIZES, Asteroid, SizeType
from Interactables_Objects.Player import Player
from game_logic.Lives import Lives
from game_logic.Score import Score

# Asteroids Game
# Create your own challenge (will pull settings from config file)
class Game:

    def __init__(self, screen: pygame.Surface, debugging_mode=False):
        # Default game settings
        # TODO: Import from config file
        self.screen=screen
        self.screen_width=screen.get_width()
        self.screen_height=screen.get_height()
        self.fps=60

        self.num_background_asteroids=150
        self.asteroid_spawn_rate_seconds=7
        self.initial_asteroid_number=7

        self.initial_player_lives=3
        self.intial_player_position_x = self.screen_width / 2
        self.intial_player_position_y = self.screen_height / 2
        self.intial_player_position = pygame.Vector2(self.screen_width / 2, self.screen_height / 2)
        
   
        sounds = self._soundify("Sounds/background_game_music.wav",
                                "Sounds/player_hit_sound.wav", 
                                "Sounds/bangLarge.wav", 
                                "Sounds/bangMedium.wav", 
                                "Sounds/bangSmall.wav")
        self.background_music = sounds[0]
        self.player_hit_sound = sounds[1]
        self.explosion_sounds_big_to_small = sounds[2:]
        
        self.debugging_mode=debugging_mode

        self._create_game_objects()

    def _create_game_objects(self):

        # NON-INTERACTABLE OBJECTS
        # Initiate Background Aesthetics
        self.background_asteroids: List[Asteroid] = [Asteroid(self.screen, random.choice([s for s in SizeType]), background=True) for _ in range(self.num_background_asteroids)]
        
        self.score = Score()
        self.lives = Lives(self.initial_player_lives)
        self.clock = pygame.time.Clock()
        self.game_tick = 0
        self.win = False
        
        # INTERACTABLE OBJECTS
        # Initiate Player
        # TODO: Allow for multiple players
        intial_player_position = pygame.Vector2(self.intial_player_position_x, self.intial_player_position_y)
        self.player=Player(self.screen, intial_player_position, fps=self.fps)

        # Initiate Asteroids
        self.asteroids: List[Asteroid] = [Asteroid(self.screen, SizeType.LARGE) for _ in range(self.initial_asteroid_number)]
        
    # Returns True if player wants to play again
    def run(self):
        #Background music
        pygame.mixer.Channel(0).play(self.background_music, loops=1000)
        game_continues  = True
        while game_continues:
            game_continues = self._tick()
        return self._run_post_game()
    

    # Returns True if the game is still going, False otherwise
    def _tick(self):
        # limits FPS to 60
        self.clock.tick(self.fps)
        self.game_tick += 1

        shooting = False
        # Game events (user-input and more)
        # pygame.QUIT - user clicked X to close your window
        # pygame.K_SPACE - checking if SPACE has been pressed (once)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.score.bullet_fired()
                shooting = True
        
        # No asteroids left in Game
        if len(self.asteroids) == 0: 
            self._win()
            return False
        
        # interactions
        if self._player_collision_detected():
            self.score.player_hit()
            pygame.mixer.Channel(6).play(self.player_hit_sound)
            dead = self.lives.die()
            if dead:
                return False
            else:
                self.player.restart_position(self.screen, invincible=True)
        
        self._handle_bullet_collisions()

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")
        # Aesthetics only
        [background_asteroid.tick() for background_asteroid in self.background_asteroids]
        # Score
        score_x_loc = self.screen_width / 25
        score_y_loc = self.screen_height / 20
        self.score.tick(self.screen, score_x_loc, score_y_loc)

        # Player and bullets
        self.player.tick()
        self.player.receive_commands(shooting=shooting)

        # Lives
        self.lives.tick(self.screen)

         # Asteroids
        [asteroid.tick() for asteroid in self.asteroids]
        
        # Spawn new asteroid
        if (self.game_tick / self.fps) % self.asteroid_spawn_rate_seconds == 0.0:
            # Find spawn point not near player
            new_asteroid = Asteroid(self.screen, random.choice(ASTEROID_ORDERED_SIZES[:-1]), is_in_game_spawn=True)
            self.asteroids.append(new_asteroid)

        # flip() the display
        pygame.display.flip()

        return True


    def _run_post_game(self):
        size = 100
        font_title = pygame.font.SysFont('Smooch Sans', size, bold=True)
        font_play_again = pygame.font.SysFont('Smooch Sans', math.ceil(size / 2))
 
        boo = pygame.mixer.Sound("Sounds/booing_sound.wav")
        cheer = pygame.mixer.Sound("Sounds/applause.wav")
        channel = 2
        # Play Sounds
        if self.win:
            pygame.mixer.Channel(channel).play(cheer)
            status_surface = font_title.render("YOU WIN!", False, (0, 180, 0))
            self.player.color = "green"
        if not self.win:
            pygame.mixer.Channel(channel).play(boo)
            status_surface = font_title.render("OOPS! YOU LOSE!", False, (180, 0, 0))
            self.player.color = "red"
        
        running = True
        while running == True: # running: [True, False, "quit"]
            running = self._tick_post_game(size, font_play_again, status_surface, channel)

        return running != "quit"

    
    def _tick_post_game(self, size, font_play_again, status_surface, sound_channel):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Channel(sound_channel).stop()
                return False
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")
        # Draw background asteroids before text
        [background_asteroid.tick() for background_asteroid in self.background_asteroids]

        self.screen.blit(status_surface, (self.screen_width / 2 - size * 2, self.screen_height / 2 - size))

        score_x_loc = self.screen_width / 2 - 50
        score_y_loc = self.screen_height / 2
        self.score.tick(self.screen, score_x_loc, score_y_loc, size=150, count=False)

        play_again_surface = font_play_again.render("Click to Play Again", False, (100, 100, 100))
        self.screen.blit(play_again_surface, (self.screen_width / 2 - size, self.screen_height * 4 / 5 - size))

        # Draw rest of (inactive) game
        self.player.tick(active_game=False)
        if not self.win:
            self.player._rotate_angle(1)
        else:
            self.player.receive_commands(shooting=False)

        [asteroid.tick() for asteroid in self.asteroids]

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        self.clock.tick(60) / 1000

        return True
        
    def _player_collision_detected(self):
        if not self.player.invincible:
            for asteroid in self.asteroids:
                actual_distance = self.player.position.distance_to(asteroid.position)
                min_distance = self.player.scaled_bound_radius + asteroid.boundary_radius

                if actual_distance <= min_distance:
                    return True
        return False
    
    def _soundify(self, *file_paths):
        return [pygame.mixer.Sound(file) for file in file_paths]
    
    def _win(self):
        self.win = True
    
    def _handle_bullet_collisions(self):
        bullets = self.player.bullets
        for bullet_index, bullet in enumerate(bullets):
            for asteroid_index, asteroid in enumerate(self.asteroids):
                actual_distance = bullet.position.distance_to(asteroid.position)
                min_distance = bullet.RADIUS + asteroid.boundary_radius

                if actual_distance <= min_distance:
                    # Update score
                    self.score.asteroid_hit(asteroid.size)

                    # Update bullets
                    if bullet in bullets:
                        bullets.remove(bullet)

                    # Update asteroids
                    self.asteroids.remove(asteroid)
                    new_type = ASTEROID_ORDERED_SIZES[ASTEROID_ORDERED_SIZES.index(SizeType(asteroid.size)) + 1]
                    if new_type is not None:
                        for _ in range(2):
                            new_ast = Asteroid(self.screen, new_type, deepcopy(asteroid.position))
                            self.asteroids.append(new_ast)
                    
                    # Play asteroid explosion sound
                    if asteroid.size == SizeType.LARGE.value:
                        self.explosion_sounds_big_to_small[0].play()
                    elif asteroid.size == SizeType.MEDIUM.value:
                        self.explosion_sounds_big_to_small[1].play()
                    elif asteroid.size == SizeType.SMALL.value:
                        self.explosion_sounds_big_to_small[2].play()

                if asteroid_index >= len(self.asteroids):
                    break
            if bullet_index >= len(bullets):
                break

        