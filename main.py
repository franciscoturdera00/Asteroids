import argparse
import pygame
from game_logic.Game import Game

def main():
    # Adding optional argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--p2", help = "Two Player Mode", action='store_true')
    args = parser.parse_args()
    two_player = args.p2

    # Initilalize game dev lib
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("ASTEROIDS")

    # Start Game
    screen_width = 1400
    screen_height = 900
    running = True
    while running:
        game = Game(screen = pygame.display.set_mode((screen_width, screen_height)), two_player=two_player, debugging_mode=False)
        running = game.run()


if __name__ == "__main__":
    main()