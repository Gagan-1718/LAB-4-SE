"""
Tests for Task 4 (timed round and restart). Run from coin-collector/:

    python -m unittest test_round
"""

import unittest

import pygame

from game.coin import Coin
from game.game_engine import GameEngine, ROUND_SECONDS, START_LIVES


class RoundTest(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.engine.obstacles = []

    def run_seconds(self, seconds, fps=60):
        for _ in range(int(seconds * fps)):
            self.engine.update(1 / fps)

    def test_round_starts_with_full_timer(self):
        self.assertEqual(self.engine.time_left, ROUND_SECONDS)
        self.assertFalse(self.engine.round_over)

    def test_timer_counts_down_in_real_seconds(self):
        self.run_seconds(10)
        self.assertAlmostEqual(self.engine.time_left, ROUND_SECONDS - 10, places=3)
        self.assertFalse(self.engine.round_over)

    def test_round_ends_when_time_runs_out(self):
        self.run_seconds(ROUND_SECONDS + 1)
        self.assertEqual(self.engine.time_left, 0)
        self.assertTrue(self.engine.round_over)

    def test_long_stall_does_not_drain_the_timer(self):
        self.engine.update(5.0)
        self.assertGreater(self.engine.time_left, ROUND_SECONDS - 1)

    def test_nothing_changes_after_round_ends(self):
        self.run_seconds(ROUND_SECONDS + 1)
        p = self.engine.player
        self.engine.coins.append(Coin.of_kind("gold", p.x, p.y))
        score = self.engine.score
        self.engine.update()
        self.assertEqual(self.engine.score, score)

    def test_restart_resets_score_lives_and_timer(self):
        self.engine.score = 42
        self.engine.lives = 1
        self.run_seconds(ROUND_SECONDS + 1)
        self.engine.handle_keydown(pygame.K_r)
        self.assertEqual(self.engine.score, 0)
        self.assertEqual(self.engine.lives, START_LIVES)
        self.assertEqual(self.engine.time_left, ROUND_SECONDS)
        self.assertFalse(self.engine.round_over)

    def test_restart_after_running_out_of_lives(self):
        self.engine.lives = 0
        self.assertTrue(self.engine.round_over)
        self.engine.handle_keydown(pygame.K_RETURN)
        self.assertEqual(self.engine.lives, START_LIVES)
        self.assertFalse(self.engine.round_over)

    def test_restart_key_ignored_mid_round(self):
        self.engine.score = 7
        self.engine.handle_keydown(pygame.K_r)
        self.assertEqual(self.engine.score, 7)

    def test_clearing_the_field_brings_new_coins(self):
        p = self.engine.player
        self.engine.coins = [Coin.of_kind("silver", p.x, p.y)]
        self.engine.update()
        self.assertEqual(self.engine.score, 3)
        self.assertGreater(len(self.engine.coins), 0)


if __name__ == "__main__":
    unittest.main()
