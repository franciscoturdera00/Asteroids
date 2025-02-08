import argparse
import pygame
from game_logic.PreGame import PreGame
from game_logic.Game import Game

def main():
    # Old way of doing 2-player
    # Leaving in case of decoupling game screens
    # Optional Arguments
    # --p2: 2-Player Mode
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--p2", help = "Two Player Mode", action='store_true')
    # args = parser.parse_args()
    # two_player = args.p2

    # Initilalize game dev lib
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("ASTEROIDS")

    # Start Game
    screen_width = 1400
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    font_path = "Fonts/novem.ttf"
    running = True
    pre_game = PreGame(screen, font_path=font_path)
    pre_game.run()
    while running:
        game = Game(screen=screen, font_path=font_path, two_player=pre_game.multiplayer, debugging_mode=False)
        running = game.run()


if __name__ == "__main__":
    main()