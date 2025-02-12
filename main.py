import argparse
from typing import List, Tuple
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
        update_high_score("test", game.score.score)
    
    # deactivates the pygame library
    pygame.quit()


def update_high_score(user, score, max_saved=15):
    high_scores: List[Tuple[str,int]] = get_current_high_scores()
    high_scores.append((user, score))
    high_scores = sorted(high_scores, key=lambda score: score[1], reverse=True)
    high_scores = high_scores[:max_saved]
    store_high_score(high_scores)

def get_current_high_scores():
    try:
        # Reading high score file
        with open("shared_info/high_score") as file:
            scores = list()
            for line in file.readlines():
                user, score = line.split("=")
                scores.append((user, int(score)))
        return scores
    except:
        return list()


def store_high_score(scores:List[Tuple[str,int]]): # Ordered list
    # Writing high score file (overwrites existing content)
    with open("shared_info/high_score", "w") as file:
        for score in scores:
            file.write(score[0] + "=" + str(score[1]) + "\n")

if __name__ == "__main__":
    main()