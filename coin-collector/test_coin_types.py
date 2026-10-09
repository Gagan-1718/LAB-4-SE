"""
Tests for Task 2 (coin types). Run from coin-collector/:

    python -m unittest test_coin_types
"""

import unittest

from game.coin import Coin, COIN_TYPES
from game.game_engine import GameEngine


class CoinTypesTest(unittest.TestCase):
    def test_at_least_three_types_with_distinct_values_and_colors(self):
        self.assertGreaterEqual(len(COIN_TYPES), 3)
        values = [value for value, _ in COIN_TYPES.values()]
        colors = [color for _, color in COIN_TYPES.values()]
        self.assertEqual(len(set(values)), len(values))
        self.assertEqual(len(set(colors)), len(colors))

    def test_each_type_awards_its_value(self):
        for kind, expected in [("bronze", 1), ("silver", 3), ("gold", 5)]:
            with self.subTest(kind=kind):
                engine = GameEngine()
                p = engine.player
                engine.coins = [Coin.of_kind(kind, p.x, p.y)]
                for _ in range(30):
                    engine.update()
                self.assertEqual(engine.score, expected)
                self.assertEqual(engine.coins, [])

    def test_new_field_contains_every_type(self):
        kinds = {coin.kind for coin in GameEngine().coins}
        self.assertEqual(kinds, set(COIN_TYPES))


if __name__ == "__main__":
    unittest.main()
