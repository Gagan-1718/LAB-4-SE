"""
GameEngine: owns the player and all coins.

Coins come in bronze/silver/gold types (Task 2); no obstacles or timer
yet. Collected coins are removed in `update` (Task 1), so each coin is
scored once.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin, COIN_TYPES
from game.obstacle import Obstacle
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
# Relative spawn chances: bronze is common, gold is rare.
COIN_WEIGHTS = {"bronze": 3, "silver": 2, "gold": 1}

NUM_OBSTACLES = 3
OBSTACLE_SIZE = 40
OBSTACLE_SPEED = (1.5, 2.5)  # min/max pixels per frame on each axis
# Obstacles never spawn inside this square around the player's start.
SAFE_ZONE = 160


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        # One coin of every kind so all types appear, the rest random.
        self.coins = [self._random_coin(kind) for kind in COIN_TYPES]
        self.coins += [self._random_coin() for _ in range(NUM_COINS - len(COIN_TYPES))]
        self.obstacles = [self._random_obstacle() for _ in range(NUM_OBSTACLES)]
        self.score = 0

    def _random_coin(self, kind=None):
        if kind is None:
            kind = random.choices(list(COIN_WEIGHTS), weights=list(COIN_WEIGHTS.values()))[0]
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        return Coin.of_kind(kind, x=x, y=y, radius=12)

    def _random_obstacle(self):
        safe = pygame.Rect(0, 0, SAFE_ZONE, SAFE_ZONE)
        safe.center = (int(self.player.x), int(self.player.y))
        while True:
            x = random.randint(0, WIDTH - OBSTACLE_SIZE)
            y = random.randint(0, HEIGHT - OBSTACLE_SIZE)
            vx = random.uniform(*OBSTACLE_SPEED) * random.choice((-1, 1))
            vy = random.uniform(*OBSTACLE_SPEED) * random.choice((-1, 1))
            obstacle = Obstacle(x, y, OBSTACLE_SIZE, OBSTACLE_SIZE, vx, vy)
            if not obstacle.get_rect().colliderect(safe):
                return obstacle

    def handle_input(self, keys_pressed):
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        for obstacle in self.obstacles:
            obstacle.update(WIDTH, HEIGHT)

        # Collected coins are removed from the field so that standing on
        # one awards its value exactly once instead of every frame.
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.coins.remove(coin)
            self.score += coin.value

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_legend(surface, font, COIN_TYPES)
