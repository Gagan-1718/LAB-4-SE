"""
GameEngine: owns the player, coins and obstacles.

Collected coins are removed in `update` (Task 1), so each coin is scored
once. Coins come in bronze/silver/gold types (Task 2). Moving obstacles
cost a life when the player first touches one, followed by a short grace
period; the game stops at zero lives (Task 3). No timer yet.
"""

import math
import random
import pygame

from game.player import Player
from game.coin import Coin, COIN_TYPES
from game.obstacle import Obstacle
from game.collection import check_collection, touching_obstacle
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
# Screen corners covered by the HUD (top-left) and legend (top-right);
# coins don't spawn there so they're never hidden behind text.
HUD_AREAS = [pygame.Rect(0, 0, 150, 95), pygame.Rect(WIDTH - 185, 0, 185, 90)]
# Relative spawn chances: bronze is common, gold is rare.
COIN_WEIGHTS = {"bronze": 3, "silver": 2, "gold": 1}

ROUND_SECONDS = 30
RESTART_KEYS = (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE)
# Longest time step one frame may take off the clock, so a stall (e.g.
# dragging the window) doesn't drain the timer in a single frame.
MAX_FRAME_SECONDS = 0.25
# The timer turns red when this many seconds or fewer remain.
LOW_TIME_SECONDS = 5

START_LIVES = 3
# Frames of invulnerability after a hit (60 frames = 1 second).
HIT_GRACE_FRAMES = 60

NUM_OBSTACLES = 3
OBSTACLE_SIZE = 40
OBSTACLE_SPEED = (1.5, 2.5)  # min/max pixels per frame on each axis
# Obstacles never spawn inside this square around the player's start.
SAFE_ZONE = 160


class GameEngine:
    def __init__(self):
        self._big_font = None  # created on first use, needs pygame.font
        self.reset()

    def reset(self):
        """Start a fresh round: new field, score 0, full lives, full timer."""
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = self._new_coin_field()
        self.obstacles = [self._random_obstacle() for _ in range(NUM_OBSTACLES)]
        self.score = 0
        self.lives = START_LIVES
        self.was_touching = False
        self.grace_frames = 0
        self.time_left = ROUND_SECONDS

    def _new_coin_field(self):
        # One coin of every kind so all types appear, the rest random.
        coins = [self._random_coin(kind) for kind in COIN_TYPES]
        coins += [self._random_coin() for _ in range(NUM_COINS - len(COIN_TYPES))]
        return coins

    def _random_coin(self, kind=None):
        if kind is None:
            kind = random.choices(list(COIN_WEIGHTS), weights=list(COIN_WEIGHTS.values()))[0]
        while True:
            x = random.randint(30, WIDTH - 30)
            y = random.randint(30, HEIGHT - 30)
            coin = Coin.of_kind(kind, x=x, y=y, radius=12)
            near_player = self.player.get_rect().inflate(80, 80)
            if (coin.get_rect().collidelist(HUD_AREAS) == -1
                    and not coin.get_rect().colliderect(near_player)):
                return coin

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

    @property
    def round_over(self):
        """The round ends when time runs out or lives reach zero."""
        return self.time_left <= 0 or self.lives <= 0

    def handle_keydown(self, key):
        """One-shot key presses; restarts the round once it is over."""
        if self.round_over and key in RESTART_KEYS:
            self.reset()

    def handle_input(self, keys_pressed):
        if self.round_over:
            return
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

    def update(self, dt=1 / 60):
        """Advance one frame; `dt` is the real time it took, in seconds."""
        if self.round_over:
            return
        self.time_left = max(0, self.time_left - min(dt, MAX_FRAME_SECONDS))

        for obstacle in self.obstacles:
            obstacle.update(WIDTH, HEIGHT)

        # Lose a life only on the frame contact begins, not on every
        # frame the player keeps overlapping an obstacle, and never again
        # during the short grace period right after a hit.
        if self.grace_frames > 0:
            self.grace_frames -= 1
        touching = touching_obstacle(self.player, self.obstacles)
        if touching and not self.was_touching and self.grace_frames == 0:
            self.lives -= 1
            self.grace_frames = HIT_GRACE_FRAMES
        self.was_touching = touching

        # Collected coins are removed from the field so that standing on
        # one awards its value exactly once instead of every frame.
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.coins.remove(coin)
            self.score += coin.value
        # Clearing the field brings a fresh set of coins for the rest of
        # the round.
        if not self.coins:
            self.coins = self._new_coin_field()

    def draw(self, surface, font):
        from game import renderer
        # Blink the player (5 frames on, 5 off) while invulnerable after a hit.
        visible = self.grace_frames == 0 or (self.grace_frames // 5) % 2 == 0
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles, visible)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 36))
        time_color = (255, 90, 90) if self.time_left <= LOW_TIME_SECONDS else renderer.COLOR_TEXT
        renderer.draw_text(surface, font, f"Time: {math.ceil(self.time_left)}", (10, 62), time_color)
        renderer.draw_legend(surface, font, COIN_TYPES)
        if self.round_over:
            reason = "Out of lives!" if self.lives <= 0 else "Time's up!"
            if self._big_font is None:
                self._big_font = pygame.font.SysFont("consolas", 40, bold=True)
            renderer.draw_banner(surface, font, [
                reason,
                (f"Final score: {self.score}", self._big_font),
                "Press R to play again",
            ])
