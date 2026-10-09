"""
Regression tests for Task 1 (coin collection). Run from coin-collector/:

    python -m unittest test_collection
"""

import unittest

from game.coin import Coin
from game.game_engine import GameEngine


class CoinCollectionTest(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        p = self.engine.player
        self.coin = Coin(x=p.x, y=p.y, value=1)
        self.far_coin = Coin(x=p.x + 200, y=p.y, value=1)
        self.engine.coins = [self.coin, self.far_coin]

    def test_coin_scored_once_while_standing_on_it(self):
        for _ in range(100):
            self.engine.update()
        self.assertEqual(self.engine.score, 1)

    def test_collected_coin_is_removed(self):
        self.engine.update()
        self.assertNotIn(self.coin, self.engine.coins)
        self.assertIn(self.far_coin, self.engine.coins)


if __name__ == "__main__":
    unittest.main()
