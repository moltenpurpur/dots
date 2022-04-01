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
        if len(empty_dots) == 0:
            return Dot(-1, -1)
        return empty_dots[random.randint(0, len(empty_dots) - 1)]

    def select_certain_dot(self):
        empty_dots: List[Dot] = [Dot(0, 1), Dot(1, 0), Dot(1, 2),
                                 Dot(2, 1), Dot(3, 3), Dot(9, 9),
                                 Dot(9, 8), Dot(9, 7), Dot(9, 6),
                                 Dot(9, 5), Dot(9, 3), Dot(9, 4),
                                 Dot(9, 2)]
        self.t += 1
        if self.t == 14:
            self.t = 1
        return empty_dots[self.t - 1]

    def select_little_smart_dot(self, game_map):
        opponent_dots = []
        neighbor_dots = []
        for x in range(len(game_map.dots)):
            for y in range(len(game_map.dots[x])):
                if game_map.dots[x][y] is self.color.RED:
                    opponent_dots.append(Dot(x, y))

        for dot in opponent_dots:
            n_dots = []
            for neighbor in game_map.get_four_neighbors(dot):
                if game_map[neighbor] == self.color.EMPTY:
                    n_dots.append(neighbor)
            if len(n_dots) > 0:
                neighbor_dots.append(n_dots)
        neighbor_dots.sort(key=lambda x: len(x))

        if len(neighbor_dots) > 0:
            flag = 0
            for n in game_map.get_four_neighbors(neighbor_dots[0][0]):
                if game_map[n] == self.color.RED:
                    flag += 1
            # if flag == 4:
            #     return self.select_little_smart_dot(game_map)
            return neighbor_dots[0][0]
        return self.select_any_dot(game_map)

    def try_set_dot_opponent(self, game_map: Map):
        game_map.try_set_dot(self.select_little_smart_dot(game_map),
                             self.color)
