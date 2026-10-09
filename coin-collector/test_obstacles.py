"""
Tests for Task 3 (obstacles and lives). Run from coin-collector/:

    python -m unittest test_obstacles
"""

import unittest

from game.game_engine import GameEngine, START_LIVES, HIT_GRACE_FRAMES
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

FAR_AWAY = (-1000, -1000)


class ObstacleTest(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.engine.coins = []
        # A single static obstacle the tests move onto/off the player.
        self.obstacle = Obstacle(*FAR_AWAY, 40, 40)
        self.engine.obstacles = [self.obstacle]

    def touch(self):
        p = self.engine.player
        self.obstacle.x, self.obstacle.y = p.x - 20, p.y - 20

    def leave(self):
        self.obstacle.x, self.obstacle.y = FAR_AWAY

    def test_touching_obstacle_costs_one_life(self):
        self.touch()
        self.engine.update()
        self.assertEqual(self.engine.lives, START_LIVES - 1)

    def test_staying_on_obstacle_costs_only_one_life(self):
        self.touch()
        for _ in range(HIT_GRACE_FRAMES * 5):
            self.engine.update()
        self.assertEqual(self.engine.lives, START_LIVES - 1)

    def test_no_second_hit_during_grace_period(self):
        self.touch()
        self.engine.update()
        self.leave()
        self.engine.update()
        self.touch()
        self.engine.update()
        self.assertEqual(self.engine.lives, START_LIVES - 1)

    def test_new_touch_after_grace_costs_another_life(self):
        self.touch()
        self.engine.update()
        self.leave()
        for _ in range(HIT_GRACE_FRAMES):
            self.engine.update()
        self.touch()
        self.engine.update()
        self.assertEqual(self.engine.lives, START_LIVES - 2)

    def test_round_stops_at_zero_lives(self):
        for _ in range(START_LIVES + 2):
            self.touch()
            self.engine.update()
            self.leave()
            for _ in range(HIT_GRACE_FRAMES):
                self.engine.update()
        self.assertEqual(self.engine.lives, 0)
        self.assertTrue(self.engine.round_over)

    def test_obstacles_stay_in_play_area(self):
        engine = GameEngine()
        for _ in range(2000):
            engine.update()
            for obstacle in engine.obstacles:
                rect = obstacle.get_rect()
                self.assertTrue(0 <= rect.left and rect.right <= WIDTH, rect)
                self.assertTrue(0 <= rect.top and rect.bottom <= HEIGHT, rect)
            if engine.round_over:
                break

    def test_obstacles_never_spawn_on_player(self):
        for _ in range(200):
            engine = GameEngine()
            player_rect = engine.player.get_rect()
            for obstacle in engine.obstacles:
                self.assertFalse(obstacle.get_rect().colliderect(player_rect))


if __name__ == "__main__":
    unittest.main()
