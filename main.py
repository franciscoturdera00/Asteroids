import pygame
from game_logic.Game import Game

def main():
    # Initilalize game dev lib
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("ASTEROIDS")

    # Start Game
    screen_width = 1700
    screen_height = 1000
    running = True
    while running:
        game = Game(screen = pygame.display.set_mode((screen_width, screen_height)), debugging_mode=True)
        running = game.run()


if __name__ == "__main__":
    main()