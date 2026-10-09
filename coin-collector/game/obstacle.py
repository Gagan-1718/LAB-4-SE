"""
Obstacle: a rectangular hazard that drifts around the play area,
bouncing off its edges. Touching one costs the player a life.
"""

import pygame


class Obstacle:
    def __init__(self, x, y, width, height, vx=0, vy=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy

    def update(self, bounds_width, bounds_height):
        """Move by the velocity, bouncing off the play-area edges."""
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x + self.width > bounds_width:
            self.vx = -self.vx
            self.x = max(0, min(bounds_width - self.width, self.x))
        if self.y < 0 or self.y + self.height > bounds_height:
            self.vy = -self.vy
            self.y = max(0, min(bounds_height - self.height, self.y))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
