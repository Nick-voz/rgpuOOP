import unittest
from math import isclose

from tkinter_extended.utils import Point


class TestPoint(unittest.TestCase):

    def setUp(self):
        self.point_a = Point(3, 4)
        self.point_b = Point(0, 0)
        self.point_c = Point(3, 4)  # Same as point_a for testing distance
        self.point_d = Point(-1, -1)

    def test_initialization(self):
        self.assertEqual(self.point_a.x, 3)
        self.assertEqual(self.point_a.y, 4)

    def test_cords(self):
        self.assertEqual(self.point_a.cords(), (3, 4))
        self.assertEqual(self.point_b.cords(), (0, 0))

    def test_dist(self):
        self.assertTrue(isclose(self.point_a.dist(self.point_b), 5.0))
        self.assertTrue(isclose(self.point_a.dist(self.point_c), 0.0))
        self.assertTrue(
            isclose(self.point_b.dist(self.point_d), 1.4142135623730951)
        )

    def test_decriment_move(self):
        self.assertEqual(self.point_a.decriment_move(self.point_b), (-3, -4))
        self.assertEqual(self.point_b.decriment_move(self.point_a), (3, 4))
        self.assertEqual(self.point_a.decriment_move(self.point_d), (-4, -5))

    def test_str(self):
        self.assertEqual(str(self.point_a), "(3, 4)")
        self.assertEqual(str(self.point_b), "(0, 0)")


if __name__ == "__main__":
    unittest.main()
