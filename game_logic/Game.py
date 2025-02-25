
from copy import deepcopy
import math
import random
from typing import  List, Tuple, Union
import pygame

from Interactables_Objects.Alien import Alien
from Interactables_Objects.Asteroid import ASTEROID_ORDERED_SIZES, Asteroid, SizeType
from Interactables_Objects.Items.ExtraLifeItem import ExtraLifeItem
from Interactables_Objects.Items.Item import Item
from Interactables_Objects.Items.BlackHoleItem import BlackHoleItem
from Interactables_Objects.Items.PlusBulletItem import PlusBulletItem
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
        self.item_spawn_rate = .2
        
        if two_player:
            self.intial_players_positions = [(-self.screen_width / 3, self.screen_height / 2), (-self.screen_width * 2 / 3, self.screen_height / 2)]
        else:
            self.intial_players_positions = [(-self.screen_width / 2, self.screen_height / 2)]
        
        # Rates depend on number of players
        self.asteroid_spawn_rate_seconds_per_player = math.ceil(7 / len(self.intial_players_positions))
        self.alien_spawn_rate_seconds_per_player = math.ceil(12 / len(self.intial_players_positions))

        # TODO: Add a bunch of sounds
        self.background_music = pygame.mixer.Sound("Sounds/background_game_music.wav")
        self.player_hit_sound = pygame.mixer.Sound("Sounds/player_hit.wav")
        self.explosion_sounds_big_to_small = [pygame.mixer.Sound("Sounds/bangLarge.wav"),
                                              pygame.mixer.Sound("Sounds/bangMedium.wav"),
                                              pygame.mixer.Sound("Sounds/bangSmall.wav")]
        
        self.debugging_mode=debugging_mode

        self._create_game_objects()

    def _create_game_objects(self):

        # NON-INTERACTABLE OBJECTS
        # Initiate Background Aesthetics
        self.background_asteroids: List[Asteroid] = [Asteroid(self.screen, random.choice([s for s in SizeType]), background=True) for _ in range(self.num_background_asteroids)]
        
        self.picked_up_items: List[Tuple[Item, Player]] = list()

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

        self.items: List[Item] = list()
        
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
                if event.type == pygame.KEYDOWN and event.key in player.shoot:
                    player.shoot_bullet(self.score)

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
            else:
                collision = self._player_collision_detected(player)
                if collision:
                    self.score.player_hit()
                    self.player_hit_sound.play()
                    dead = player.lives.die()
                    if type(collision) == Asteroid:
                        self._update_asteroids_after_collision(collision)
                    elif type(collision) == Alien:
                        self._update_aliens_after_collision(collision)
                    if not dead:
                        player.restart_position()
        all_dead = all([player.is_dead() for player in self.players])
        if all_dead:
            return False
        
        self._handle_bullet_collisions()
        self._handle_item_player_collision()

         # Aesthetics only
        for background_asteroid in self.background_asteroids:
            background_asteroid.update()

        # Player and bullets
        for player in self.players:
            player.update()
            if not player.is_dead():
                player.receive_commands()

        # Spawn new asteroid
        if (self.game_tick / self.fps) % self.asteroid_spawn_rate_seconds_per_player == 0.0:
            new_asteroid = Asteroid(self.screen, random.choice(ASTEROID_ORDERED_SIZES[:-1]), is_in_game_spawn=True, debugging_mode=self.debugging_mode)
            self.asteroids.append(new_asteroid)
        
        # Asteroids
        for asteroid in self.asteroids:
            asteroid.update(players_pos=[player.position for player in self.players])
        
        # Spawn new Alien
        if (self.game_tick / self.fps) % self.alien_spawn_rate_seconds_per_player == 0.0:
            new_alien = Alien(self.screen, self.fps, debugging_mode=self.debugging_mode)
            self.aliens.append(new_alien)

        # Alien
        for alien in self.aliens:
            alien.update([player.position for player in self.players])

        # Score
        self.score.update()

        # Remove item if time's up
        for item in self.items:
            if item.ticks_left <= 0:
                self.items.remove(item)
                break

        # Items
        for item in self.items:
            item.update()

        for item, player in self.picked_up_items:
            item.perform_action(score=self.score, player=player, asteroids=self.asteroids, aliens=self.aliens, play_sounds_function=self._play_asteroid_sound)

        return True
    

    def render_game(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")

        # Aesthetics only
        for background_asteroid in self.background_asteroids:
            background_asteroid.render()

        for item, player in self.picked_up_items:
            cont = item.render_item_effect()
            if not cont:
                self.picked_up_items.remove((item, player))
                break

        # Player and bullets
        for player in self.players:
            player.render()
            for bullet in player.bullets:
                bullet.render()

        # Asteroids
        for asteroid in self.asteroids:
            asteroid.render()
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

        for item in self.items:
            item.render()

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
                if not player.is_dead():
                    player.color = "green"
        if not self.win:
            pygame.mixer.Channel(channel).play(boo)
            status_surface = font_title.render("YOU LOSE!", False, (180, 0, 0))
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
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pygame.mixer.Channel(sound_channel).stop()
            #     return False
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pygame.mixer.Channel(sound_channel).stop()
            return False
            
        # Background Aesthetics
        for background_asteroid in self.background_asteroids:
            background_asteroid.update([player.position for player in self.players])
                                       
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
        for asteroid in self.asteroids:
            asteroid.update(players_pos=[player.position for player in self.players])

        return True
    

    def _render_post_game(self, size, font_play_again: pygame.font.Font, status_surface):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")
        # Draw background asteroids before text
        for background_asteroid in self.background_asteroids:
            background_asteroid.render()

        # Win / Lose text
        self.screen.blit(status_surface, (self.screen_width / 5, size * 2 / 3))

        # Draw Score
        size = 150
        score_x_loc = self.screen_width / 2 - size
        score_y_loc = self.screen_height / 3 - size / 2
        self.score.render(score_x_loc, score_y_loc, size=size)  

        # Play Again text
        play_again_surface = font_play_again.render("[P] Play Again", False, (100, 100, 100))
        self.screen.blit(play_again_surface, (self.screen_width - size * 3, self.screen_height - size))
        
        # Player
        for player in self.players:
            player.render()

        # Aliens
        for alien in self.aliens:
            alien.render()

        # Asteroids
        for asteroid in self.asteroids:
            asteroid.render()

        # flip() the display to put your work on screen
        pygame.display.flip()

    def _player_collision_detected(self, player: Player) -> Union[Asteroid, Alien, None]:
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
                    return thing
        return False
    
    def _win(self):
        self.score.win(sum([player.lives.number for player in self.players]))
        self.win = True

    def _players_have_won(self):
        return len(self.asteroids) == 0 and len(self.aliens) == 0
    
    def _handle_item_player_collision(self):
        for player in self.players:
            for item in self.items:
                if item.position.distance_to(player.position) < (player.BOUNDS_RADIUS + (item.hitbox / 2)):
                    item.play_pick_up_sound()
                    self.picked_up_items.append((item, player))
                    self.items.remove(item)
                    break
                

    def _handle_bullet_collisions(self):
        self._handle_asteroid_bullet_collisions()
        self._handle_alien_bullet_collision()
    
    def _handle_asteroid_bullet_collisions(self):
        asteroid: Asteroid
        player, bullet, asteroid = self._handle_thing_bullet_collisions(self.asteroids)
        if asteroid:
            # Update bullets
            player.bullets.remove(bullet)
            # Update asteroids and its side effects
            self._update_asteroids_after_collision(asteroid)
            self._play_asteroid_sound(asteroid_size=asteroid.size)


    def _update_asteroids_after_collision(self, asteroid: Asteroid):
        # Update score
        self.score.asteroid_hit(asteroid.size)
        # Update asteroids
        self.asteroids.remove(asteroid)
        new_type = ASTEROID_ORDERED_SIZES[ASTEROID_ORDERED_SIZES.index(SizeType(asteroid.size)) + 1]

        # New Asteroids - No new ones if asteroid is smallest
        if new_type is not None:
            for _ in range(2):
                new_ast = Asteroid(self.screen, new_type, deepcopy(asteroid.position), debugging_mode=self.debugging_mode)
                self.asteroids.append(new_ast)
        # Spawn Item
        self._spawn_item_with_chance(self.item_spawn_rate, asteroid.position)


    def _handle_alien_bullet_collision(self):
        alien: Alien
        player, bullet, alien = self._handle_thing_bullet_collisions(self.aliens)
        if alien:
            # Update bullets
            player.bullets.remove(bullet)
            # Update aliens and its side effects
            self._update_aliens_after_collision(alien)
            alien.play_hit_sound()
    
    def _update_aliens_after_collision(self, alien: Alien):
        # Update score
        self.score.alien_hit()
        # Remove alien
        self.aliens.remove(alien)
        # Spawn Item
        self._spawn_item_with_chance(self.item_spawn_rate * 3, alien.position)
    
    def _spawn_item_with_chance(self, spawn_rate, position):
        if random.random() < spawn_rate:
            item = None
            bullet_item = PlusBulletItem(self.screen, self.fps, self.players, position.copy(), 5)
            nuke_item = BlackHoleItem(self.screen, self.fps, self.players, position.copy(), 7)
            extra_life_item = ExtraLifeItem(self.screen, self.fps, self.players, position.copy(), 7)
            all_items = bullet_item, nuke_item, extra_life_item

            # Probabilities are normalized. Probability values should be considered relative to their sum
            item_pobabilities = 8, 1, 1
            item_probabilities_norm = [float(prob)/sum(item_pobabilities) for prob in item_pobabilities]
            item = random.choices(all_items, weights=item_probabilities_norm)[0]
            self.items.append(item)
                    
    def _handle_thing_bullet_collisions(self, interactable_objects):
        for player in self.players:
            for _, bullet in enumerate(player.bullets):
                for _, interactable_object in enumerate(interactable_objects):          
                    actual_distance = bullet.position.distance_to(interactable_object.position)
                    min_distance = bullet.RADIUS + interactable_object.hitbox_radius

                    if actual_distance <= min_distance:
                        return player, bullet, interactable_object
        return None, None, None
                 

    def _play_asteroid_sound(self, asteroid_size):
        # Play asteroid explosion sound
        if asteroid_size == SizeType.LARGE.value:
            self.explosion_sounds_big_to_small[0].play()
        elif asteroid_size == SizeType.MEDIUM.value:
            self.explosion_sounds_big_to_small[1].play()
        elif asteroid_size == SizeType.SMALL.value:
            self.explosion_sounds_big_to_small[2].play()