
from copy import deepcopy
import math
import random
from typing import List
import pygame

from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import ASTEROID_ORDERED_SIZES, Asteroid, SizeType
from Interactables_Objects.Player import Player
from game_logic.Score import Score

# Asteroids Game
# Create your own challenge (will pull settings from config file)
class Game:

    def __init__(self, screen: pygame.Surface, font_path, two_player=False, debugging_mode=False):
        # Default game settings
        # TODO: Import from config file
        self.font_path = font_path
        self.screen=screen
        self.screen_width=screen.get_width()
        self.screen_height=screen.get_height()
        self.fps=45

        self.num_background_asteroids=300
        self.initial_asteroid_number=7
        self.initial_player_lives=3
        
        if two_player:
            self.intial_players_positions = [(-self.screen_width / 3, self.screen_height / 2), (-self.screen_width * 2 / 3, self.screen_height / 2)]
        else:
            self.intial_players_positions = [(-self.screen_width / 2, self.screen_height / 2)]\
        
        # Rates depend on number of players
        self.asteroid_spawn_rate_seconds_per_player = math.ceil(7 / len(self.intial_players_positions))
        self.alien_spawn_rate_seconds_per_player = math.ceil(12 / len(self.intial_players_positions))
   
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
        
        self.score = Score(self.screen, self.font_path)
        self.clock = pygame.time.Clock()
        self.game_tick = 0
        self.win = False
        
        # INTERACTABLE OBJECTS
        # Initiate Player
        player_1_initial_position =- pygame.Vector2(self.intial_players_positions[0][0], self.intial_players_positions[0][1])
        player1 = Player(0, self.screen, player_1_initial_position,  fps=self.fps, debugging_mode=self.debugging_mode)
        self.players = [player1]

        if len(self.intial_players_positions) == 2:
            player_2_initial_position =- pygame.Vector2(self.intial_players_positions[1][0], self.intial_players_positions[1][1])
            player2 = Player(1, self.screen, player_2_initial_position,  fps=self.fps, color="purple",
                             thrust_button=[pygame.K_i, pygame.K_UP], rotate_left_button=[pygame.K_j, pygame.K_LEFT], rotate_right_button=[pygame.K_l, pygame.K_RIGHT], 
                             shoot_button=[pygame.K_RSHIFT],
                             debugging_mode=self.debugging_mode)
            self.players.append(player2)

        # Initiate Asteroids
        self.asteroids: List[Asteroid] = [Asteroid(self.screen, SizeType.LARGE, debugging_mode=self.debugging_mode) for _ in range(self.initial_asteroid_number)]

        # Intiate Aliens
        self.aliens: List[Alien] = list()
        
    # Returns True if player wants to play again
    def run(self):
        #Background music
        # pygame.mixer.Channel(0).play(self.background_music, loops=1000)

        game_continues  = True
        while game_continues:
            game_continues = self._update_game()
            self.render_game()
        return self._run_post_game()
    

    # Returns True if the game is still going, False otherwise
    def _update_game(self):
        # Game events (user-input and more)
        # pygame.QUIT - user clicked X to close your window
        # pygame.K_SPACE - checking if SPACE has been pressed (once)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for player in self.players:
                if not player.is_dead() and event.type == pygame.KEYDOWN and event.key in player.shoot:
                    self.score.bullet_fired()
                    player.shoot_bullet()

        # limits FPS to 60
        self.clock.tick(self.fps)
        self.game_tick += 1

        if self._players_have_won(): 
            self._win()
            return False
        
        # interactions
        for player in self.players:
            if player.is_dead():
                player.color = "red"
                player.rotate_angle(1)
            if not player.is_dead() and self._player_collision_detected(player):
                self.score.player_hit()
                pygame.mixer.Channel(6).play(self.player_hit_sound)
                dead = player.lives.die()
                if not dead:
                    player.restart_position(invincible=True)
        all_dead = all([player.is_dead() for player in self.players])
        if all_dead:
            return False
        
        self._handle_bullet_collisions()

         # Aesthetics only
        [background_asteroid.update() for background_asteroid in self.background_asteroids]

        # Player and bullets
        for player in self.players:
            player.update()
            if not player.is_dead():
                player.receive_commands()

        # Spawn new asteroid
        if (self.game_tick / self.fps) % self.asteroid_spawn_rate_seconds_per_player == 0.0:
            new_asteroid = Asteroid(self.screen, random.choice(ASTEROID_ORDERED_SIZES[:-1]), is_in_game_spawn=True, debugging_mode=self.debugging_mode)
            self.asteroids.append(new_asteroid)
        
        # Spawn new Alien
        if (self.game_tick / self.fps) % self.alien_spawn_rate_seconds_per_player == 0.0:
            new_alien = Alien(self.screen, self.fps, debugging_mode=self.debugging_mode)
            self.aliens.append(new_alien)

        # Alien
        for alien in self.aliens:
            alien.update([player.position for player in self.players])

        # Asteroids
        [asteroid.update(players_pos=[player.position for player in self.players]) for asteroid in self.asteroids]

        # Score
        self.score.update()

        return True
    

    def render_game(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")

        # Aesthetics only
        [background_asteroid.render() for background_asteroid in self.background_asteroids]

        # Player and bullets
        for player in self.players:
            player.render()
            [bullet.render() for bullet in player.bullets]

        # Asteroids
        [asteroid.render() for asteroid in self.asteroids]

        # Score
        score_x_loc = self.screen_width / 25
        score_y_loc = self.screen_height / 20
        self.score.render(score_x_loc, score_y_loc)

        # Draw bullets remaining and lives
        for player in self.players:
            player.draw_bullets_remaining()
            player.lives.render()
        
        # Aliens
        for alien in self.aliens:
            alien.render()

        # flip() the display
        pygame.display.flip()


    def _run_post_game(self):
        size = 100
        font_title = pygame.font.Font(self.font_path, size)
        font_play_again = pygame.font.Font(self.font_path, math.ceil(size / 2))
 
        boo = pygame.mixer.Sound("Sounds/booing_sound.wav")
        cheer = pygame.mixer.Sound("Sounds/applause.wav")
        channel = 2
        # Play Sounds
        if self.win:
            pygame.mixer.Channel(channel).play(cheer)
            status_surface = font_title.render("YOU WIN!", False, (0, 180, 0))
            for player in self.players:
                player.color = "green"
        if not self.win:
            pygame.mixer.Channel(channel).play(boo)
            status_surface = font_title.render("OOPS! YOU LOSE!", False, (180, 0, 0))
            for player in self.players:
                player.color = "red"
        
        running = True
        while running == True: # running: [True, False, "quit"]
            running = self._update_post_game(channel)
            self._render_post_game(size, font_play_again, status_surface)

        return running != "quit"
    
    def _update_post_game(self, sound_channel):
        # limits FPS to 60
        self.clock.tick(self.fps)

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Channel(sound_channel).stop()
                return False
            
        # Background Aesthetics
        [background_asteroid.update([player.position for player in self.players]) for background_asteroid in self.background_asteroids] 

        # Update rest of (inactive) game
        for player in self.players:
            if not self.win or player.is_dead():
                player.rotate_angle(1)
            else:
                player.receive_commands() 
            player.update()

        # Alien
        for alien in self.aliens:
            alien.update([player.position for player in self.players])
        
        # Asteorids
        [asteroid.update(players_pos=[player.position for player in self.players]) for asteroid in self.asteroids]

        return True
    

    def _render_post_game(self, size, font_play_again, status_surface):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")
        # Draw background asteroids before text
        [background_asteroid.render() for background_asteroid in self.background_asteroids]

        # Win / Lose text
        self.screen.blit(status_surface, (self.screen_width / 2 - size * 3, self.screen_height / 3 - size))

        # Draw Score
        size = 150
        score_x_loc = self.screen_width / 2 - size
        score_y_loc = self.screen_height / 2
        self.score.render(score_x_loc, score_y_loc, size=size)  

        # Play Again text
        play_again_surface = font_play_again.render("Click to Play Again", False, (100, 100, 100))
        self.screen.blit(play_again_surface, (self.screen_width / 2 - size * 2, self.screen_height * 4 / 5 - size / 2))
        
        # Player
        for player in self.players:
            player.render()

        # Aliens
        for alien in self.aliens:
            alien.render()

        # Asteroids
        [asteroid.render() for asteroid in self.asteroids]

        # flip() the display to put your work on screen
        pygame.display.flip()

    def _player_collision_detected(self, player: Player):
        return self._player_collision_with_asteroid_detected(player) or self._player_collision_with_alien_detected(player)
        
    def _player_collision_with_asteroid_detected(self, player: Player):
        return self._player_collision_with_thing_detected(player, self.asteroids)
    
    def _player_collision_with_alien_detected(self, player: Player):
        return self._player_collision_with_thing_detected(player, self.aliens)
    
    def _player_collision_with_thing_detected(self, player: Player, things: List):
        if not player.invincible:
            for thing in things:
                actual_distance = player.position.distance_to(thing.position)
                min_distance = player.hitbox_radius + thing.hitbox_radius
                if actual_distance <= min_distance:
                    return True
        return False
    
    def _soundify(self, *file_paths):
        return [pygame.mixer.Sound(file) for file in file_paths]
    
    def _win(self):
        self.score.win(sum([player.lives.number for player in self.players]))
        self.win = True

    def _players_have_won(self):
        return len(self.asteroids) == 0 and len(self.aliens) == 0

    def _handle_bullet_collisions(self):
        self._handle_asteroid_bullet_collisions()
        self._handle_alien_bullet_collision()
    
    def _handle_asteroid_bullet_collisions(self):
        player, bullet, asteroid = self._handle_thing_bullet_collisions(self.asteroids)
        if asteroid:
            # Update score
            self.score.asteroid_hit(asteroid.size)
            # Update bullets
            if bullet in player.bullets:
                player.bullets.remove(bullet)
            # Update asteroids
            self.asteroids.remove(asteroid)
            new_type = ASTEROID_ORDERED_SIZES[ASTEROID_ORDERED_SIZES.index(SizeType(asteroid.size)) + 1]
            if new_type is not None:
                for _ in range(2):
                    new_ast = Asteroid(self.screen, new_type, deepcopy(asteroid.position), debugging_mode=self.debugging_mode)
                    self.asteroids.append(new_ast)
            
            self._play_asteroid_sound(asteroid_size=asteroid.size)

    def _handle_alien_bullet_collision(self):
        player, bullet, alien = self._handle_thing_bullet_collisions(self.aliens)
        if alien:
            # Update score
            self.score.alien_hit()
            # Update bullets
            if bullet in player.bullets:
                player.bullets.remove(bullet)
            # Remove alien
            self.aliens.remove(alien)

            self._play_asteroid_sound(asteroid_size=SizeType.MEDIUM)

                    
    def _handle_thing_bullet_collisions(self, interactable_objects):
        for player in self.players:
            for _, bullet in enumerate(player.bullets):
                for _, interactable_object in enumerate(interactable_objects):          
                    actual_distance = bullet.position.distance_to(interactable_object.position)
                    min_distance = bullet.RADIUS + interactable_object.hitbox_radius

                    if actual_distance <= min_distance:
                        return player, bullet, interactable_object
        return None, None, None
                        # Update score
                        # self.score.alien_hit()
                    
                #     # Update bullets
                #     if bullet in player.bullets:
                #         player.bullets.remove(bullet)
                    
                #     # Remove alien
                #     self.aliens.remove(alien)

                #     if alien_index >= len(self.aliens):
                #         break
                # if bullet_index >= len(player.bullets):
                    #  break
                 

    def _play_asteroid_sound(self, asteroid_size):
        # Play asteroid explosion sound
        if asteroid_size == SizeType.LARGE.value:
            self.explosion_sounds_big_to_small[0].play()
        elif asteroid_size == SizeType.MEDIUM.value:
            self.explosion_sounds_big_to_small[1].play()
        elif asteroid_size == SizeType.SMALL.value:
            self.explosion_sounds_big_to_small[2].play()