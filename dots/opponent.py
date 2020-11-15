from dots.map import Map
from dots.player import Player
from dots.dot import Dot
from typing import *
import random


class Opponent(Player):
    def select_any_dot(self, game_map) -> Dot:
        empty_dots: List[Dot] = []
        for x in range(len(game_map.dots)):
            for y in range(len(game_map.dots[x])):
                if game_map.dots[x][y] is self.color.EMPTY:
                    empty_dots.append(Dot(x, y))
        return empty_dots[random.randint(0, len(empty_dots) - 1)]

    def try_set_dot_opponent(self, game_map: Map):
        game_map.try_set_dot(self.select_any_dot(game_map), self.color)
