"""
Obstacle: a rectangular hazard the player must avoid. Touching one
costs the player a life.
"""

import pygame


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
