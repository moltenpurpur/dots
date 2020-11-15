from dots.dot import Dot
from dots.color import Color
from typing import *


class Map:
    def __init__(self, win_size):
        self.dots: List[List[Color]] = []
        self.size: Tuple[int, int] = win_size
        self.players: List[Color] = [Color.RED, Color.BLUE]
        self.set_turn: int = 0
        self.fill_map()

    def __getitem__(self, item: Dot):
        return self.dots[item.x][item.y]

    def __setitem__(self, key, value):
        if self.dots[key.x][key.y] == Color.EMPTY:
            self.dots[key.x][key.y] = value

    def fill_map(self):
        for x in range(self.size[0]):
            dots_line = []
            for y in range(self.size[1]):
                dots_line.append(Color.EMPTY)
            self.dots.append(dots_line)

    def can_set_dot(self, dot: Dot):
        return 0 <= dot.x < len(self.dots) \
               and 0 <= dot.y < len(self.dots[dot.x]) \
               and self[dot] == Color.EMPTY

    def try_set_dot(self, target_dot: Dot, color: Color):
        if self.players[self.set_turn] == color and self.can_set_dot(
                target_dot):
            self[target_dot] = color
            self.set_turn += 1
            if self.set_turn >= len(self.players):
                self.set_turn = 0

            # self.find_cycle(target_dot)
