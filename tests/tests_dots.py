import unittest

from dots.color import Color
from dots.dot import Dot
from dots.map import Map


class TestMap(unittest.TestCase):
    def setUp(self):
        self.test_map = Map((3, 3))

    def test_fill_map(self):
        for x in self.test_map.dots:
            for y in x:
                self.assertEqual(y, Color.EMPTY)

    def test_size_map(self):
        self.assertEqual(len(self.test_map.dots), 3)
        for x in self.test_map.dots:
            self.assertEqual(len(x), 3)

    def test_drop_map(self):
        self.test_map.set_dot(Dot(1, 1), Color.RED)
        self.test_map.set_dot(Dot(2, 2), Color.BLUE)
        self.test_map.drop_map()
        for x in self.test_map.dots:
            for y in x:
                self.assertEqual(y, Color.EMPTY)

    def test_can_set_dot_in_map(self):
        self.assertEqual(self.test_map.can_set_dot(Dot(0, 0)), True)

    def test_can_set_dot_out_map(self):
        self.assertEqual(self.test_map.can_set_dot(Dot(3, 0)), False)

    def test_can_set_busy_dot(self):
        self.test_map.set_dot(Dot(1, 1), Color.BLUE)
        self.assertEqual(self.test_map.can_set_dot(Dot(1, 1)), False)

    def test_try_set_dot(self):
        self.test_map.try_set_dot(Dot(0, 0), Color.RED)
        self.assertEqual(self.test_map[Dot(0, 0)], Color.RED)

    def test_try_set_double_dot(self):
        self.test_map.try_set_dot(Dot(0, 0), Color.RED)
        self.test_map.try_set_dot(Dot(1, 1), Color.RED)
        self.assertEqual(self.test_map[Dot(1, 1)], Color.EMPTY)

    def test_find_cycles_blue(self):
        self.test_map.set_dot(Dot(0, 1), Color.BLUE)
        self.test_map.set_dot(Dot(1, 0), Color.BLUE)
        self.test_map.set_dot(Dot(2, 1), Color.BLUE)
        self.test_map.set_dot(Dot(1, 2), Color.BLUE)
        self.test_map.set_dot(Dot(1, 1), Color.RED)
        self.assertEqual(self.test_map.cycle_way[Color.BLUE], [[Dot(1, 0),
                                                                Dot(0, 1),
                                                                Dot(1, 2),
                                                                Dot(2, 1),
                                                                Dot(1, 0)]])

    def test_find_cycles_red(self):
        self.test_map.set_dot(Dot(0, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 0), Color.RED)
        self.test_map.set_dot(Dot(2, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 2), Color.RED)
        self.test_map.set_dot(Dot(1, 1), Color.BLUE)
        self.assertEqual(self.test_map.cycle_way[Color.RED], [[Dot(1, 0),
                                                               Dot(0, 1),
                                                               Dot(1, 2),
                                                               Dot(2, 1),
                                                               Dot(1, 0)]])

    def test_find_several_cycles(self):
        self.test_map = Map((4, 4))
        self.test_map.set_dot(Dot(1, 1), Color.RED)
        self.test_map.set_dot(Dot(2, 2), Color.RED)
        s = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)]
        for i in s:
            self.test_map.set_dot(Dot(i[0], i[1]), Color.BLUE)
        cycles = [[Dot(1, 0), Dot(0, 1), Dot(1, 2), Dot(2, 1), Dot(1, 0)],
                  [Dot(3, 2), Dot(2, 1), Dot(1, 2), Dot(2, 3), Dot(3, 2)]]
        self.assertEqual(self.test_map.cycle_way[Color.BLUE], cycles)

    def test_get_blocked(self):
        self.assertEqual(self.test_map.get_blocked(Color.RED, {Dot(1, 1)}), [])

    def test_is_dot_on_border(self):
        self.assertEqual(self.test_map.is_dot_on_border(Dot(0, 1)), True)
        self.assertEqual(self.test_map.is_dot_on_border(Dot(2, 1)), True)

    def test_is_dot_not_on_border(self):
        self.assertEqual(self.test_map.is_dot_on_border(Dot(1, 1)), False)

    def test_get_four_neighbors(self):
        self.assertEqual(self.test_map.get_four_neighbors(Dot(1, 1)),
                         [Dot(0, 1), Dot(1, 0), Dot(1, 2), Dot(2, 1)])

    def test_get_four_neighbors_in_corner(self):
        self.assertEqual(self.test_map.get_four_neighbors(Dot(0, 0)),
                         [Dot(0, 1), Dot(1, 0)])

    def test_get_four_neighbors_on_border(self):
        self.assertEqual(self.test_map.get_four_neighbors(Dot(0, 1)),
                         [Dot(0, 0), Dot(0, 2), Dot(1, 1)])

    def test_get_all_neighbor(self):
        self.assertEqual(self.test_map.get_all_neighbor(Dot(1, 1)),
                         [Dot(0, 0), Dot(0, 1), Dot(0, 2), Dot(1, 0),
                          Dot(1, 2), Dot(2, 0), Dot(2, 1), Dot(2, 2)])

    def test_get_all_neighbor_in_corner(self):
        self.assertEqual(self.test_map.get_all_neighbor(Dot(0, 0)),
                         [Dot(0, 1), Dot(1, 0), Dot(1, 1)])

    def test_get_all_neighbor_on_border(self):
        self.assertEqual(self.test_map.get_all_neighbor(Dot(0, 1)),
                         [Dot(0, 0), Dot(0, 2), Dot(1, 0), Dot(1, 1),
                          Dot(1, 2)])

    def test_get_opponent_color_red(self):
        self.assertEqual(self.test_map.get_opponent_color(Color.BLUE),
                         Color.RED)

    def test_get_opponent_color_blue(self):
        self.assertEqual(self.test_map.get_opponent_color(Color.RED),
                         Color.BLUE)

    def test_update_score(self):
        self.test_map.set_dot(Dot(0, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 0), Color.RED)
        self.test_map.set_dot(Dot(2, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 2), Color.RED)
        self.test_map.set_dot(Dot(1, 1), Color.BLUE)
        self.test_map.update_score()
        self.assertEqual(self.test_map.score[Color.RED], 1)

    def test_get_count(self):
        self.test_map.set_dot(Dot(1, 1), Color.BLUE)
        self.test_map.set_dot(Dot(2, 2), Color.BLUE)
        self.assertEqual(
            self.test_map.get_count(Color.BLUE, [{Dot(1, 1), Dot(2, 2)}]), 2)

    def test_fill_blocked(self):
        self.test_map.set_dot(Dot(0, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 0), Color.RED)
        self.test_map.set_dot(Dot(2, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 2), Color.RED)
        self.test_map.set_dot(Dot(1, 1), Color.BLUE)
        self.test_map.fill_blocked()
        self.assertEqual(self.test_map.blocked, {Dot(1, 1)})

    def test_fill_blocked_empty(self):
        self.test_map.set_dot(Dot(0, 1), Color.RED)
        self.test_map.set_dot(Dot(1, 0), Color.RED)
        self.test_map.fill_blocked()
        self.assertEqual(self.test_map.blocked, set())

    def test_writing_to_sequence(self):
        self.test_map.try_set_dot(Dot(1, 2), Color.RED)
        self.test_map.try_set_dot(Dot(1, 1), Color.BLUE)
        self.assertEqual(self.test_map.dot_sequence,
                         [(Dot(1, 2), Color.RED), (Dot(1, 1), Color.BLUE)])
