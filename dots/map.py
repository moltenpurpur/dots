import collections

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
        self.dict_cycle_way: Dict[Color, List[List[Dot]]] = \
            collections.defaultdict(list)

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
        if self.players[self.set_turn] == color \
                and self.can_set_dot(target_dot):
            self[target_dot] = color
            self.set_turn += 1
            if self.set_turn >= len(self.players):
                self.set_turn = 0
            self.find_cycles_bfs(target_dot, color)

    def find_cycles_bfs(self, target_dot: Dot, color: Color):
        dict_way: Dict[Dot, Dot] = {}
        visited, queue = set(), [Dot(target_dot.x, target_dot.y)]
        visited.add(target_dot)
        previous_dot = Dot(target_dot.x, target_dot.y)
        while queue:
            current_dot = queue.pop()
            dict_way[current_dot] = previous_dot
            for neighbor in self.get_neighbor(current_dot, color):
                if neighbor not in visited \
                        or (dict_way[current_dot] != target_dot
                            and neighbor == target_dot):
                    visited.add(neighbor)
                    queue.append(neighbor)
            previous_dot = current_dot

        self.dict_cycle_way[color].append(Map.find_cycle(dict_way, target_dot))

        # for dot in dict_way:
        #     print(str(dot.x) + " " + str(dot.y) + "||" + str(
        #         dict_way[dot].x) + " " + str(dict_way[dot].y))
        # print('\n\n\n')

    def get_neighbor(self, dot: Dot, color: Color):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                current_dot = Dot(dot.x + dx, dot.y + dy)
                if 0 <= current_dot.x < self.size[0] \
                        and 0 <= current_dot.y < self.size[1] \
                        and self[current_dot] == color:
                    yield current_dot

    @staticmethod
    def find_cycle(dict_way: Dict[Dot, Dot], target_dot: Dot):
        cycle_way: List[Dot] = []
        if target_dot in dict_way:
            previous_dot = dict_way[target_dot]
            cycle_way.append(previous_dot)
            while previous_dot != target_dot:
                if previous_dot in dict_way:
                    previous_dot = dict_way[previous_dot]
                    cycle_way.append(previous_dot)

            # for dot in cycle_way:
            #     print(str(dot.x) + ' ' + str(dot.y))
            # print("\n\n")
            return cycle_way
