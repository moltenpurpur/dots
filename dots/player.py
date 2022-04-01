from dots.dot import Dot
from dots.map import Map
from dots.color import Color
from typing import *


class Player:
    def __init__(self, color: Color, map_size: Tuple[int, int]):
        self.current_dot: Dot = Dot(0, 0)
        self.color: Color = color
        self.map_size: Tuple[int, int] = map_size
        self.t = 0

    def move_left(self):
        self.current_dot.x -= 1
        if self.current_dot.x == -1:
            self.current_dot.x = self.map_size[0] - 1

    def move_right(self):
        self.current_dot.x += 1
        if self.current_dot.x == self.map_size[0]:
            self.current_dot.x = 0

    def move_up(self):
        self.current_dot.y -= 1
        if self.current_dot.y == -1:
            self.current_dot.y = self.map_size[1] - 1

    def move_down(self):
        self.current_dot.y += 1
        if self.current_dot.y == self.map_size[1]:
            self.current_dot.y = 0

    def select_dot(self) -> Dot:
        return self.current_dot

    def try_set_dot_player(self, game_map: Map):
        game_map.try_set_dot(self.select_dot(), self.color)
