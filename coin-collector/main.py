"""
Coin Collector (Lab Starter)

Run with:  python3 main.py

Controls: Arrow keys to move.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Coin Collector")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    engine = GameEngine()
    running = True
    dt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        engine.handle_input(keys)
        engine.update(dt)
        engine.draw(screen, font)

        pygame.display.flip()
        # Seconds since the last frame, so the round timer uses real time.
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
